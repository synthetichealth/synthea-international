#!/usr/bin/env python3
"""Build the Japan (jp) configuration for Synthea from open data.

Usage:
    python3 scripts/jp/build_jp.py [--cache DIR]

The script downloads the source files into the cache directory (default:
scripts/jp/.cache) and writes the Synthea input files into jp/src/main/resources.

Sources (see jp/README_jp.md for licenses):
  - 2020 Census, e-Stat table 2-7 (population by municipality, 5-year age group and sex)
  - Japan Post postal code list in romaji (KEN_ALL_ROME)
  - GeoNames postal codes for Japan (JP.zip), for latitude and longitude
  - MHLW medical facility open data (hospitals, clinics, hospital departments)

Only the Python standard library and openpyxl are needed.
"""

import argparse
import csv
import io
import os
import re
import statistics
import sys
import unicodedata
import urllib.request
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "jp", "src", "main", "resources")

CENSUS_URL = ("https://www.e-stat.go.jp/stat-search/file-download"
              "?statInfId=000032142410&fileKind=0")
POST_URL = ("https://www.post.japanpost.jp/service/search/zipcode/download/"
            "roman/KEN_ALL_ROME.zip")
GEONAMES_URL = "https://download.geonames.org/export/zip/JP.zip"
MHLW_BASE = "https://www.mhlw.go.jp/content/11121000/"
MHLW_DATE = "20260601"
MHLW_FILES = {
    "hospital": "01-1_hospital_facility_info_%s.csv.zip" % MHLW_DATE,
    "clinic": "02-1_clinic_facility_info_%s.csv.zip" % MHLW_DATE,
    "hospital_departments": "01-2_hospital_speciality_hours_%s.csv.zip" % MHLW_DATE,
}

# Synthea "state" = region (chihō), "county" = prefecture, "city" = municipality.
# The three-letter codes avoid clashes with US state codes in the default Synthea files.
REGIONS = [
    ("Hokkaidō", "HKD", [1]),
    ("Tōhoku", "THK", [2, 3, 4, 5, 6, 7]),
    ("Kantō", "KNT", [8, 9, 10, 11, 12, 13, 14]),
    ("Chūbu", "CHB", [15, 16, 17, 18, 19, 20, 21, 22, 23]),
    ("Kinki", "KNK", [24, 25, 26, 27, 28, 29, 30]),
    ("Chūgoku", "CGK", [31, 32, 33, 34, 35]),
    ("Shikoku", "SKK", [36, 37, 38, 39]),
    ("Kyūshū", "KYS", [40, 41, 42, 43, 44, 45, 46, 47]),
]
PREF_TO_REGION = {p: (name, st) for name, st, prefs in REGIONS for p in prefs}

PREFECTURES = [
    "Hokkaido", "Aomori", "Iwate", "Miyagi", "Akita", "Yamagata", "Fukushima",
    "Ibaraki", "Tochigi", "Gunma", "Saitama", "Chiba", "Tokyo", "Kanagawa",
    "Niigata", "Toyama", "Ishikawa", "Fukui", "Yamanashi", "Nagano", "Gifu",
    "Shizuoka", "Aichi", "Mie", "Shiga", "Kyoto", "Osaka", "Hyogo", "Nara",
    "Wakayama", "Tottori", "Shimane", "Okayama", "Hiroshima", "Yamaguchi",
    "Tokushima", "Kagawa", "Ehime", "Kochi", "Fukuoka", "Saga", "Nagasaki",
    "Kumamoto", "Oita", "Miyazaki", "Kagoshima", "Okinawa",
]

# Household income: share of households by income in steps of 1 million yen,
# from under 1 million yen to 20 million yen and over. 2024 Comprehensive Survey of
# Living Conditions (MHLW), figure 9 (income in 2023).
HOUSEHOLD_INCOME_PCT = [6.7, 14.4, 14.4, 13.1, 9.9, 8.5, 7.6, 5.4, 4.4, 3.3, 2.8,
                        2.0, 1.6, 1.0, 0.9, 0.8, 0.6, 0.4, 0.4, 0.4, 1.4]
