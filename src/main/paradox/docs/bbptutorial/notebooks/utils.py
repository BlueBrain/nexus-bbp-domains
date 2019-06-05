import json
from pygments.lexers import JsonLexer
from pygments import highlight
from pygments.formatters import TerminalFormatter
import os
import requests
from nexussdk.utils import http as nexussdk_http

def get_at_id(data_type:str, allen_id:str) -> str:
    """
    :param data_type: The type of the data to be created (e.g. "cell" for data of type cell)
    :param allen_id: The identifier provided by the allen institute
    :return: An identifier string to be used in the @id field of the payload for Blue Brain Nexus
    """
    at_id = "https://bbp.epfl.ch/neurosciencegraph/data/{}_{}".format(data_type, allen_id)
    return at_id

def get_json(filename:str) -> dict:
    """
    :param filename: The file name of the json file to be loaded
    :return: The json file as dictionary
    """
    with open(filename) as json_file:
        json_data = json.load(json_file)
        return json_data

def get_layer(layer:str) -> dict:
    """
    :param layer: The cortical layer as string ("1", "2", "3" ...)
    :return: The layer object with the ontology term to be included in the payload for Blue Brain Nexus
    """
    layer_object = None
    if layer == "1":
        layer_object = {
            "label": "layer 1",
            "@id": "http://purl.obolibrary.org/obo/UBERON_0005390"
        }
    elif layer == "2":
        layer_object = {
            "label": "layer 2",
            "@id": "http://purl.obolibrary.org/obo/UBERON_0005391"
        }
    elif layer == "3":
        layer_object = {
            "label": "layer 3",
            "@id": "http://purl.obolibrary.org/obo/UBERON_0005392"
        }
    elif layer == "4":
        layer_object = {
            "label": "layer 4",
            "@id": "http://purl.obolibrary.org/obo/UBERON_0005393"
        }
    elif layer == "5":
        layer_object = {
            "label": "layer 5",
            "@id": "http://purl.obolibrary.org/obo/UBERON_0005394"
        }
    elif layer == "6":
        layer_object = {
            "label": "layer 6",
            "@id": "http://purl.obolibrary.org/obo/UBERON_0005395"
        }
    return layer_object

def pretty_print(payload:dict):
    """
    This helper function display a Python dict in a nice way, using the JSON syntax and an indentation of 2.
    Credits: Pierre-Alexandre Fonta
    :param payload: A Python dict
    """
    print(highlight(json.dumps(payload, indent=4), JsonLexer(), TerminalFormatter()))

def analysis(personID:str, datasetID:str, file_meta:dict) -> dict:
    """
    :param personID: The Blue Brain Nexus identifier of the person agent
    :param datasetID: The Blue Brain Nexus identifier for the dataset on which the analysis was performed
    :param file_meta: The Blue Brain Nexus generated metadata of the file
    :return: The Blue Brain Nexus payload for the analysis
    """
    try:
        payload = {}
        payload["@context"] = "https://bbp.neuroshapes.org"
        payload["@type"] = ["Entity", "Analysis"]
        payload["name"] = "Persistence Image"
        payload["derivation"] =  [{
            "@type": "Derivation",
            "entity": {
                "@id": datasetID
            }
        }]
        payload["contribution"] = {
            "@type": "Contribution",
            "agent": {
                "@id": personID,
                "@type": [
                    "Agent",
                    "Person"
                ]
            }
        }
        payload["distribution"] = [
            {
                "@type": "DataDownload",
                "contentSize": {
                    "unitCode": "bytes",
                    "value": file_meta["content_value"]
                },
                "contentUrl": {
                    "@id": file_meta["file_id"]
                },
                "digest": {
                    "algorithm": "SHA-256",
                    "value": file_meta["digest_value"]
                },
                "encodingFormat": "image/png",
                "name": file_meta["file_name"]
            }
        ]
        return payload
    except Exception as exc:
        print(exc)

