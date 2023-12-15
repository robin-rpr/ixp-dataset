# IXP Data Integration

This repository contains Python scripts to fetch, merge, and analyze Internet Exchange Point (IXP) data from various sources, including PeeringDB, PCH, and Hurricane Electric.

## Scripts

1. **PeeringDB Script (`get_peeringdb_data.py`):**
   - Fetches data from PeeringDB API.
   - Outputs data to `data/peeringdb.json`.

2. **PCH Script (`get_pch_data.py`):**
   - Retrieves data from the PCH API.
   - Only cosider data for IXPs whcih have status active
   - Outputs data to `data/pch.json`.

3. **Hurricane Electric Script (`get_he_ixps.py`):**
   - Scrapes data from the [bgp.he.net](https://bgp.he.net) website.
   - Added a further check, and only consider prefixes where data feed health is not bad
   - Outputs data to `data/he.json`.

4. **Merge IXP Data Script (`merge_ixp_data.py`):**
   - Merges data from PeeringDB, PCH, and Hurricane Electric.
   - Resolves duplicates based on the `peeringlan` field.
   - Outputs the final merged data to `data/ixps.json`.

## Merging Logic
The merge_ixp_data.py script processes data from different sources related to internet exchange points (IXPs) and merges them into a unified dataset. The data includes information about ixp name, regions, countries, and peering LAN prefixes associated with various IXPs. Please keep in mind there are IXPs that have colocations in several countries. We have not mapped those in our dataset.

The `process_data_file` function reads data from JSON files and populates a dictionary (`ip_dict`) with information about each IXP entry, including the peering LAN prefix. It checks for duplicate prefixes and handles cases where a prefix is a subnet or supernet of an existing entry. If a supernet is found, it removes subnets of that supernet from the dictionary to ensure a consistent and non-overlapping dataset.

The script also ensures that each entry has a unique identifier (`id`) by combining the IXP's identifier (pdb, pch, or he), the IX ID, and a counter. The generated ID format is "{pdb/pch/he}_{ix_id}_{counter:02}", where the counter ensures uniqueness. The `create_entry_data` function is responsible for constructing the entry data with the modified ID and prefix.

Finally, the script standardizes region names, and the resulting dataset is saved to a JSON file named `ixps.json`. The `standardize_region_name` function helps in converting specific region names to a standardized format.

In summary the merge_ixp_data.py script follows following approach to merge data from different sources while avoiding duplicates based on the peeringlan field. 

Here's a step-by-step breakdown:
1. Load data from PeeringDB, creating a dictionary based on the `peeringlan` field for uniqueness.
2. Load data from PCH, adding entries that are missing in PeeringDB.
3. Load data from Hurricane Electric, adding entries that are missing in both PeeringDB and PCH.
4. Remove duplicates and subnets
5. Standardize region names for consistency.
6. Save the final merged data to `data/ixps.json`.


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
