#!/bin/bash
# This script generates 10 sample patients for each province within each international location
# then checks for errors.

rm -R test_results
mkdir test_results

for nation in at be bg ca cz de dk ee es fi fr gb hr hu ie it nl no nz pl pt ro se si sk
do
  # ${nation}
  echo "Running ${nation}..."
  cp -R ../${nation}/* ../../synthea

  provinces=()
  # declare -a provinces
  {
    read # discard headers
    while IFS=, read -a -d=\n a b c d
    do
      provinces+=(${a})
    done
  } < ../${nation}/src/main/resources/geography/timezones.csv

  echo ${provinces}

  for province in ${provinces}
  do
    echo "  - ${nation}, ${province}..."
    ../../synthea/run_synthea -p 10 ${province} &> ./test_results/${nation}_${province}.txt
  done

done

echo "Done."