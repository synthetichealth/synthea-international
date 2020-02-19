import pandas as pd
import pyproj

# convert from Finnish map epsg:3067 to lat, lon
def xy_to_latlon(x, y, dst='epsg:4326'):
    # in:  x,y (ETRS-TM35FIN)
    # out: lat,lon (dd.ddd, WGS84 default)
    #      (might also be lon,lat...)
    proj_latlon = pyproj.Proj(init=dst) # default: WGS84
    proj_etrs = pyproj.Proj(init='epsg:3067') # ETRS-TM35FIN
    return pyproj.transform(proj_etrs, proj_latlon, x, y)

# load the posti key file into a dataframe
keydf = pd.read_csv('../data/alueryhmittely_posnro_2020_en.csv', dtype='object')
keydf = keydf.rename(columns={'Postal code area': 'zipcode'})
keydf['zipcode'] = keydf['zipcode'].astype(str)

# load the preprocessed lat and lon data
latlondf = pd.read_csv('../data/paavo_geospacial_by_city_processed.csv', dtype='object')

# load the paavo geospacial data into a dataframe
# not sure why they put 3 columns into one column but convert it back now
geodf = pd.read_csv('../data/paavo_geospacial_by_city.csv', dtype='object') 
geodf = geodf.fillna(0)
geodf['zipcode'], geodf['city_muni'] = geodf['Postal code area'].str.split(' ', 1).str
geodf = geodf.drop(['Postal code area'], axis=1)
geodf['city'], geodf['muni'] = geodf['city_muni'].str.split(' \(', 1).str
geodf['muni'] = geodf['muni'].str.replace(')', '')
geodf = geodf.drop(['city_muni'], axis=1)
geodf['zipcode'] = geodf['zipcode'].astype(str)
geodf = geodf.rename(columns={'X coordinate in metres': 'ycoordinate'})
geodf = geodf.rename(columns={'Y coordinate in metres': 'xcoordinate'})

# load the region name to iso code mapping file
regiondf = pd.read_csv('../data/region_iso_code.csv', dtype='object')

# convert x and y in meters to lat lon

# do an innner join based on city name
df = pd.merge(keydf,geodf, on='zipcode', how='inner')

# do an left join to fill region name
df = pd.merge(df.astype(str),regiondf.astype(str), on='Name of the region', how='left')

# join the pre processed lat and lon coordinates by row
df = pd.merge(df, latlondf, left_index=True, right_index=True)


# create output columns
df['USPS'] = df['Name of the region']
df['ST'] = df['Region iso code']
df['NAME'] = df['muni']
df['ZCTA5'] = df['zipcode']
df['LAT'] = df['lat']
df['LON'] = df['lon']

# write the new dataframe to the demographics file
header = ['USPS','ST','NAME','ZCTA5','LAT','LON']
df.to_csv('../src/main/resources/geography/zipcodes.csv', columns = header)
