import requests
import csv
import xml.etree.ElementTree as ET
import os

def fetch_country_codes():
    username = 'qasimlone'
    base_url = 'http://api.geonames.org'
    endpoint = f'{base_url}/countryInfo?'

    params = {
        'username': username
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch country codes. Status code: {response.status_code}")
        return None

def create_country_code_mapping(xml_content):
    country_code_mapping = {}

    root = ET.fromstring(xml_content)
    for country_element in root.findall('.//country'):
        country_name = country_element.find('countryName').text
        country_code_element = country_element.find('countryCode')

        if country_code_element is not None:
            country_code = country_code_element.text
            country_code_mapping[country_name] = country_code

    return country_code_mapping

def save_country_code_mapping(mapping, output_file_path):
    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Country', 'CC']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for country, code in mapping.items():
            writer.writerow({'Country': country, 'CC': code})

def main():
    xml_content = fetch_country_codes()
    if xml_content:
        country_code_mapping = create_country_code_mapping(xml_content)
        
        if country_code_mapping:
            output_file_path = os.path.join('data', 'country_codes.csv')
            save_country_code_mapping(country_code_mapping, output_file_path)
            print(f"Country code mapping saved to {output_file_path}")
        else:
            print("Failed to create country code mapping.")
    else:
        print("Failed to fetch XML content.")

if __name__ == '__main__':
    main()

