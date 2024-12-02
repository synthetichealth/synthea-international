require 'csv'
require 'terminal-table'
require 'pry'

NATIONS = [
  'at','be','bg','ca','cz','de','dk','ee','es','fi','fr','gb','hr','hu','ie','it','nl','no','nz','pl','pt','ro','se','si','sk'
]

NATIONS.each do |nation|
  sdoh_filename = "../#{nation}/src/main/resources/geography/sdoh.csv"
  if File.file?(sdoh_filename)
    File.delete(sdoh_filename)
  end
end

NATIONS.each do |nation|
  puts "Checking for SDOH files for #{nation}..."

  sdoh_filename = "../#{nation}/src/main/resources/geography/sdoh.csv"
  if !File.file?(sdoh_filename)
    puts '  * sdoh.csv file not found, checking demographics.csv...'
    demographics_filename = "../#{nation}/src/main/resources/geography/demographics.csv"
    if File.file?(demographics_filename)
      locations = []
      CSV.foreach(demographics_filename, headers: true, col_sep: ',') do |row|
        #ID,COUNTY,NAME,STNAME,POPESTIMATE2015,CTYNAME,TOT_POP,TOT_MALE,TOT_FEMALE,WHITE,HISPANIC,BLACK,ASIAN,NATIVE,OTHER,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,00..10,10..15,15..25,25..35,35..50,50..75,75..100,100..150,150..200,200..999,LESS_THAN_HS,HS_DEGREE,SOME_COLLEGE,BS_DEGREE
        county = row['CTYNAME']
        state = row['STNAME']
        locations << [ county, state ]
      end
      locations.uniq!
      locations.sort! {|a,b| a.last <=> b.last && a.first <=> b.first}

      abbreviations = {}
      zipcodes_filename = "../#{nation}/src/main/resources/geography/zipcodes.csv"
      if File.file?(zipcodes_filename)
        CSV.foreach(zipcodes_filename, headers: true, col_sep: ',') do |row|
          #,USPS,ST,NAME,ZCTA5,LAT,LON
          state = row['USPS']
          abbreviation = row['ST']
          abbreviations[state] = abbreviation
        end
      end

      file = File.open(sdoh_filename, 'w:UTF-8')
      file.write("FIPS_CODE,COUNTY_CODE,COUNTY,ST,STATE,FOOD_INSECURITY,SEVERE_HOUSING_COST_BURDEN,UNEMPLOYED,NO_VEHICLE_ACCESS,UNINSURED\n")
      fips = 0
      county_code = 0
      locations.each do |location|
        state = location.last
        abbv = abbreviations[state]
        file.write("#{fips},#{county_code},#{location.first},#{abbv},#{state},0.15,0.15,0.1,0.15,0.1\n")
        fips += 1
        county_code += 1
      end
      puts '  + generated sdoh.csv from demographics.csv.'
    else
      puts '  * demographics.csv file not found!'
    end
  end
end