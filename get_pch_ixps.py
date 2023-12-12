import requests
import json

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
        if "version" in item and "subnet" in item and item["subnet"]:
            extracted_item = {
                "af": item["version"],
                "peeringlan": item["subnet"]
            }
            extracted_data.append(extracted_item)
    return extracted_data

# Main function to generate the desired JSON output
def generate_output():
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
                output_item = {
                    "id": f"pch_{item['id']}",
                    "name": item["name"],
                    "country": item["country"],
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

