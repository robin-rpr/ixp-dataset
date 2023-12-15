import requests
import json
import ipaddress
from xml.etree import ElementTree as ET
import csv
import os
from pprint import pprint

# Function to fetch data from the first endpoint
def get_ixp_data():
    url = "https://www.pch.net/api/ixp/directory/Active?format=json"
    response = requests.get(url)
    return response.json()

# Function to extract required fields from the first endpoint response
def filter_fields(data):
    filtered_data = []
    for item in data:
        filtered_item = {
            "id": item["id"],
            "country": item["ctry"],
            "city": item["cit"],
            "region": item["reg"],
            "name": item["name"],
            "url": item["url"]
        }
        filtered_data.append(filtered_item)
    return filtered_data

# Function to fetch data from the second endpoint using IXP_ID
def get_subnet_data(ixp_id):
    url = f"https://www.pch.net/api/ixp/subnets/{ixp_id}?format=json"
    response = requests.get(url)
    return response.json()

# Function to validate whether a given string is a valid IP network subnet
def is_valid_subnet(subnet_str):
    try:
        ipaddress.ip_network(subnet_str,strict=False)
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError):
        return False

# Function to extract required fields from the second endpoint response
def extract_subnet_fields(data):
    extracted_data = []
    parsing_errors = []

    for item in data:
        subnet_str = item.get("subnet")

        if item.get("status") == "Active" and subnet_str:
            subnet_str =subnet_str.strip()
            if is_valid_subnet(subnet_str):
                extracted_item = {
                    "peeringlan": subnet_str
                }
                extracted_data.append(extracted_item)
            else:
                parsing_errors.append({
                    "id": item.get("id"),
                    "subnet": subnet_str
                })

    return extracted_data, parsing_errors

def load_country_code_mapping():
    country_code_mapping = {}

    with open(os.path.join('data', 'country_codes.csv'), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country_code_mapping[row['Country']] = row['CC']

    return country_code_mapping

def translate_country_to_code(country_name, country_code_mapping):
    country_code = country_code_mapping.get(country_name)

    if country_code is None:
        print(f"Country code not found for: {country_name}")

    return country_code

# Main function to generate the desired JSON output
def generate_output():
    # Load country code mapping from the CSV file
    country_codes_mapping = load_country_code_mapping()

    ixp_data = get_ixp_data()
    filtered_ixp_data = filter_fields(ixp_data)

    output_data = []
    parsing_errors = []

    for item in filtered_ixp_data:
        ixp_id = item["id"]
        subnet_data = get_subnet_data(ixp_id)
        extracted_subnet_data, errors = extract_subnet_fields(subnet_data)

        if extracted_subnet_data:
            # Loop over each subnet and create a separate record
            for subnet_item in extracted_subnet_data:
                # Translate country name to country code
                country_code = translate_country_to_code(item["country"], country_codes_mapping)
                output_item = {
                    "id": f"pch_{item['id']}",
                    "name": item["name"],
                    "country": country_code,
                    "city": item["city"],
                    "region": item["region"],
                    "url": item["url"],
                    "peeringlan": subnet_item["peeringlan"]
                }
                output_data.append(output_item)

        if errors:
            parsing_errors.extend(errors)

    return output_data, parsing_errors

# Run the main function and save the result to a file
result, errors = generate_output()

output_file_path = "data/pch.json"
with open(output_file_path, "w") as output_file:
    json.dump(result, output_file, indent=2)

print(f"Output saved to {output_file_path}")

# Save parsing errors to a separate file
error_file_path = "data/pch_parsing_errors.json"
with open(error_file_path, "w") as error_file:
    json.dump(errors, error_file, indent=2)

print(f"Parsing errors saved to {error_file_path}")

