import pandas as pd
R = 0

# load the posti key file into a dataframe
keydf = pd.read_csv('../data/alueryhmittely_posnro_2020_en.csv')
keydf = keydf.rename(columns={'Postal code area': 'zipcode'})
keydf = keydf.fillna(0)
keydf = keydf['zipcode'].astype(str)
print(len(keydf))

# load the paavo geospacial data into a dataframe
# not sure why they put 3 columns into one column but convert it back now
geodf = pd.read_csv('../data/paavo_geospacial_by_city.csv') 
geodf = geodf.fillna(0)
geodf['zipcode'], geodf['city_muni'] = geodf['Postal code area'].str.split(' ', 1).str
geodf = geodf.drop(['Postal code area'], axis=1)
geodf['city'], geodf['muni'] = geodf['city_muni'].str.split(' \(', 1).str
geodf['muni'] = geodf['muni'].str.replace(')', '')
geodf = geodf.drop(['city_muni'], axis=1)
geodf = geodf['zipcode'].astype(str)
print(len(geodf))

# convert meters to lat lon
# not so easy?  Need to investigate more

# do an innner join based on city name
df = pd.merge(keydf,geodf, on='zipcode', how='inner')
print(df.count())
print(df)
