# -*- coding: utf-8 -*-
from collections import OrderedDict
import pandas as pd
import os
import zipfile
from dotenv import load_dotenv
import ModelSyntheaPandas
import ModelData
import unicodedata
import sys

if len(sys.argv) <2:
    print("BASEDIR should be set")
    sys.exit()
basedir = sys.argv[1]

# ------------------------
# load env
# ------------------------
load_dotenv(verbose=True)

# set output directory
# Path to the directory containing the city data
BASE_INPUT_DIRECTORY    = os.environ['BASE_INPUT_DIRECTORY']

# load synthea model
model_synthea = ModelSyntheaPandas.ModelSyntheaPandas()

# list of countries to be processed.
countries= ["BE", "BG", "CY", "CZ", "DK", "DE", "EE", "GR", "IE", "ES", "FR", "HR", "IT", "LV", "LT", "LU", "HU", "MT", "NL", "AT", "PL", "PT", "RO", "SI", "SK", "SE", "NO", "GB"]

# output file in utf-8
columns = ['country','region','demographics','zipcodes','hospitals','urgent','primary']
temp = OrderedDict([('country', 'Init'),('region', 'Init'),('demographics', True),('zipcodes', True),('hospitals', True),('urgent', True),('primary', True)])
outdf = pd.DataFrame(temp, columns=columns, index=[0])

for country in countries:
    zonefile = BASE_INPUT_DIRECTORY + "/" + country.lower() + "/src/main/resources/geography/timezones.csv"
    df = pd.read_csv(zonefile, encoding ='utf-8')
    regions = df.STATE.unique()
    for region in regions:
        # Region should be in the following files for it to have a chnace of working
        # check demographics file
        demographics = BASE_INPUT_DIRECTORY + "/" + country.lower() + "/src/main/resources/geography/demographics.csv"
        if (os.path.exists(demographics)):
            demographicsdf = pd.read_csv(demographics, dtype=model_synthea.model_schema['demographics'], encoding ='utf-8')
            state = 'STNAME'
            demographicsdf = demographicsdf[demographicsdf[state].str.contains(region, na=False)] 
            if len(demographicsdf) > 0:
                demographics_valid = True
            else:
                demographics_valid = False
        # check zipcodes
        zipcodes = BASE_INPUT_DIRECTORY + "/" + country.lower() + "/src/main/resources/geography/zipcodes.csv"
        if (os.path.exists(zipcodes)):
            zipcodesdf = pd.read_csv(zipcodes, dtype=model_synthea.model_schema['zipcodes'], encoding ='utf-8')
            state = 'USPS'
            zipcodesdf = zipcodesdf[zipcodesdf[state].str.contains(region, na=False)]
            if len(zipcodesdf) > 0:
                zipcodes_valid = True
            else:
                zipcodes_valid = False
        else:
            zipcodes_valid = False
        # check providers hospitals
        hospitals = BASE_INPUT_DIRECTORY + "/" + country.lower() + "/src/main/resources/providers/hospitals.csv"
        if (os.path.exists(hospitals)):
            hospitalsdf = pd.read_csv(hospitals, dtype=model_synthea.model_schema['hospitals'], encoding ='utf-8')
            state = 'state'
            hospitalsdf = hospitalsdf[hospitalsdf[state].str.contains(region, na=False)]
            if len(hospitalsdf) > 0:
                hospitals_valid = True
            else:
                hospitals_valid = False
        else:
            hospitals_valid = False
        # check providers urgent care
        urgent = BASE_INPUT_DIRECTORY + "/" + country.lower() + "/src/main/resources/providers/urgent_care_facilities.csv"
        if (os.path.exists(urgent)):
            urgentdf = pd.read_csv(urgent, dtype=model_synthea.model_schema['hospitals'], encoding ='utf-8')
            state = 'state'
            urgentdf = urgentdf[urgentdf[state].str.contains(region, na=False)]
            if len(urgentdf) > 0:
                urgent_valid = True
            else:
                urgent_valid = False
        else:
            urgent_valid = False
        # check providers primary care
        primary = BASE_INPUT_DIRECTORY + "/" + country.lower() + "/src/main/resources/providers/primary_care_facilities.csv"
        if (os.path.exists(primary)):
            primarydf = pd.read_csv(primary, dtype=model_synthea.model_schema['primary_care_facilities'], encoding ='utf-8')
            state = 'state'
            primarydf = primarydf[primarydf[state].str.contains(region, na=False)]
            if len(primarydf) > 0:
                primary_valid = True
            else:
                primary_valid = False
        else:
            primary_valid = False
        
        temp = OrderedDict([('country', country),('region', region),('demographics', demographics_valid),('zipcodes', zipcodes_valid),('hospitals', hospitals_valid),('urgent', urgent_valid),('primary', primary_valid)])
        outdf2 = pd.DataFrame(temp, columns=columns, index=[0])
        outdf = outdf.append(outdf2)
outdf.to_csv('results.txt', encoding='utf-8')
