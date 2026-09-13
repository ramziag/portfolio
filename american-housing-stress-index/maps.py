import pandas as pd
from pathlib import Path
from pprint import pprint
p = Path('.')
resource_path = p/'resources' 
# Create a dict out of the master list of CBSA codes and names
cbsa_codes_names = pd.read_csv(resource_path/'cbsa_codes_names_lookup_cleaned.csv')
cbsa_codes_names.set_index('cbsacode', inplace=True)
ccn_to_dict = cbsa_codes_names.to_dict()

#Load ZIP-CBSA code crosswalk file that needs CBSA names added
zip_to_cbsa = pd.read_csv(resource_path/'ZIP_to_CBSA_122025.csv')
zip_to_cbsa['cbsa_names'] = zip_to_cbsa['CBSA'].map(ccn_to_dict['cbsatitle'])
print(zip_to_cbsa.head)
#print(cbsa_codes_names.dtypes)
output_path = p/('output')
output_path.mkdir()
zip_to_cbsa.to_csv(p/'output'/'converted_file.csv')
#pprint(ccn_to_dict)

#for x in ccn_to_dict:
#    while read_counter < 5:
#        print(x)
#    read_counter+=1
#for x in resource_path.iterdir():
#    print(x)
