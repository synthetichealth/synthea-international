require 'csv'
require 'terminal-table'
require 'pry'

NATIONS = [
  'at','be','bg','ca','cz','de','dk','ee','es','fi','fr','gb','hr','hu','ie','it','nl','no','nz','pl','pt','ro','se','si','sk'
]

def distance(coords_a, coords_b)
  dx = (coords_a[0] - coords_b[0]).abs
  dy = (coords_a[1] - coords_b[1]).abs
  Math.hypot(dx,dy)
end

results = []

NATIONS.each do |nation|
  puts "Checking Hospitals for #{nation}..."

  locations = {}
  filename = "../#{nation}/src/main/resources/geography/zipcodes.csv"
  if File.file?(filename)
    CSV.foreach(filename, headers: true, col_sep: ',') do |row|
      state = row['USPS']
      locations[state] = [] unless locations[state]
      locations[state] << [ row['LAT'].to_f, row['LON'].to_f, row['NAME'] ]
    end
    locations.each do |state, coord_list|
      coord_list.uniq!
    end
  else
    puts '  * zipcodes.csv file not found!'
  end

  hospitals = {}
  filename = "../#{nation}/src/main/resources/providers/hospitals.csv"
  if File.file?(filename)
    CSV.foreach(filename, headers: true, col_sep: ',') do |row|
      state = row['state']
      hospitals[state] = [] unless hospitals[state]
      hospitals[state] << [ row['LAT'].to_f, row['LON'].to_f ]
    end
    hospitals.each do |state, coord_list|
      coord_list.uniq!
    end
  else
    puts '  * hospitals.csv file not found!'
  end

  required_distance = 0
  locations.each do |state, state_coords|
    state_coords.each do |location|
      location_distances = []
      location_count = 0
      if hospitals[state]
        hospitals[state].each do | hospital_coords |
          distance = distance(location, hospital_coords)
          location_distances << distance
        end
        location_count = location_distances.length
      else
        location_count = 0
      end
      if !location_distances.empty?
        loc_min = location_distances.min
        loc_max = location_distances.max
        if (loc_min > 32)
          results << [nation, state, location.last, location_count, location_distances.min, location_distances.max]
        end
      else
        results << [nation, state, location.last, location_count, Float::INFINITY, Float::INFINITY]
      end
    end
  end
end

# table = Terminal::Table.new :headings => ['Nation','State','City','Minimum Distance (degrees)','Maximum Distance (degrees)'], :rows => results
# puts table

results_state = []
states_and_cities = results.map {|r| [r[0],r[1],r[2]]}.uniq!
states_and_cities.each do | state_and_city |
  subset = results.select {|r| r[0] == state_and_city[0] && r[1] == state_and_city[1]}
  min_col = subset.map {|r| r[4]}
  max_col = subset.map {|r| r[5]}
  # results_state << [ state_and_city[0], state_and_city[1], state_and_city[2], min_col.max, max_col.max ]
  results_state << [ state_and_city[0], state_and_city[1], min_col.max, max_col.max ]
end
results_state.uniq!
table = Terminal::Table.new :headings => ['Nation','State','Minimum Distance (degrees)','Maximum Distance (degrees)'], :rows => results_state
puts table


# find the centroid of the nation / state
results_state.each do |row|
  # [nation, state, min distance, max distance]
  nation = row[0]
  state = row[1]

  puts "Calculating centroid for #{nation}, #{state}..."

  zlat = []
  zlon = []
  filename = "../#{nation}/src/main/resources/geography/zipcodes.csv"
  if File.file?(filename)
    CSV.foreach(filename, headers: true, col_sep: ',') do |zrow|
      zstate = zrow['USPS']
      if zstate == state
        zlat << zrow['LAT'].to_f
        zlon << zrow['LON'].to_f
      end
    end
  else
    puts '  * zipcodes.csv file not found!'
  end

  slat = zlat.sum.to_f / zlat.length.to_f
  slon = zlon.sum.to_f / zlon.length.to_f

  # find the nearest hospital in the nation to each centroid
  # copy that hospital, but put it in the "new" state
  best_dx = Float::INFINITY
  best_hospital = nil
  row_num = 0
  row_id = 0
  filename = "../#{nation}/src/main/resources/providers/hospitals.csv"
  if File.file?(filename)
    CSV.foreach(filename, headers: true, col_sep: ',') do |hrow|
      hlat = hrow['LAT'].to_f
      hlon = hrow['LON'].to_f
      dx = distance([slat, slon], [hlat, hlon])
      if best_hospital.nil? || (dx < best_dx)
        best_hospital = hrow
        best_dx = dx
      end
      row_num = hrow[0].to_i if (hrow[0].to_i) > row_num
      row_id = hrow[1].to_i if (hrow[1].to_i) > row_id
    end
  else
    puts '  * hospitals.csv file not found!'
  end
  row << best_dx
  best_hospital[0] = (row_num + 1)
  best_hospital[1] = (row_id + 1)
  best_hospital['state'] = state
  row << best_hospital
end

patched_nations = results_state.map {|r| r[0]}.uniq
patched_nations.each do |nation|
  file = File.open("../#{nation}/src/main/resources/providers/hospitals.csv", 'a:UTF-8')
  patched_results = results_state.select {|r| r[0] == nation}
  row_num = patched_results[0].last[0].to_i
  row_id = patched_results[0].last[1].to_i
  patched_results.each do |row|
    row.last[0] = row_num
    row.last[1] = row_id
    row.last['state'] = row[1]
    file.write(row.last.to_s)
    row_num += 1
    row_id += 1
  end
  file.close
end






