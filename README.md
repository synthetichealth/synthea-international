# synthea-international

[Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) is an open-source Synthetic Patient Population Simulator.

Synthea defaults to generating populations inside the United States of America, but it can be configured for [Other Areas](https://github.com/synthetichealth/synthea/wiki/Other-Areas).

This repository contains metadata and configuration files for international locations.

Each folder within this repository contains files for one nation or area. To configure Synthea for one of these locations, simply copy the contents of a folder into the Synthea repository. For example:

```
cp -R example/* ../synthea

```

Here are the specific steps need to generate patients for Great Britain county of Suffolk city Bristol

```
git clone https://github.com/synthetichealth/synthea
git clone https://github.com/synthetichealth/synthea-international
cd synthea-international
cp -R gb/* ../synthea
cd ../synthea
./run_synthea -p 5 Somerset Bristol
```


# International region status

Most regions of the countries provided in this repository are working but some are not.  

This can be due to lack of provider data from a particular region.

This is a [report](./status.txt) of the current status.

- Demographic data is not accurate.  We don't have demographics data for each european country.  All European countries get a copy of Finland's demographics where we have data
- zip codes/lat/lon and city data is accurate.
- health care providers are extracted from open street maps.
- phone numbers are in US format still.

# License

Copyright 2020 The MITRE Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