def subject(cell_metadata: dict) -> dict:
    """
    :param cell_metadata: The metadata of the cell
    :return: The Blue Brain Nexus payload for the subject
    """
    try:
        payload = {}
        allen_id = cell_metadata["donor__id"]
        payload["@context"] = "https://bbp.neuroshapes.org"
        at_id = get_at_id("subject", allen_id)
        payload["@id"] = at_id
        payload["@type"] = ["Entity", "Subject"]
        payload["name"] = cell_metadata["donor__name"]
        payload["identifier"] = allen_id
        species_label = cell_metadata["donor__species"]
        if species_label == "Mus musculus":
            payload["species"] = {
                "label": species_label,
                "@id":"https://www.ncbi.nlm.nih.gov/taxonomy/10090"}
        elif species_label == "Homo Sapiens":
            payload["species"] = {
                "label": "Homo sapiens",
                "@id": "http://purl.obolibrary.org/obo/NCBITaxon_9606"}
        sex_label = cell_metadata["donor__sex"]
        if sex_label == "Male":
            payload["sex"] = {
                "label": "male",
                "@id":"http://purl.obolibrary.org/obo/PATO_0000384"}
        elif sex_label == "Female":
            payload["sex"] = {
                "label": "female",
                "@id": "http://purl.obolibrary.org/obo/PATO_0000383"}
        return payload
    except Exception as exc:
        print(exc)

def patchedcell(cell_metadata: dict, allen_grid:str) -> dict:
    """
    :param cell_metadata: The metadata of the cell
    :param allen_grid: The grid identifier of the Allen Institute
    :return: The Blue Brain Nexus payload for the patched cell
    """
    try:
        payload = {}
        allen_id = cell_metadata["specimen__id"]
        payload["@context"] = "https://bbp.neuroshapes.org"
        at_id = get_at_id("patchedcell", allen_id)
        payload["@id"] = at_id
        payload["@type"] = ["Entity", "PatchedCell"]
        payload["name"] = cell_metadata["specimen__name"]
        payload["identifier"] = allen_id
        brainregion_label = cell_metadata["structure__acronym"]
        structure_area_id = cell_metadata["structure__id"]
        brainregion_id = "http://api.brain-map.org/api/v2/data/Structure/{}".format(structure_area_id)
        payload["brainLocation"] = {
            "@type": "BrainLocation",
            "brainRegion": {
                "label": brainregion_label,
                "@id": brainregion_id
            }
        }
        payload["derivation"] =  [{
            "@type": "Derivation",
            "entity": {
                "@id": get_at_id("subject", cell_metadata["donor__id"])
            }
        }]
        payload["subject"] = {
            "@id": get_at_id("subject", cell_metadata["donor__id"]),
            "@type": [
                "Subject",
                "Entity"
            ]
        }
        payload["contribution"] = {
            "@type": "Contribution",
            "agent": {
                "@id": allen_grid,
                "@type": [
                    "Agent",
                    "Organization"
                ]
            }
        }
        return payload
    except Exception as exc:
        print(exc)

def neuronmorphology(cell_metadata: dict, allen_grid:str, file_meta:dict) -> dict:
    """
    :return: The Blue Brain Nexus payload for the patched cell
    :param file_meta: The Blue Brain Nexus generated metadata of the file
    :return: The Blue Brain Nexus payload for the patched neuron morphology
    """
    try:
        payload = {}
        allen_id = cell_metadata["specimen__id"]
        payload["@context"] = "https://bbp.neuroshapes.org"
        at_id = get_at_id("neuronmorphology", allen_id)
        payload["@id"] = at_id
        payload["@type"] = ["Entity", "NeuronMorphology"]
        payload["name"] = cell_metadata["specimen__name"]
        payload["identifier"] = allen_id
        payload["apicalDendrite"] = cell_metadata["tag__apical"]
        brainregion_label = cell_metadata["structure__acronym"]
        structure_area_id = cell_metadata["structure__id"]
        brainregion_id = "http://api.brain-map.org/api/v2/data/Structure/{}".format(structure_area_id)
        payload["brainLocation"] = {
            "@type": "BrainLocation",
            "brainRegion": {
                "label": brainregion_label,
                "@id": brainregion_id
            },
            "coordinatesInBrainAtlas": {
                "valueX": cell_metadata["csl__x"],
                "valueY": cell_metadata["csl__y"],
                "valueZ": cell_metadata["csl__z"]
            },
            "layer": get_layer(cell_metadata["structure__layer"])
        }
        payload["derivation"] =  [{
            "@type": "Derivation",
            "entity": {
                "@id": get_at_id("subject", cell_metadata["donor__id"])
            }
        },
            {
                "@type": "Derivation",
                "entity": {
                    "@id": get_at_id("patchedcell", cell_metadata["specimen__id"])
                }
            }
        ]
        payload["subject"] = {
            "@id": get_at_id("subject", cell_metadata["donor__id"]),
            "@type": [
                "Subject",
                "Entity"
            ]
        }
        payload["contribution"] = {
            "@type": "Contribution",
            "agent": {
                "@id": allen_grid,
                "@type": [
                    "Agent",
                    "Organization"
                ]
            }
        }
        payload["distribution"] = [
            {
                "@type": "DataDownload",
                "contentSize": {
                    "unitCode": "bytes",
                    "value": file_meta["content_value"]
                },
                "contentUrl": {
                    "@id": file_meta["file_id"]
                },
                "digest": {
                    "algorithm": "SHA-256",
                    "value": file_meta["digest_value"]
                },
                "encodingFormat": "application/octet-stream",
                "name": file_meta["file_name"]
            }
        ]
        return payload
    except Exception as exc:
        print(exc)


