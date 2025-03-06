require 'csv'
require 'terminal-table'
require 'pry'

NATIONS = [
  'at','be','bg','ca','cz','de','dk','ee','es','fi','fr','gb','hr','hu','ie','it','nl','no','nz','pl','pt','ro','se','si','sk'
]

SYNTHEA_DIR = '../../synthea'

def reset_test_results
  `rm -R test_results`
  `mkdir test_results`
end

def run_tests
  NATIONS.each do |nation|
    puts "Running #{nation}..."

    logfile = "../synthea-international/scripts/test_results/#{nation}.txt"

    Dir.chdir(SYNTHEA_DIR) {
      # restoring default settings
      `touch #{logfile}`
      `rm -R src/main/resources &> #{logfile}`
      `git restore src/main/resources &> #{logfile}`
      `git restore src/test &> #{logfile}`      
      `git restore README.md &> #{logfile}`
      `rm -R data &> #{logfile}`
      `rm -R scripts &> #{logfile}` 
      `rm -R test &> #{logfile}`
      # apply new settings
      `cp -R ../synthea-international/#{nation}/* . &> #{logfile}`
    }

    provinces = []
    filename = "../#{nation}/src/main/resources/geography/timezones.csv"

    if File.file?(filename)
      CSV.foreach(filename, headers: true, col_sep: ',') do |row|
        provinces << row[0]
      end
    else
      puts '  * timezones.csv file not found!'
    end
    provinces.uniq!

    provinces.each do |province|
      puts "  - #{nation}, #{province}..."
      province_filesafe = province.gsub('(','_').gsub(')','_').gsub(' ','_').gsub('\'','_')
      Dir.chdir(SYNTHEA_DIR) {
        `touch ../synthea-international/scripts/test_results/#{nation}_#{province_filesafe}.txt`
        `./run_synthea --generate.providers.default_to_hospital_on_failure=true -p 10 \"#{province}\" &> ../synthea-international/scripts/test_results/#{nation}_#{province_filesafe}.txt`
      }
    end
  end
end

def read_test_results
  results = `grep -A1 "Exception" ./test_results/*`
  results = results.split("--\n").map {|a| a.split("\n")}
  # results is now an array, one entry per test result file.
  # each entry is an array, with one pair of lines per Exception.
  # for each pair, line 0 is the exception, after the string `.txt:`
  #                line 1 is the first line of the stack trace, after the string `.txt-\t`
  results_table = results.map do |a|
    n = a.first.gsub('./test_results/','').split('_').first
    s = a.first.gsub("./test_results/#{n}_",'').split('.txt:').first
    e = a.first.split('.txt:').last
    w = a.last.split("\t").last
    # [nation, state, exception, where]
    [n, s, e, w]
  end  
  results_table.uniq!
  results_table
end

# --------------------------------------------------------------------

reset_test_results
run_tests
results_table = read_test_results

# nations with most errors
table = Terminal::Table.new :headings => ['Nation','Errors'], :rows => results_table.map{|a| a[0]}.tally.sort {|a,b| b.last <=> a.last}
puts table

# provinces with most errors
# results_table.map{|a| a[1]}.tally.sort {|a,b| b.last <=> a.last}

# most frequent exception type
table = Terminal::Table.new :headings => ['Exception','Count'], :rows => results_table.map{|a| a[2]}.tally.sort {|a,b| b.last <=> a.last}
puts table

# most frequent cause
table = Terminal::Table.new :headings => ['Issue','Count'], :rows => results_table.map{|a| a[3]}.tally.sort {|a,b| b.last <=> a.last}
puts table

#binding.pry

puts 'Done.'