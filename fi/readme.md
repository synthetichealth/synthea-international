# Country oF Finland

This folder contains the configuration files for the country of Finland.  The initial implementation includes the hospital district Uusimaa that includes Helsinki and the surrounding region. 

# Finland Helath System Overview
Healthcare in Finland consists of a highly decentralized three-level publicly funded healthcare system and a much smaller private sector.
(ref https://en.wikipedia.org/wiki/Healthcare_in_Finland)

Public healthcare is available to all permanent residents in Finland regardless of their financial situation. Primary health care services are provided by municipal health centres (terveysasemat), and specialised medical care is provided by district hospitals (sairaalat).
(ref https://www.expat-finland.com/living_in_finland/public_healthcare.html)

# Using Synthea to Model Finnish Healthcare

# Healthcare Regions
There are 20 healthcare regions in Finland.  Each healthcare region is modeled as an entry in the insurance_companies.csv resource file.  The heathcare region provides all services for the particular region (state) and no other region (state).

# state names
Finland has regions and not states like in USA.  Whenever the state abbreviations is used such as MA or NY, the 2 digits ISO code for the Finnish region is used.  It is done in this way since there is a further conversion to OMOP format that allows only 2 digits for the state field.

Finland iso codes for region can be seen here:  https://en.wikipedia.org/wiki/ISO_3166-2:FI

To do:
Update the primary_care_facilities.csv for each hospital's specialities.
Add other Finnish regions

Usage:

1) Overlay this folder on top of the resources folder.  You may need to merge the sythea.properties file with your own.

2) Compile the code

3) Examples for running synthea
./run_synthea "Uusimaa"
./run_synthea "Uusimaa" Helsinki
./run_synthea "Uusimaa" Espoo
./run_synthea "Uusimaa" Vantaa

