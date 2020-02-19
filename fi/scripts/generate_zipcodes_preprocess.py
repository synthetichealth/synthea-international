import csv
import pyproj

# convert from Finnish map epsg:3067 to lat, lon
def xy_to_latlon(x, y, dst='epsg:4326'):
    # in:  x,y (ETRS-TM35FIN)
    # out: lon,lat (dd.ddd, WGS84 default)
    proj_latlon = pyproj.Proj(init=dst) # default: WGS84
    proj_etrs = pyproj.Proj(init='epsg:3067') # ETRS-TM35FIN
    return pyproj.transform(proj_etrs, proj_latlon, x, y)

# preprocess the geospacial file to convert epsg:3067 coordinates to epsg:4326
# wasn't working properly as a pandas dataframe function
results = []
with open("../data/paavo_geospacial_by_city.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        results.append(row)
        
with open("../data/paavo_geospacial_by_city_processed.csv", "w") as csvfile:
    fieldnames = ['lat','lon']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        x=float(row['X coordinate in metres'])
        y=float(row['Y coordinate in metres'])
        (lon, lat) = xy_to_latlon([x], [y])
        temp = {}
        temp['lat'] = lat[0]
        temp['lon'] = lon[0]
        writer.writerow(temp)
