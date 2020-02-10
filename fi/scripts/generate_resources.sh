#!/bin/bash

# Read in data from paavo generated file and write geogroaphy demographics file
python generate_demographics.py

# generate the zip code file as combination of posti key file and paavo geospacial data
python geneate_zipcodes.py
