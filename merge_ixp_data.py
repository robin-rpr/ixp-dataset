from pprint import pprint
import json
import ipaddress

def standardize_region_name(region):
    if region == "Asia-Pacific":
        return "Asia Pacific"
    elif region == "South America":
        return "Latin America"
    else:
        return region  # Leave other regions unchanged

def create_entry_data(entry, prefix, suffix=''):
    return {
        'entry_data': {
            **entry,
            'id': f"{entry['id']}_{suffix:02}" if suffix else entry['id']
        },
        'prefix': prefix,
        'id': f"{entry['id']}_{suffix:02}" if suffix else entry['id'],
    }

def is_subnet(existing, new_prefix):
    if existing.version != new_prefix.version:
        return False
    return existing.subnet_of(new_prefix)

def is_supernet(existing, new_prefix):
    if existing.version != new_prefix.version:
        return False
    return existing.supernet_of(new_prefix)

def remove_entry_with_prefix(prefix_to_remove, ip_dict):
    # Create a list of keys to remove
    keys_to_remove = [key for key, entry_data in ip_dict.items() if entry_data['prefix'] == prefix_to_remove]

    # Remove the entries with the specified prefix
    for key in keys_to_remove:
        del ip_dict[key]

    if keys_to_remove:
        print(f"Entries with prefix {prefix_to_remove} removed.")
    else:
        print(f"No entries found with prefix {prefix_to_remove}.")

def process_data_file(file_path, ip_dict):
    with open(file_path, 'r') as file:
        data = json.load(file)

        for entry in data:
            peeringlan = entry['peeringlan']
            prefix = ipaddress.IPv4Network(peeringlan, strict=False) if ':' not in peeringlan else ipaddress.IPv6Network(peeringlan, strict=False)

            # Check if the prefix already exists in the dictionary, if yes, skip the entry
            prefix_exists = any(ip_dict_entry['prefix'] == prefix for ip_dict_entry in ip_dict.values())
            if prefix_exists:
                continue

            # Check if it's a subnet of an existing prefix
            subnet_of_existing = any(is_subnet(prefix, ip_dict_entry['prefix']) for ip_dict_entry in ip_dict.values())
            if subnet_of_existing:
                continue

            # Check if it's a supernet of an existing prefix
            supernet_of_existing = any(is_supernet(prefix, ip_dict_entry['prefix']) for ip_dict_entry in ip_dict.values())
            if supernet_of_existing:
                # Remove subnets of the existing supernet from the dictionary
                subnets_to_remove = [ip_dict_entry['prefix'] for ip_dict_entry in ip_dict.values() if is_subnet(ip_dict_entry['prefix'], prefix)]
                for subnet_to_remove in subnets_to_remove:
                    remove_entry_with_prefix(subnet_to_remove, ip_dict)

            # Add the entry to the dictionary with a unique ID
            counter = 1
            while f"{entry['id']}_{counter:02}" in ip_dict:
                counter += 1
            ip_dict[f"{entry['id']}_{counter:02}"] = create_entry_data(entry, prefix, counter)

def merge_ixp_data():
    # Separate dictionary for IPv4 and IPv6 entries
    ip_dict = {}

    # Process peeringdb_data
    process_data_file('data/peeringdb_peeringlan.json', ip_dict)

    # Process pch_data
    process_data_file('data/pch.json', ip_dict)

    # Process he_data
    process_data_file('data/he.json', ip_dict)

    # Convert the merged dictionary values to a list for the final output
    merged_result = [entry_data['entry_data'] for entry_data in ip_dict.values()]

    # Standardize region names
    for entry_data in merged_result:
        entry_data['region'] = standardize_region_name(entry_data.get('region', ''))

    # Save the final output in ixps.json
    with open('data/ixps.json', 'w') as file:
        json.dump(merged_result, file, indent=2)

if __name__ == '__main__':
    merge_ixp_data()
