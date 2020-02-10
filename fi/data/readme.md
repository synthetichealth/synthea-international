# Data #

These comma delimited csv files in utf-8 format are used to generate the following files:
- geograhpy/zipcodes.csv
- geography/demographics.csv

# Generating Demographic data #

This is data generated from Paavo - Open data by postal code area

Ubuntu for Windows 10 was used to run the python scripts

Instructions to generate:

1) Go to 
http://pxnet2.stat.fi/PXWeb/pxweb/en/Postinumeroalueittainen_avoin_tieto/
2) Select the latest year "Data Published in 2020" and then "All data groups"
3) Select all of the information and all the zip codes in postal code area. 
4) Next to the continue button, select csv file and then continue
5) Remove the top 2 lines of the generated file
Save the file create to this directory as paavo.csv
The file is a windows encoding.  Convert it to utf-8
iconv -f iso-8859-1 -t utf-8 paavo.csv -o paavo.csv.utf8

# Download the Paavo Posti key file #

https://www.stat.fi/static/media/uploads/tup/paavo/alueryhmittely_posnro_2020_en.xlsx

Use excel to save as a csv comma delimited utf-8 format

# Region mapping to ISO code #

The 2 digit ISO code for a countries region is used instead of a 2 digit state abbreviation.

This file was created by hand based on ISO data.
