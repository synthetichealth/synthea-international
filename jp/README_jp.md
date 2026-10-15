# Japan (jp)

This folder configures Synthea for Japan. It is a first version. It runs, but many parts are simplified (see "Limitations").

## How to run

```
git clone https://github.com/synthetichealth/synthea
git clone https://github.com/synthetichealth/synthea-international
cd synthea-international
cp -R jp/* ../synthea
cd ../synthea
./run_synthea -p 5 Kantō Tokyo
```

## Places

| Synthea | Japan | Count | Example |
|---|---|---|---|
| state | region (chihō) | 8 | Kantō |
| county | prefecture | 47 | Kanagawa |
| city | municipality | 1,718 | Yokohama |

The eight regions are Hokkaidō, Tōhoku, Kantō, Chūbu, Kinki, Chūgoku, Shikoku and Kyūshū (Okinawa is in Kyūshū). Region names use macrons, so type `Kantō`, not `Kanto`.

- The 23 special wards of Tokyo are one city, `Tokyo`.
- Each of the 20 designated cities (for example Yokohama, Osaka, Sapporo) is one city. Their wards are not separate.
- Towns and villages keep their suffix: `-machi`, `-cho`, `-mura` or `-son` (for example `Hakone-machi`).
- When two municipalities in the same region have the same name, the prefecture is added, for example `Ikeda-cho (Gifu)`. If they are in the same prefecture, the district is added, for example `Esashi-cho (Hiyama)`.
- Futaba-machi (Fukushima) is left out, because it had no residents on census day in 2020.

All names are in the file `src/main/resources/geography/demographics.csv` (column `NAME`, region in `STNAME`).

## Data sources

| Data | Source | License |
|---|---|---|
| Population by municipality, 5-year age group and sex | 2020 Census, table 2-7, Statistics Bureau of Japan, via [e-Stat](https://www.e-stat.go.jp/stat-search/files?toukei=00200521&tstat=000001136464) | [Government of Japan Standard Terms of Use 2.0](https://www.e-stat.go.jp/terms-of-use) (compatible with CC BY 4.0) |
| Postal codes and municipality names in romaji | [Japan Post, KEN_ALL_ROME](https://www.post.japanpost.jp/service/search/zipcode/download/roman-zip.html) | Japan Post does not claim copyright on the postal code data and allows free redistribution ([terms](https://www.post.japanpost.jp/zipcode/dl/readme_ro.html)) |
| Latitude and longitude of postal codes | [GeoNames postal codes, JP.zip](https://download.geonames.org/export/zip/) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Household income (2023) | [Ministry of Health, Labour and Welfare, 2024 Comprehensive Survey of Living Conditions](https://www.mhlw.go.jp/toukei/saikin/hw/k-tyosa/k-tyosa24/index.html), figure 9 | [Public Data License 1.0](https://www.digital.go.jp/resources/open_data/public_data_license_v1.0) (compatible with CC BY 4.0) |
| Hospitals, clinics and hospital departments (June 2026) | [Ministry of Health, Labour and Welfare, medical facility open data](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryou/newpage_43373.html) | [Public Data License 1.0](https://www.digital.go.jp/resources/open_data/public_data_license_v1.0) (compatible with CC BY 4.0) |

The files were made by `scripts/jp/build_jp.py`, which downloads the sources and builds every file in this folder. The data has been changed from the originals by the contributors of this folder (selected columns, joined and converted to the Synthea format). The data files keep the licenses of their sources.

Postal codes come from Japan Post (120,621 codes; the 21 codes of Futaba-machi are left out). The coordinates come from GeoNames. 342 Japan Post codes are not in GeoNames. Most of them use the average position of the other codes in the same municipality. On four islands of Tokyo (Miyake, Mikurajima, Hachijo and Aogashima) no code is in GeoNames, so the average position of the medical facilities there is used.

## Providers

- `hospitals.csv`: 7,715 hospitals. `urgent_care_facilities.csv` is the same list, because Japan has no separate urgent care system.
- `primary_care_facilities.csv`: 80,154 clinics and the hospitals above.
- Names are in romaji when the source has one (about 98% of hospitals and 91% of clinics). The rest use the Japanese name. Romaji names are written as in the source, so some are in lower case without spaces. Addresses are in Japanese.
- A hospital is marked `emergency = true` when one of its departments has 救急 (emergency) in its name (903 hospitals). Many more hospitals take emergency patients in reality.
- 5,233 facilities have no coordinates in the source (268 hospitals). They are placed at the centre of their municipality.
- `bed_count` is the total number of beds, as in the source. For about 100 hospitals it is empty or lower than 20. The original MHLW ID is in `mhlw_id`.

## Payer

There is one payer, "Japan Public Health Insurance". Everyone is eligible and there is no premium. The share paid by the patient depends on age:

| Age | Patient pays |
|---|---|
| Under 6 (in Japan: until starting primary school) | 20% |
| 6 to 69 | 30% |
| 70 to 74 | 20% |
| 75 and over | 10% |

The yearly amount a patient pays is capped at 3,600 US dollars (Synthea costs are in dollars). This stands for the high-cost medical expense benefit. In Japan the cap is set per month and depends on income. For a middle-income patient (about 3.7 to 7.7 million yen a year) it is 85,800 yen plus 1% of costs over a limit, and 44,400 yen from the fourth high-cost month in 12 months. Since August 2026 there is also a yearly cap of 530,000 yen for this group. 3,600 dollars is about 530,000 yen at 150 yen to the dollar.

Synthea checks the cap before each claim. The claim that passes the cap is still shared as usual, so some patients pay more than 3,600 dollars in a year. The year runs from one birthday to the next. A new age group starts in the first week after the birthday.

## Limitations

This is not an accurate model of the Japanese health system.

- Japan has many insurers (employee health insurance, National Health Insurance, the late-stage elderly system). Here they are one payer.
- Older people with higher income pay 20% or 30% in Japan. Here the rate depends on age only. The monthly cap depends on income in Japan. Here it is one yearly amount.
- Costs are the Synthea defaults, in US dollars. Japanese fees are not used.
- Person names are the Synthea defaults (US names). I have not found a list of Japanese names with a clear license.
- Race is set to Asian for everyone. Synthea chooses the first language from race using US data. As a result, about one quarter to one third of patients (24% and 34% in two test runs) get Chinese, Korean, Vietnamese or Hindi as their first language and a birthplace outside Japan, and most of the others get English.
- Income is household income from the 2024 Comprehensive Survey of Living Conditions, converted at 150 yen to the dollar. The survey gives steps of 1 million yen. Each step is spread evenly over the Synthea income bands, and the top step (20 million yen and over) is split into three equal parts by assumption. The same values are used for every municipality.
- Education, food insecurity, housing cost burden and vehicle access are not built from Japanese data. They use the same values as the European folders. Unemployment is 2.8% (2020, Labour Force Survey). Uninsured is 0%.
- Synthea moves a person to "no insurance" when their health costs in a year are higher than their income. This is not a rule of the Japanese system, but it still happens here: in a test with 382 patients (`-s 42 -p 300 Kantō`), 39 had at least one encounter without insurance, and 3.5% of encounters were not covered. With the income values of the European folders, the same test gave 70 of 391 patients and 4.7%.
- Phone numbers are not set.

## Rebuilding

```
pip install openpyxl
python3 scripts/jp/build_jp.py
```

The downloads are kept in `scripts/jp/.cache`.
