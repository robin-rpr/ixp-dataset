import requests
import json
from xml.etree import ElementTree as ET
import csv
import os

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

# Function to extract required fields from the second endpoint response
def extract_subnet_fields(data):
    extracted_data = []
    for item in data:
        if  "subnet" in item and item["subnet"]:
            extracted_item = {
                "peeringlan": item["subnet"]
            }
            extracted_data.append(extracted_item)
    return extracted_data

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
    for item in filtered_ixp_data:
        ixp_id = item["id"]
        subnet_data = get_subnet_data(ixp_id)
        extracted_subnet_data = extract_subnet_fields(subnet_data)

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

    return output_data

# Run the main function and save the result to a file
result = generate_output()

output_file_path = "data/pch.json"
with open(output_file_path, "w") as output_file:
    json.dump(result, output_file, indent=2)

print(f"Output saved to {output_file_path}")