YEN_PER_DOLLAR = 150
# Synthea income bands, in thousands of US dollars.
INCOME_BANDS = [(0, 10), (10, 15), (15, 25), (25, 35), (35, 50), (50, 75), (75, 100),
                (100, 150), (150, 200), (200, 999)]


def income_shares():
    """Spread each 1-million-yen step evenly over the Synthea bands it overlaps.
    The survey does not split 20 million yen and over; we assume a third of it
    in each of 20-22.5, 22.5-30 and over 30 million yen."""
    steps = [(i * 100, (i + 1) * 100, pct) for i, pct in enumerate(HOUSEHOLD_INCOME_PCT[:-1])]
    top = HOUSEHOLD_INCOME_PCT[-1] / 3
    steps += [(2000, 2250, top), (2250, 3000, top), (3000, 15000, top)]
    shares = []
    for lo_k, hi_k in INCOME_BANDS:
        lo, hi = lo_k * 1000 * YEN_PER_DOLLAR / 10000, hi_k * 1000 * YEN_PER_DOLLAR / 10000
        shares.append(sum(pct * max(0, min(hi, b) - max(lo, a)) / (b - a)
                          for a, b, pct in steps))
    total = sum(shares)
    return [round(x / total, 6) for x in shares]


INCOME = income_shares()
# Education is not built from Japanese data yet. These are the same values used
# for the European folders in this repository.
EDUCATION = [0.4481645824929407, 0.036506655909640987, 0.409035901573215,
             0.10629286002420331]
# Unemployment: 2.8% in 2020 (Labour Force Survey, Statistics Bureau of Japan).
# Uninsured: 0, because everyone is covered by public health insurance.
# The other three values are placeholders copied from the European folders.
SDOH = {"FOOD_INSECURITY": 0.15, "SEVERE_HOUSING_COST_BURDEN": 0.15,
        "UNEMPLOYED": 0.028, "NO_VEHICLE_ACCESS": 0.15, "UNINSURED": 0.0}


def fetch(url, path):
    if not os.path.exists(path):
        print("downloading", url)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(path + ".part", "wb") as f:
            f.write(data)
        os.replace(path + ".part", path)
    return path


def read_zip_csv(path, encoding):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.lower().endswith((".csv", ".txt"))
                 and "readme" not in n.lower()]
        name = names[0]
        return z.read(name).decode(encoding)


def nfkc(s):
    # NFKC also turns the ideographic space into a normal space
    s = unicodedata.normalize("NFKC", s or "").replace(" ", "")
    return s.replace("惠", "恵")  # 須惠町 in the post code list, 須恵町 in the census


def title_romaji(words):
    """'SAPPORO SHI' -> 'Sapporo', 'TOMA CHO' -> 'Toma-cho'."""
    words = [w for w in words.split() if w]
    suffix = words[-1] if words else ""
    base = " ".join(w.capitalize() for w in words[:-1])
    if suffix in ("SHI", "KU"):
        return base
    if suffix in ("CHO", "MACHI", "MURA", "SON"):
        return "%s-%s" % (base, suffix.lower())
    return " ".join(w.capitalize() for w in words)


# KEN_ALL_ROME cuts municipality names at 35 characters. Suffix for names
# that lost it completely.
CUT_SUFFIX = {"19346": "CHO"}  # Ichikawamisato-cho (Yamanashi)
KANJI_SUFFIX = {"町": ("CHO", "MACHI"), "村": ("MURA", "SON")}


def town_words(code, muni_k, muni_r):
    """Romaji words of a town or village, without the district (gun)."""
    words = muni_r.split()
    if "GUN" in words:
        words = words[words.index("GUN") + 1:]
    elif "\u3000" in muni_k:
        # "MIYAKEJIMA MIYAKE MURA" -> "MIYAKE MURA"
        words = words[-2:]
    suffixes = KANJI_SUFFIX.get(muni_k[-1])
    if suffixes and words[-1] not in suffixes:
        cut = [x for x in suffixes if len(words) > 1 and x.startswith(words[-1])]
        if len(cut) == 1:
            words[-1] = cut[0]
        elif code in CUT_SUFFIX:
            words.append(CUT_SUFFIX[code])
        else:
            sys.exit("cannot read the romaji name of %s %s: %s" % (code, muni_k, muni_r))
    return " ".join(words)


