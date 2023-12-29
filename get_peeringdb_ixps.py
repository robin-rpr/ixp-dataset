import requests
import json
from collections import defaultdict
from pprint import pprint
import argparse

#KEY = ""
#with open("/Users/qlone/.peeringdb") as inf:
#    KEY = inf.readline().strip()


def get_peeringdb_info(output_peeringlani,apikey):
    headers = {"Authorization": "Api-Key " + apikey}
    ix2lans = {}
    ixlan2ixpfx = defaultdict(lambda: {"peeringlan": []})

    j_ixpfx = requests.get("https://www.peeringdb.com/api/ixpfx", headers=headers).json()

    for ixpfx in j_ixpfx['data']:
        ixlan_id = int(ixpfx['ixlan_id'])
        protocol = ixpfx['protocol']
        ixlan2ixpfx[ixlan_id]['peeringlan'].append(ixpfx['prefix'])

    j_ixlan = requests.get("https://www.peeringdb.com/api/ixlan", headers=headers).json()

    output_data = []

    for ixlan in j_ixlan['data']:
        ix_id = ixlan['ix_id']
        ixlan_id = int(ixlan['id'])

        if ix_id not in ix2lans:
            ix2lans[ix_id] = []

        ix2lans[ix_id].append({
            'ixlan_id': ixlan_id,
            'name': ixlan['name'],
            'desc': ixlan['descr'],
            'peeringlans': ixlan2ixpfx[ixlan_id]['peeringlan']
        })

    r_ix = requests.get("https://www.peeringdb.com/api/ix", headers=headers).json()

    for ix in r_ix['data']:
        ix_id = ix['id']
        if ix_id not in ix2lans:
            print("ixlan not found for ", ix_id)
            raise(0)
            continue

        icountry = ix['country']
        icity = ix['city']
        iname = ix['name']
        iregion_continent = ix['region_continent']
        url = ix['website']

        for ixlan_info in ix2lans[ix_id]:
            if output_peeringlan:
                # Output peeringlan separately
                for peeringlan in ixlan_info['peeringlans']:
                    base_row = {
                        'id': f"pdb_{ixlan_info['ixlan_id']}",
                        'name': iname + ("-%s" % ixlan_info['name'] if ixlan_info['name'] else ""),
                        'country': icountry,
                        'city': icity,
                        'region': iregion_continent,
                        'url': url,
                        'peeringlan': peeringlan
                    }
                    output_data.append(base_row)
            else:
                # Output combined peeringlans
                base_row = {
                    'id': f"pdb_{ixlan_info['ixlan_id']}",
                    'name': iname + ("-%s" % ixlan_info['name'] if ixlan_info['name'] else ""),
                    'country': icountry,
                    'city': icity,
                    'region': iregion_continent,
                    'url': url,
                    'peeringlans': ixlan_info['peeringlans']
                }
                output_data.append(base_row)

    return output_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process PeeringDB data.')
    parser.add_argument('--output-peeringlan', action='store_true',
                        help='Output peeringlan separately.')
    parser.add_argument('apikey', help='API key for authentication')
    args = parser.parse_args()

    peeringdb_data = get_peeringdb_info(args.output_peeringlan,args.apikey)

    output_filename = 'data/peeringdb_peeringlan.json' if args.output_peeringlan else 'data/peeringdb.json'

    with open(output_filename, 'w') as json_file:
        json.dump(peeringdb_data, json_file, indent=2)

    print(f"Output saved to {output_filename}")

