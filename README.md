# synthea-international

[Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) is an open-source Synthetic Patient Population Simulator.

Synthea defaults to generating populations inside the United States of America, but it can be configured for [Other Areas](https://github.com/synthetichealth/synthea/wiki/Other-Areas).

This repository contains metadata and configuration files for international locations.

Each folder within this repository contains files for one nation or area. To configure Synthea for one of these locations, simply copy the contents of a folder into the Synthea repository. For example:

```
cp -R example/* ../synthea

```

Here are the specific steps needed to generate patients for Great Britain county of Suffolk city Bristol

```
git clone https://github.com/synthetichealth/synthea
git clone https://github.com/synthetichealth/synthea-international
cd synthea-international
cp -R gb/* ../synthea
cd ../synthea
./run_synthea -p 5 Somerset Bristol
```

# Data sources

Providers - Extracted from OpenStreetMaps

Zip codes, city names and populations - geonames.org

Demographic data - Finland demographics are copied to all European countries. 

# International region status

Most regions of the countries provided in this repository are working but some are not.  

This is a [report](./status.txt) of the current status.  A region needs all "True" entries to function.  This can be due to lack of mappers in OpenStreetMaps where providers are extracted from.  There are also issues with the zip code files that have mostly English names that don't match up with local naming.  

After some research, OpenStreetMaps and geonames.org was determined to be the best source of open data.  If there is one open source set of zip codes, cities and providers across Europe let us know and we can build that into the pipeline.

Other Issues:

- phone numbers are in US format still.
- Names are based on USA common names except for Finland.

# License

Copyright 2020 - 2021 The MITRE Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
