# synthea-international

[Synthea<sup>TM</sup>](https://github.com/synthetichealth/synthea) is an open-source Synthetic Patient Population Simulator.

Synthea defaults to generating populations inside the United States of America, but it can be configured for [Other Areas](https://github.com/synthetichealth/synthea/wiki/Other-Areas).

This repository contains metadata and configuration files for international locations.

Each folder within this repository contains files for one nation or area. To configure Synthea for one of these locations, simply copy the contents of a folder into the Synthea repository. For example:

```
cp -R example/ ../synthea
```

# EU

EU data is taken from the following sources:

geonames.org - postal code data is taken from https://download.geonames.org/export/zip/
    License:  Creative Commons Attribution 3.0 License

openstreetmap.com - health site data is extracted from open street maps.
    License: Open Database License
    “© OpenStreetMap contributors”.  https://www.openstreetmap.org/copyright

Azure pipelines to generate data:
    https://github.com/science-automation/genSyntheaEU
    https://dev.azure.com/shambergerm/SyntheaInternational/_build

Notes:
Demographic data is fake.  Looking for good source of demographics data.  EU census data is a possibility
Cost data is still default us
Only a single payer per country as the National Health Insurance.   Needs more work

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