#Resource creation from json
def create_resource(nexus, json_payload, org, project):
    try:
        response = nexus.resources.create(org_label=org, project_label=project, data=json_payload)
        return response
    except nexus.HTTPError as ne:
        return ne.response.json()

def create_resolver(nexus, json_payload, org, project):
    try:
        full_url = nexussdk_http._full_url(path=[nexus.resolvers.SEGMENT, org, project], use_base=False)
        response = nexus.resolvers.create_(path=full_url, payload=json_payload)

    #response = nexus.resolvers.create(org_label=org, project_label=project, data=json_payload)
        return response
    except nexus.HTTPError as ne:
        return ne.response.json()


def tag_resource(nexus, json_payload, tag_value, rev_to_tag, rev=None):
    try:
        response = nexus.resources.tag(resource=json_payload, tag_value=tag_value, rev=rev)
        return response
    except nexus.HTTPError as ne:
        return ne.response.json()

#Resource update from an identifier which can be a non url-encoded CURIE or a full URI
def update_resource(nexus,identifier, updated_json_payload, org, project):
    try:
        resource = nexus.resources.fetch(org_label=org,project_label=project,resource_id=identifier)
        resource_current_revision = resource["_rev"]
        updated_json_payload["_self"]= resource["_self"]
        response = nexus.resources.update(resource=updated_json_payload, rev=resource_current_revision)
        return response
    except nexus.HTTPError as e:
        return e.response.json()

#Resource update from an identifier which can be a non url-encoded CURIE or a full URI
def fetch_resource(nexus, identifier, org, project, tag=None, rev=None):
    try:
        response = nexus.resources.fetch(org_label=org,project_label=project,resource_id=identifier, tag=tag, rev=rev)
        return response
    except nexus.HTTPError as e:
        return e.response.json()


def download_from_nexus(downloadurls_to_name, download_dir, token):
    header = dict()
    header["Accept"] = "*/*"
    header["Authorization"] = "Bearer " + token
    download_reports = []
    for download_url, name in downloadurls_to_name:
        download_reports.append(_fetch_url(download_url, name,download_dir,header))
    return download_reports


def _fetch_url(url, name,download_dir, header):
    print(url)
    print(name)
    print(download_dir)
    file_path = "/".join([download_dir,name.replace("/","-")])
    #url = str(url).split("/")[-1]
    try:
        #r = requests.get(url, stream=True)
        #file_metadata = nexus.files.fetch(org_label=org,project_label=project,file_id=url,out_filepath=file_path)

        if not os.path.exists(file_path):
            r = requests.get(url, stream=True, headers=header)
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
                    f.close()
            else:
                raise Exception ("Failed to get the binary with code %" % (r.status_code))
        #print(url)
        return (file_path,"INFO", "Downloaded")

    except Exception as e:
        print(str(e))
        return (file_path,"FATAL", str(e))