import json
from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET, POSTDIRECTLY, CSV
import pandas as pd
import nexussdk as nxs

pd.set_option('display.max_colwidth', -1)

def load_json(filename:str) -> dict:
    """
    :return: The data loaded from a json file.
    """
    with open(filename) as json_file:
        json_data = json.load(json_file)
        return json_data


def save_json(payload:dict, filename:str):
    with open(filename, 'w') as filehandle:
        json.dump(payload, filehandle, sort_keys=True, indent=4)
        

def store_allen_files(nexus, cell_id:str, data_type:str, metadata_dict:dict, org_label:str, project_label:str) -> dict:
    if data_type == "reconstruction":
        file_extension = "swc"
        content_type = "application/swc"
    elif data_type == "ephys":
        file_extension = "nwb"
        content_type = "application/nwb"
    file_path = f"./allen_cell_types_db/specimen_{cell_id}/{data_type}.{file_extension}"
    try:
        response = nxs.files.create(org_label=org_label, project_label=project_label, filepath=file_path, content_type=content_type, filename=f"{cell_id}.{file_extension}")
        metadata_dict[cell_id] = {
           "@type": "DataDownload",
           "url": response["@id"],
            "contentSize": {
                "unitCode": "bytes",
                "value": response["_bytes"]
            },
            "digest": {
                "algorithm": "SHA-256",
                "value": response["_digest"]["_value"],
            },
            "encodingFormat": f"application/{file_extension}",
            "name": response["_filename"]
        }
        at_id = response["@id"]
        print(f"{cell_id} {data_type} stored with @id {at_id}")
    except nxs.HTTPError as e:
        print(e)
        print("---")
        nxs.tools.pretty_print(e.response.json())
    return metadata_dict
        
        
def store_allen_metadata(nexus, org_label, project_label, metadata_entities, morph_files_meta, ephys_files_meta):
    entities = metadata_entities["@graph"]
    context = metadata_entities["@context"]
    for entity in entities:
        entity["@context"] = context
        entity_type = entity["@type"]
        schema = entity_type.lower()
        if "ReconstructedNeuronMorphology" == entity_type:
            distribution = morph_files_meta[int(entity["identifier"])] # TODO: use the identifier
            entity["distribution"] = distribution
            schema = "reconstructedpatchedcell"
        elif "TraceCollection" == entity_type:
            distribution = ephys_files_meta[int(entity["identifier"])] # TODO: use the identifier
            entity["distribution"] = distribution
        try:
            nxs.resources.create(org_label=org_label, project_label=project_label, data=entity, schema_id=f"datashapes:{schema}")
        except nxs.HTTPError as e:
            print(e)
            print("---")
            nxs.tools.pretty_print(e.response.json()) 

def create_sparql_client(sparql_endpoint, http_query_method=POST, result_format=JSON, token=None):
    sparql_client = SPARQLWrapper(sparql_endpoint)
    if token:
        sparql_client.addCustomHttpHeader("Authorization","Bearer {}".format(token))
    sparql_client.setMethod(http_query_method)
    sparql_client.setReturnFormat(result_format)
    if http_query_method == POST:
        sparql_client.setRequestMethod(POSTDIRECTLY)
    
    return sparql_client


# Convert SPARQL results into a Pandas data frame
def sparql2dataframe(json_sparql_results):
    cols = json_sparql_results['head']['vars']
    out = []
    for row in json_sparql_results['results']['bindings']:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get('value'))
        out.append(item)
    return pd.DataFrame(out, columns=cols)

# Send a query using a sparql wrapper 
def query_sparql(query, sparql_client):
    sparql_client.setQuery(query)
    result_object = sparql_client.query()
    if sparql_client.returnFormat == JSON:
        return result_object._convertJSON()
    return result_object.convert()

def query_data(sparqlview_endpoint:str, data_type:str, brain_region_layer:str, apical_dendrite:str, token:str):
    page_size = 5000
    offset = 0
    nexus_df=None
    count = 0
    sparqlview_wrapper = utils.create_sparql_client(sparql_endpoint=sparqlview_endpoint, token=token)
    while (count <= 200000): 
        select_query = """
            SELECT *
            WHERE
            {
                BIND (%s as ?type).
                ?id a nsg:ReconstructedNeuronMorphology;
                  nsg:brainLocation / nsg:layer / rdfs:label %s;
                  nsg:apicalDendrite %s;
                  schema:distribution/schema:url ?downloadUrl;
                  schema:name ?name
            }
            LIMIT 1000
            """ % (data_type, brain_region_layer, apical_dendrite)
        nexus_results = utils.query_sparql(select_query, sparqlview_wrapper)
        result_df = utils.sparql2dataframe(nexus_results)
        if len(result_df.index) > 0:
            if nexus_df is None:
                nexus_df = pd.DataFrame(result_df)
            else:
                nexus_df = pd.concat([nexus_df, result_df], ignore_index=True)
            count = count + page_size
            offset = offset + page_size
        else:
            break;
    return nexus_df