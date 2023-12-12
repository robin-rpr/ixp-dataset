import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_exchange_data():
    url = "https://bgp.he.net/report/exchanges#_exchanges"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    exchange_data = []

    for row in soup.select('#exchangestable tbody tr'):
        exchange_name = row.select_one('td a').text.strip()
        country_code = row.select_one('td:nth-of-type(4)').text.strip()
        city = row.select_one('td:nth-of-type(5)').text.strip()
        website = row.select_one('td:nth-of-type(6) a').get('href')
        exchange_id = re.search(r'/exchange/(.+)', row.select_one('td a').get('href')).group(1)

        # Follow the link to get prefixes and additional details
        exchange_url = f"https://bgp.he.net/exchange/{exchange_id}"
        exchange_response = requests.get(exchange_url)
        exchange_soup = BeautifulSoup(exchange_response.content, 'html.parser')

        # Extracting region information from the second link
        region_element = exchange_soup.select_one('.asleft:-soup-contains("Region:") + .asright')
        region = region_element.text.strip() if region_element else ""

        ipv4_prefix = exchange_soup.select_one('.asleft:-soup-contains("IPv4 Prefixes") + .asright')
        ipv6_prefix = exchange_soup.select_one('.asleft:-soup-contains("IPv6 Prefixes") + .asright')

        # Check if the elements are found before attempting to access their .text property
        ipv4_prefix_text = ipv4_prefix.text.strip() if ipv4_prefix else ""
        ipv6_prefix_text = ipv6_prefix.text.strip() if ipv6_prefix else ""

        # Split the prefixes using commas and create separate entries for each one
        ipv4_prefixes = [p.strip() for p in ipv4_prefix_text.split(",") if p.strip()]
        ipv6_prefixes = [p.strip() for p in ipv6_prefix_text.split(",") if p.strip()]

        # Combine all prefixes into a single list
        all_prefixes = ipv4_prefixes + ipv6_prefixes

        # Create entries for each prefix
        for prefix in all_prefixes:
            exchange_info = {
                "id": f"he_{exchange_id}",
                "name": exchange_name,
                "country": country_code,
                "city": city,
                "region": region,
                "url": website,
                "peeringlan": prefix
            }

            exchange_data.append(exchange_info)

    return exchange_data

if __name__ == "__main__":
    result = scrape_exchange_data()

    output_file_path = "data/he.json"
    with open(output_file_path, "w") as output_file:
        json.dump(result, output_file, indent=2)

    print(f"Output saved to {output_file_path}")

