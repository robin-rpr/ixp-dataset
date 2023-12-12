import json

def standardize_region_name(region):
    if region == "Asia-Pacific":
        return "Asia Pacific"
    elif region == "South America":
        return "Latin America"
    else:
        return region  # Leave other regions unchanged

def merge_ixp_data():
    # Load data from peeringdb_peeringlan.json
    with open('data/peeringdb_peeringlan.json', 'r') as file:
        peeringdb_data = json.load(file)

    # Create a dictionary of unique entries based on the peeringlan field
    peeringdb_dict = {entry['peeringlan']: entry for entry in peeringdb_data}

    # Load data from pch.json
    with open('data/pch.json', 'r') as file:
        pch_data = json.load(file)

    # Merge only the entries that are missing in peeringdb
    for entry in pch_data:
        peeringlan = entry['peeringlan']
        if peeringlan not in peeringdb_dict:
            peeringdb_dict[peeringlan] = entry

    # Load data from he.json
    with open('data/he.json', 'r') as file:
        he_data = json.load(file)

    # Merge only the entries that are missing in both peeringdb and pch
    for entry in he_data:
        peeringlan = entry['peeringlan']
        if peeringlan not in peeringdb_dict:
            peeringdb_dict[peeringlan] = entry

    # Convert the merged dictionary values to a list for the final output
    merged_result = list(peeringdb_dict.values())

    # Standardize region names
    for entry in merged_result:
        entry['region'] = standardize_region_name(entry.get('region', ''))

    # Save the final output in ixps.json
    with open('data/ixps.json', 'w') as file:
        json.dump(merged_result, file, indent=2)

if __name__ == '__main__':
    merge_ixp_data()

