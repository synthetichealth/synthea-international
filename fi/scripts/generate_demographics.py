import pandas as pd

# load the paavo csv into a dataframe
df = pd.read_csv('../data/paavo_municipality_demographics.csv', dtype=object) 
df = df.fillna("")
df = df.rename(columns={'Inhabitants, total, 2018 (HE)': 'poptotal'})  # make shorter column name

# load the posti key file so we can match municipality with region
keydf = pd.read_csv('../data/alueryhmittely_posnro_2020_en.csv', dtype=object)
keydf = keydf.rename(columns={'Name of the municipality': 'NAME'})
# get rid of columns we are not using and drop duplicates
keydf = keydf[['Name of the region','NAME']]
keydf = keydf.drop_duplicates(subset=['Name of the region','NAME'])

# create new dataframe columns with the data in synthea demographics format
df.loc[:,'COUNTY'] = ""
df["NAME"] = df["Area"]
df = pd.merge(df.astype(str),keydf.astype(str), on='NAME', how='left')
df["poptotal"] = df["poptotal"].astype(int)
df["STNAME"] = df["Name of the region"]
df["POPESTIMATE2015"] = df["poptotal"]
df["CTYNAME"] = df["Area"]
df["TOT_MALE"] = df["Males, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["TOT_FEMALE"] = df["Females, 2018 (HE)"].astype(int).divide(df["poptotal"])
df.loc[:,'WHITE'] = 1.0
df.loc[:,'HISPANIC'] = 0.0
df.loc[:,'BLACK'] = 0.0
df.loc[:,'ASIAN'] = 0.0
df.loc[:,'NATIVE'] = 0.0
df.loc[:,'OTHER'] = 0.0
df["1"] = (df["0-2 years, 2018 (HE)"]+df["3-6 years, 2018 (HE)"]).astype(int).divide(df["poptotal"])  # should be 0-4 but data does not fit
df["2"] = df["7-12 years, 2018 (HE)"].astype(int).divide(df["poptotal"]) # should be 5-9 but data does not fit
df["3"] = df["13-15 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["4"] = (df["16-17 years, 2018 (HE)"]+df["18-19 years, 2018 (HE)"]).astype(int).divide(df["poptotal"])
df["5"] = df["20-24 years, 2018 (HE)"].astype(int).divide(df["poptotal"])  # good matching data from here
df["6"] = df["25-29 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["7"] = df["30-34 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["8"] = df["35-39 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["9"] = df["40-44 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["10"] = df["45-49 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["11"] = df["50-54 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["12"] = df["55-59 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["13"] = df["60-64 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["14"] = df["65-69 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["15"] = df["70-74 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["16"] = df["75-79 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["17"] = df["80-84 years, 2018 (HE)"].astype(int).divide(df["poptotal"])
df["18"] = df["85 years or over, 2018 (HE)"].astype(int).divide(df["poptotal"])
df.loc[:,'00..10'] = .19
df.loc[:,'10..15'] = .1145
df.loc[:,'15..25'] = .3
df.loc[:,'25..35'] = .2
df.loc[:,'35..50'] = .1465
df.loc[:,'50..75'] = .03
df.loc[:,'100..150'] = .012
df.loc[:,'150..200'] = .005
df.loc[:,'200..999'] = .001
df['HS_DEGREE'] = df['Matriculation examination, 2018 (KO)'].astype(int).divide(df["poptotal"])
df['SOME_COLLEGE'] = df['Vocational diploma, 2018 (KO)'].astype(int).divide(df["poptotal"])
df['BS_DEGREE'] = (df['Academic degree - Lower level university degree, 2018 (KO)'].astype(int) + df['Academic degree - Higher level university degree, 2018 (KO)'].astype(int)).divide(df["poptotal"])
df.loc[:,'LESS_THAN_HS'] = 1.0
df['LESS_THAN_HS'] = df['LESS_THAN_HS'] - df['SOME_COLLEGE'] - df['BS_DEGREE'] - df['HS_DEGREE']


# write the new dataframe to the demographics file
header = ["COUNTY","NAME","STNAME","POPESTIMATE2015","CTYNAME","TOT_POP","TOT_MALE","TOT_FEMALE","WHITE","HISPANIC","BLACK","ASIAN","NATIVE","OTHER","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","00..10","10..15","15..25","25..35","35..50","50..75","100..150","150..200","200..999","LESS_THAN_HS","HS_DEGREE","SOME_COLLEGE","BS_DEGREE"]
df.to_csv('output.csv', columns = header)
