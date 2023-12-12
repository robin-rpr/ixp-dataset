# IXP Data Integration

This repository contains Python scripts to fetch, merge, and analyze Internet Exchange Point (IXP) data from various sources, including PeeringDB, PCH, and Hurricane Electric.

## Scripts

1. **PeeringDB Script (`get_peeringdb_data.py`):**
   - Fetches data from PeeringDB API.
   - Outputs data to `data/peeringdb.json`.

2. **PCH Script (`get_pch_data.py`):**
   - Retrieves data from the PCH API.
   - Outputs data to `data/pch.json`.

3. **Hurricane Electric Script (`get_he_ixps.py`):**
   - Scrapes data from the [bgp.he.net](https://bgp.he.net) website.
   - Outputs data to `data/he.json`.

4. **Merge IXP Data Script (`merge_ixp_data.py`):**
   - Merges data from PeeringDB, PCH, and Hurricane Electric.
   - Resolves duplicates based on the `peeringlan` field.
   - Outputs the final merged data to `data/ixps.json`.

## Merging Logic
The merge_ixp_data.py script follows a systematic approach to merge data from different sources while avoiding duplicates based on the peeringlan field. Here's a step-by-step breakdown:
1. Load data from PeeringDB, creating a dictionary based on the `peeringlan` field for uniqueness.
2. Load data from PCH, adding entries that are missing in PeeringDB.
3. Load data from Hurricane Electric, adding entries that are missing in both PeeringDB and PCH.
4. Standardize region names for consistency.
5. Save the final merged data to `data/ixps.json`.

This process ensures a comprehensive and non-redundant dataset from multiple sources, avoiding duplicates based on the `peeringlan` field.

## Instructions

1. Run each script in order to collect data from different sources.

   ```bash
   python get_peeringdb_data.py
   python get_pch_data.py
   python get_he_ixps.py

   
After running the scripts, execute the merge script.
python merge_ixp_data.py
The merged data will be saved in data/ixps.json.
```json
[
  {
    "id": "pdb_2",  // Prefix indicates PeeringDB
    "name": "IXP Name",
   "country": 
    "city": 
    "region": 
    "url": "URL of the IXP",
    "peeringlan": "v4/v6 Prefix of Peeringlan"
  },
  {
    "id": "pch_5",  // Prefix indicates PCH
    "name": "IXP Name",
    "country": 
    "city": 
    "region": 
    "url": "URL of the IXP",
    "peeringlan": "v4/v6 Prefix of Peeringlan"
  },
  {
    "id": "he_3",  // Prefix indicates Hurricane Electric
    "name": "IXP Name",
    "country": 
    "city": 
    "region": 
    "url": "URL of the IXP",
    "peeringlan": "v4/v6 Prefix of Peeringlan"
  },

]
```
## Dependencies
Python 3.x
Requests
BeautifulSoup (for web scraping)

## Contributing
Contributions are welcome! If you encounter issues, have suggestions, or want to add support for additional IXPs, feel free to open an issue or submit a pull request.