# ---------------------------------------------------------------- census

def load_census(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.worksheets[0]
    rows = []
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i < 12 or r[0] != "0_国籍総数":
            continue
        rows.append(r)
    # kind: a = nation/prefecture, 1 = designated city or Tokyo special wards,
    # 0 = ward, 2 = city, 3 = town or village, 9 = municipality as of 2000 (skipped)
    units = {}
    order = []
    parent = None
    for r in rows:
        kind, code, name = r[2], r[7], r[8].split("_", 1)[1]
        if kind in ("a", "9"):
            if kind == "a":
                parent = None
            continue
        if kind == "1":
            parent = code
        if kind == "0":
            continue  # wards are counted in their parent city
        if kind in ("2", "3"):
            parent = None
        u = units.setdefault(code, {"code": code, "name": name, "kind": kind,
                                    "pref": int(code[:2]), "age": {}, "sex": {}})
        if code not in order:
            order.append(code)
        sex = r[1]
        vals = list(r[9:])
        # columns: total, 0-4 ... 95-99, 100+, then summary groups
        five = [float(v) if isinstance(v, (int, float)) else 0.0 for v in vals[1:22]]
        total = float(vals[0]) if isinstance(vals[0], (int, float)) else 0.0
        u["sex"][sex] = total
        if sex == "0_総数":
            u["age"] = five[:17] + [sum(five[17:])]
            u["total"] = total
    # Futaba-machi (Fukushima) had no residents on census day, so it is left out.
    return [units[c] for c in order if units[c].get("total")]


# ---------------------------------------------------------------- post codes

def load_post(path):
    text = read_zip_csv(path, "cp932")
    out = []
    for row in csv.reader(io.StringIO(text)):
        zipc, pref_k, muni_k, _town, _pref_r, muni_r = row[:6]
        out.append((zipc, pref_k, muni_k, muni_r))
    return out


def load_geonames(path):
    text = read_zip_csv(path, "utf-8")
    coords = defaultdict(list)
    for line in text.splitlines():
        f = line.split("\t")
        if len(f) < 11 or not f[9]:
            continue
        coords[f[1].replace("-", "")].append((float(f[9]), float(f[10])))
    return {z: (statistics.mean(a for a, _ in v), statistics.mean(b for _, b in v))
            for z, v in coords.items()}


def build(cache):
    os.makedirs(cache, exist_ok=True)
    census = load_census(fetch(CENSUS_URL, os.path.join(cache, "census_2020_2-7.xlsx")))
    post = load_post(fetch(POST_URL, os.path.join(cache, "KEN_ALL_ROME.zip")))
    geo = load_geonames(fetch(GEONAMES_URL, os.path.join(cache, "JP.zip")))

    # Map (prefecture, municipality name in kanji) -> census unit
    by_name = {}
    designated = {}   # (pref, "札幌市") -> unit
    for u in census:
        key = (u["pref"], nfkc(u["name"]))
        by_name[key] = u
        if u["kind"] == "1":
            designated[key] = u

    def pref_code_of(pref_k):
        return PREF_KANJI.index(pref_k) + 1

    def unit_of(pref_k, muni_k):
        p = pref_code_of(pref_k)
        m = nfkc(muni_k)
        if p == 13 and m.endswith("区"):
            return by_name.get((13, "特別区部"))
        for (dp, dname), u in designated.items():
            if dp == p and m.startswith(dname) and dname != "特別区部":
                return u
        # "上川郡　当麻町" -> "当麻町", "三宅島　三宅村" -> "三宅村"
        return by_name.get((p, nfkc(muni_k.split("\u3000")[-1])))

    # romaji names
    romaji = {}
    district = {}
    zips = defaultdict(set)
    unmatched = set()
    for zipc, pref_k, muni_k, muni_r in post:
        u = unit_of(pref_k, muni_k)
        if u is None:
            unmatched.add((pref_k, muni_k))
            continue
        zips[u["code"]].add(zipc)
        if u["code"] in romaji:
            continue
        if u["kind"] == "1":
            romaji[u["code"]] = "Tokyo" if u["pref"] == 13 else title_romaji(
                muni_r.split(" SHI ")[0] + " SHI")
        else:
            gun = re.match(r"^(.*?) GUN ", muni_r)
            if gun:
                district[u["code"]] = gun.group(1).title()
            romaji[u["code"]] = title_romaji(town_words(u["code"], muni_k, muni_r))
    if unmatched:
        print("post code municipalities not in the 2020 census:", sorted(unmatched))

    # make names unique within a region
    seen = defaultdict(list)
    for u in census:
        u["city"] = romaji.get(u["code"])
        if u["city"] is None:
            print("no romaji name for", u["code"], u["name"])
            continue
        seen[(PREF_TO_REGION[u["pref"]][0], u["city"])].append(u)
    for (_, city), us in seen.items():
        if len(us) > 1:
            prefs = [u["pref"] for u in us]
            for u in us:
                if prefs.count(u["pref"]) > 1:
                    # same name in the same prefecture: add the district (gun)
                    u["city"] = "%s (%s)" % (city, district[u["code"]])
                else:
                    u["city"] = "%s (%s)" % (city, PREFECTURES[u["pref"] - 1])
    census = [u for u in census if u.get("city")]

    by_code = {u["code"]: u for u in census}
    facilities = {kind: read_mhlw(cache, kind) for kind in ("hospital", "clinic")}

    # coordinates per municipality: the average of its postal codes in GeoNames, or
    # of its medical facilities when none of its postal codes is in GeoNames
    # (the islands of Miyake, Mikurajima, Hachijo and Aogashima)
    fac_points = defaultdict(list)
    for rs in facilities.values():
        for r in rs:
            code = unit_code(by_code, r["都道府県コード"], r["市区町村コード"])
            pt = facility_point(r)
            if code and pt:
                fac_points[code].append(pt)
    centroid = {}
    for u in census:
        pts = [geo[z] for z in zips[u["code"]] if z in geo] or fac_points[u["code"]]
        if pts:
            centroid[u["code"]] = (statistics.mean(a for a, _ in pts),
                                   statistics.mean(b for _, b in pts))
        else:
            print("no coordinates for", u["code"], u["name"])
    all_zips = set(z for zs in zips.values() for z in zs)
    print("postal codes: Japan Post %d, found in GeoNames %d, GeoNames only %d"
          % (len(all_zips), len(all_zips & set(geo)), len(set(geo) - all_zips)))

    write_geography(census, zips, geo, centroid)
    write_providers(cache, facilities, by_code, zips, geo, centroid)
    write_payers()


PREF_KANJI = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県",
    "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県",
    "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府",
    "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県",
    "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県",
    "鹿児島県", "沖縄県",
]


