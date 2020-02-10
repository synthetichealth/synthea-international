import pandas as pd
R = 0

# load the posti key file into a dataframe
keydf = pd.read_csv('../data/alueryhmittely_posnro_2020_en.csv', dtype='object')
keydf = keydf.rename(columns={'Postal code area': 'zipcode'})
#keydf = keydf.fillna(0)
keydf['zipcode'] = keydf['zipcode'].astype(str)
print("keydf")
print(len(keydf))
print(keydf.columns.tolist())

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
print("geodf")
print(len(geodf))
print(geodf.columns.tolist())

# convert meters to lat lon
# not so easy?  Need to investigate more

# do an innner join based on city name
df = pd.merge(keydf,geodf, on='zipcode', how='inner')
print(len(df))
print(df.columns.tolist())

# create output columns
df['USPS'] = df['Name of the region']
df['ST'] = df['Region']
df['NAME'] = df['muni']
df['ZCTA5'] = df['zipcode']
df['LAT'] = df['X coordinate in metres']
df['LON'] = df['Y coordinate in metres']

# write the new dataframe to the demographics file
header = ['USPS','ST','NAME','ZCTA5','LAT','LON']
df.to_csv('zipcode.csv', columns = header)
