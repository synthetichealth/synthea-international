#!/bin/bash

# Read in data from paavo generated file and write geogroaphy demographics file
python generate_demographics.py

# generate the zip code file as combination of posti key file and paavo geospacial data
python generate_zipcodes_preprocess.py
python generate_zipcodes.py
