# Country of Finland #

This folder contains the configuration files for the country of Finland.  The initial implementation includes the hospital district Uusimaa that includes Helsinki and the surrounding region that is administered by HUS. 

# Finland Health System Overview #

[Healthcare in Finland](https://en.wikipedia.org/wiki/Healthcare_in_Finland) consists of a highly decentralized three-level publicly funded healthcare system and a much smaller private sector.

[Public healthcare](https://www.expat-finland.com/living_in_finland/public_healthcare.html) is available to all permanent residents in Finland regardless of their financial situation. Primary health care services are provided by municipal health centres (terveysasemat), and specialised medical care is provided by district hospitals (sairaalat).

# Using Synthea to Model Finnish Healthcare #

## Healthcare Regions ##

There are 20 healthcare regions in Finland.  Each healthcare region is modeled as an entry in the insurance_companies.csv resource file.  The heathcare region provides all services for the particular region (state) and no other region (state).  This is mostly accurate except in the case of very specialized procedures such as heart surgury which is only performed in a single Helsinki hospital.

## Regions are mapped to states ##

Finland has regions and not states like in USA.  Whenever the state abbreviations is used such as MA or NY, the 2 digits ISO code for the Finnish region is used.  It is done in this way since there is a further conversion to OMOP format that allows only 2 digits for the state field.

Finland [iso codes for region](https://en.wikipedia.org/wiki/ISO_3166-2:FI)

# Generating the population #

Usage:

1) Overlay this folder on top of the resources folder.  You may need to merge the synthea.properties file with your own.

2) Compile the code

3) Examples for running synthea to generate a Finnish population
./run_synthea "Uusimaa"
./run_synthea "Uusimaa" Helsinki
./run_synthea "Uusimaa" Espoo
./run_synthea "Uusimaa" Vantaa
./run_synthea "Lapland"
./run_synthea "Lapland" Salla

# To do #

Update the primary_care_facilities.csv for each hospital's specialities.
the standard visit price of 20.60 is set but the other costs are not accurate
Add other Finnish regions

