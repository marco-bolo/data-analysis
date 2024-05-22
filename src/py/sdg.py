# todo: python script to add labels to publications text
import os
from pathlib import Path
import requests
import rdflib
import json
import pandas as pd
from pykg2tbl import DefaultSparqlBuilder, KGSource, QueryResult

#Steps:
#   0: Identify required info: title, abstract, description, keywords? & set variables
#   1: Get required info, either from: 
#               -a. publications in GraphDB via sparql endpoint
#               -b. marineinfo_urls
#      & modify into correct format

# Step 0. Identify required info: title, abstract, description, keywords? & set variables
OSDGTOOL_URL = "http://localhost:5002/tag"

# Step 1.a. Get required info from publications in GraphDB & modify into correct format

# SPARQL EndPoint to use - wrapped as Knowledge-Graph 'source'
GDB_BASE: str = os.getenv("GDB_BASE", "http://graphdb:7200/")
#print(f"{os.getenv('GDB_BASE')=}")
#print(f"{GDB_BASE=}")
GDB_REPO: str = os.getenv("GDB_REPO", "kgap")
GDB_ENDPOINT: str = f"{GDB_BASE}repositories/{GDB_REPO}"
GDB: KGSource = KGSource.build(GDB_ENDPOINT)

#print(f"{GDB_ENDPOINT=}")

TEMPLATES_FOLDER = str(Path().absolute() / "queries")
GENERATOR = DefaultSparqlBuilder(templates_folder=TEMPLATES_FOLDER)


def generate_sparql(name: str, **vars) -> str:
    """Simply build the sparql by using the named query and applying the vars"""
    return GENERATOR.build_syntax(name, **vars)


def execute_to_df(name: str, **vars) -> pd.DataFrame:
    """Builds the sparql and executes, returning the result as a dataframe."""
    sparql = generate_sparql(name, **vars)
    result: QueryResult = GDB.query(sparql=sparql)
    return result.to_dataframe()

test = execute_to_df("test.sparql")
print(test)

# Step 1.b. Get required info from marineinfo_url in GraphDB & modify into correct format
#def mi_data(marine_uri: str):
#
#    """
#    get linked data from marine_uri
#    """
#
#    if not marine_uri.endswith(".ttl") or not :
#        data = requests("")
#    return data 

# Step 2. Pass that info in correct format to odsg tool ~ working from csv for now
def get_SDGs(data: str):

    """
    get SDG labels for given text string
    """

    try:
        return requests.post(OSDGTOOL_URL, json={'text': data , 'detailed': True}).json()
            
    except Exception as error:
        return {'result': None, 'status': {'execption-error': error}}


#df = pd.read_csv("./data/pubs_title_abstract.csv")
#df['sdg_text'] = df['title'] + ' | ' + df['abstract']

#pub_sdg_df = pd.DataFrame(columns=['sdg','relevance','fos_ids','fos_names','publication'])
#for i,row in df.iterrows():
#    print(row['publication'])
#    result = get_SDGs(row['sdg_text'])
#
#    sdg_df = pd.DataFrame(result['result'])
#    sdg_df['publication'] = row['publication']
#
#    pub_sdg_df = pd.concat([pub_sdg_df, sdg_df])

# fos_ids and fos_names to ', '-separated list format
#pub_sdg_df['fos_names'] = pub_sdg_df['fos_names'].apply(lambda x: ', '.join(x))
#pub_sdg_df['fos_ids'] = pub_sdg_df['fos_ids'].apply(lambda x: ', '.join(x))
# write to file
#pub_sdg_df.to_csv("./data/pubs_sdg_info.csv")

# Step 3. Semantically uplift the respons into triples --> see task in /config/sembench.yaml
# Step 4. add write new triples to ./data/ folder --> see task in /config/sembench.yaml