def unit_code(by_code, pref, muni):
    """Map a 5-digit municipality code (wards included) to a census unit code."""
    code = "%02d%03d" % (int(pref), int(muni))
    if code in by_code:
        return code
    if code[:2] == "13" and "101" <= code[2:] <= "123":
        return "13100"
    # A ward of a designated city has a code just after its city's code, for example
    # Kitakyushu 40100 (wards 40101-40107) and Fukuoka 40130 (wards 40131-40137).
    # This also covers the wards of Hamamatsu created in 2024 (22138-22140).
    if code[2] == "1":
        parents = [c for c, u in by_code.items()
                   if u["kind"] == "1" and c[:2] == code[:2] and c <= code]
        if parents:
            return max(parents)
    return None


def facility_point(r):
    """Coordinates of a facility, or None when missing (some rows have 0.0) or outside Japan."""
    try:
        lat, lon = float(r["所在地座標（緯度）"]), float(r["所在地座標（経度）"])
    except ValueError:
        return None
    if 20 <= lat <= 46 and 122 <= lon <= 154:
        return lat, lon
    return None


def writer(path, header):
    f = open(path, "w", newline="", encoding="utf-8")
    w = csv.writer(f, lineterminator="\n")
    w.writerow(header)
    return f, w


def write_geography(census, zips, geo, centroid):
    g = os.path.join(OUT, "geography")
    os.makedirs(g, exist_ok=True)
    header = ["ID", "COUNTY", "NAME", "STNAME", "POPESTIMATE2015", "CTYNAME", "TOT_POP",
              "TOT_MALE", "TOT_FEMALE", "WHITE", "HISPANIC", "BLACK", "ASIAN", "NATIVE",
              "OTHER"] + [str(i) for i in range(1, 19)] + [
              "00..10", "10..15", "15..25", "25..35", "35..50", "50..75", "75..100",
              "100..150", "150..200", "200..999",
              "LESS_THAN_HS", "HS_DEGREE", "SOME_COLLEGE", "BS_DEGREE"]
    f, w = writer(os.path.join(g, "demographics.csv"), header)
    for u in census:
        region = PREF_TO_REGION[u["pref"]][0]
        total = u["total"]
        m, fe = u["sex"].get("1_男", 0), u["sex"].get("2_女", 0)
        age_total = sum(u["age"]) or 1
        w.writerow([u["code"], u["pref"], u["city"], region, int(total),
                    PREFECTURES[u["pref"] - 1], int(total),
                    round(m / (m + fe), 6), round(fe / (m + fe), 6),
                    0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
                   + [round(a / age_total, 6) for a in u["age"]] + INCOME + EDUCATION)
    f.close()

    f, w = writer(os.path.join(g, "zipcodes.csv"), ["", "USPS", "ST", "NAME", "ZCTA5",
                                                     "LAT", "LON"])
    i = 0
    for u in census:
        region, st = PREF_TO_REGION[u["pref"]]
        for z in sorted(zips[u["code"]]):
            lat, lon = geo.get(z, centroid.get(u["code"], (None, None)))
            if lat is None:
                continue
            w.writerow([i, region, st, u["city"], "%s-%s" % (z[:3], z[3:]),
                        round(lat, 4), round(lon, 4)])
            i += 1
    f.close()

    f, w = writer(os.path.join(g, "timezones.csv"), ["STATE", "ST", "TIMEZONE", "TZ"])
    for name, st, _ in REGIONS:
        w.writerow([name, st, "Japan Standard Time", "JST"])
    f.close()

    f, w = writer(os.path.join(g, "sdoh.csv"), ["FIPS_CODE", "COUNTY_CODE", "COUNTY", "ST",
                                                 "STATE"] + list(SDOH))
    for p in range(1, 48):
        region, st = PREF_TO_REGION[p]
        w.writerow([p, p, PREFECTURES[p - 1], st, region] + list(SDOH.values()))
    f.close()


def read_mhlw(cache, key):
    path = fetch(MHLW_BASE + MHLW_FILES[key], os.path.join(cache, MHLW_FILES[key]))
    text = read_zip_csv(path, "utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def write_providers(cache, facilities, by_code, zips, geo, centroid):
    p = os.path.join(OUT, "providers")
    os.makedirs(p, exist_ok=True)
    departments = read_mhlw(cache, "hospital_departments")
    emergency = {r["ID"] for r in departments if "救急" in r["診療科目名"]}

    def nearest_zip(code, lat, lon):
        best, dist = "", None
        # sorted, so that ties always pick the same code
        for z in sorted(zips.get(code, ())):
            zp = geo.get(z, centroid[code])
            if zp:
                d = (zp[0] - lat) ** 2 + (zp[1] - lon) ** 2
                if dist is None or d < dist:
                    best, dist = z, d
        return "%s-%s" % (best[:3], best[3:]) if best else ""

    header = ["id", "name", "address", "city", "state", "zip", "county", "phone", "type",
              "ownership", "emergency", "quality", "bed_count", "mhlw_id", "LAT", "LON"]
    rows = {"hospital": [], "clinic": []}
    next_id = {"hospital": 1, "clinic": 100001}
    skipped = 0
    no_point = 0
    for kind in ("hospital", "clinic"):
        for r in facilities[kind]:
            code = unit_code(by_code, r["都道府県コード"], r["市区町村コード"])
            if code is None or code not in centroid:
                skipped += 1
                continue
            pt = facility_point(r)
            if pt is None:
                # missing coordinates: use the centre of the municipality
                pt = centroid[code]
                no_point += 1
            lat, lon = round(pt[0], 6), round(pt[1], 6)
            u = by_code[code]
            region, _ = PREF_TO_REGION[u["pref"]]
            name = r["英語表記（ローマ字表記）"].strip() or nfkc(r["正式名称"])
            beds = r.get("合計病床数", "").strip()
            rows[kind].append([next_id[kind], name, r["所在地"].strip(), u["city"], region,
                               nearest_zip(code, lat, lon), PREFECTURES[u["pref"] - 1], "",
                               kind, "", "true" if r["ID"] in emergency else "false", "",
                               beds, r["ID"], lat, lon])
            next_id[kind] += 1
    print("hospitals %d, clinics %d, skipped %d (no municipality), "
          "placed at the municipality centre %d (no coordinates)"
          % (len(rows["hospital"]), len(rows["clinic"]), skipped, no_point))

    for fname, data in (("hospitals.csv", rows["hospital"]),
                        ("urgent_care_facilities.csv", rows["hospital"]),
                        ("primary_care_facilities.csv", rows["clinic"] + rows["hospital"])):
        f, w = writer(os.path.join(p, fname), header)
        for row in data:
            w.writerow(row)
        f.close()


# Yearly cap on what a patient pays. Japan caps monthly payments (the high-cost medical
# expense benefit). Since August 2026 there is also a yearly cap: 530,000 yen for a
# middle-income patient (MHLW). Synthea costs are in US dollars, so this is about
# 3,600 at 150 yen to the dollar.
MAX_OUT_OF_POCKET = 3600


def write_payers():
    p = os.path.join(OUT, "payers")
    os.makedirs(p, exist_ok=True)
    name = "Japan Public Health Insurance"
    f, w = writer(os.path.join(p, "insurance_companies.csv"),
                  ["Id", "Name", "Address", "City", "State Headquarterd", "Zip", "Phone",
                   "States Covered", "Ownership"])
    w.writerow([10000, name, "", "", "", "", "", "*", "Government"])
    f.close()

    # Patient share: 20% under age 6, 30% from 6 to 69, 20% from 70 to 74, 10% from 75.
    # "Default Coinsurance" is the share paid by the payer.
    # A lower Priority Level wins, so each person gets the plan for their age.
    f, w = writer(os.path.join(p, "insurance_plans.csv"),
                  ["Payer Id", "Plan Id", "Name", "Services Covered", "Deductible",
                   "Default Coinsurance", "Default Copay", "Monthly Premium",
                   "Max Out of Pocket", "Medicare Supplement", "Is ACA Plan",
                   "Income Based Premium", "Eligibility Policy", "Start Year", "End Year",
                   "Priority Level", "Notes"])
    plans = [
        (10001, "Public Health Insurance (age 75 and over)", 0.9, "Age75", 1),
        (10002, "Public Health Insurance (age 70 to 74)", 0.8, "Age70", 2),
        (10003, "Public Health Insurance (age 6 to 69)", 0.7, "Age6", 3),
        (10004, "Public Health Insurance (under age 6)", 0.8, "Everyone", 4),
    ]
    for plan_id, plan_name, coins, elig, prio in plans:
        w.writerow([10000, plan_id, plan_name, "*", 0, coins, 0, 0, MAX_OUT_OF_POCKET, "false",
                    "false", "false", elig, 0, "", prio, ""])
    f.close()

    f, w = writer(os.path.join(p, "insurance_eligibilities.csv"),
                  ["Name", "Poverty Multiplier", "Income Threshold", "Age Threshold",
                   "Qualifying Codes", "Qualifying Attributes", "Poverty Multiplier File",
                   "Spenddown File", "Acceptance Likelihood", "Sub-Eligibilities",
                   "Logical Operator", "Notes"])
    w.writerow(["Everyone", "", "", 0, "", "", "", "", "", "", "and", ""])
    for age in (6, 70, 75):
        w.writerow(["Age%d" % age, "", "", age, "", "", "", "", "", "", "and", ""])
    f.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(HERE, ".cache"))
    args = ap.parse_args()
    build(args.cache)
