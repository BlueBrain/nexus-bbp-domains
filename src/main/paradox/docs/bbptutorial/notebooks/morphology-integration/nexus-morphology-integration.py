import nexussdk as nexus
from urllib.parse import quote_plus as url_encode
import requests
import json


def init_nexus():
    config = json.load(open('config.json', 'r'))

    global org
    org = config['organization']
    global project
    project = config['project']
    global deployment
    deployment = config['deployment']
    global token
    token = config['token']

    nexus.config.set_environment(deployment)
    nexus.config.set_token(token)


    try:
        nexus.organizations.list()
        print('Nexus instance connected')
    except nexus.HTTPError as e:
        print("---")
        print(nexus.tools.pretty_print(e.response.json()))
        exit(-1)


def create_subject(name, age, strain_label, strain_id=None):
    subject_id = "https://bbp.epfl.ch/neurosciencegraph/data/subject." + name

    create_subject = False

    try:
        response = nexus.resources.fetch(org_label=org, project_label=project, resource_id=subject_id)
    except nexus.HTTPError as e:
        if e.response.status_code == 404:
            create_subject = True
        else:
            print(e.response.json())
            raise e

    if create_subject:
        if strain_id is None:
            strain_id = 'http://bbp.epfl.ch/neurosciencegraph/ontologies/speciestaxonomy/' + strain_label
        subject = {
            "@context": "https://bbp.neuroshapes.org",
            "@type": "Subject",
            "@id": subject_id,
            "name": name,
            "species": {
                "@id": "http://purl.obolibrary.org/obo/NCBITaxon_10090",
                "label": "Mus musculus"
            },
            "strain": {
                "@id": strain_id,
                "label": strain_label
            },
            "age": {
                "period": "Post-natal",
                "value": {
                    "@value": str(age),
                    "@type": "xsd:integer"
                },
                "unitCode": "days"
            }
        }

        try:
            response = nexus.resources.create(data=subject, org_label=org, project_label=project,
                                              schema_id='datashapes:subject')
        except nexus.HTTPError as e:
            print(subject)
            print("---")
            print(nexus.tools.pretty_print(e.response.json()))

    return response['@id']


def create_image(name, slice_direction, slice_width, slice_height, number_of_slices, slice_resolution,
                 slice_interval, subject_id):
    image_id = "https://bbp.epfl.ch/neurosciencegraph/data/imagestack." + name

    create_image = False

    try:
        response = nexus.resources.fetch(org_label=org, project_label=project, resource_id=image_id)
    except nexus.HTTPError as e:
        if e.response.status_code == 404:
            create_image = True
        else:
            print(e.response.json())
            raise e

    if create_image:
        image = {
            "@context": "https://bbp.neuroshapes.org",
            "@type": [
                "nsg:ImageStack"
            ],
            "@id": image_id,
            "name": name,
            "sliceDirection": slice_direction,
            "sliceWidth": slice_width,
            "sliceHeight": slice_height,
            "numberOfSlices": number_of_slices,
            "nsg:sliceResolution": {
                "nsg:widthResolution": {
                    "@value": slice_width,
                    "@type": "xsd:float"
                },
                "nsg:heightResolution": {
                    "@value": slice_height,
                    "@type": "xsd:float"
                },
                "unitCode": "micron"
            },
            "sliceInterval": {
                "value": {
                    "@value": slice_interval,
                    "@type": "xsd:float"
                },
                "unitCode": "micron"
            },
            "contribution": {
                "@type": "Contribution",
                "agent": {
                    "@id": "https://www.grid.ac/institutes/grid.33199.31",
                    "label": "Huazhong University of Science and Technology"
                }
            },
            "wasDerivedFrom": {
                "@id": subject_id
            }
        }

        try:
            response = nexus.resources.create(data=image, org_label=org, project_label=project,
                                              schema_id='datashapes:imagestack')
        except nexus.HTTPError as e:
            print("---")
            print(nexus.tools.pretty_print(e.response.json()))

    return response['@id']


def create_morphology(name, identifier, image_id, brain_region_label, binary_path, brain_region_id=None):
    # Check if the binary file has been uploaded
    file_id = "https://bbp.epfl.ch/neurosciencegraph/data/file.neuronmorphology." + name

    create_file = False

    try:
        file_response = nexus.files.fetch(org_label=org, project_label=project, file_id=file_id)
    except nexus.HTTPError as e:
        if e.response.status_code == 404:
            create_file = True
        else:
            print(e.response.json())
            raise e

    if create_file:
        url = "{}/files/{}/{}/{}".format(deployment, org, project, url_encode(file_id))
        file_obj = {"file": open(binary_path, "rb")}
        attachment_headers = {}
        attachment_headers["Authorization"] = "Bearer {}".format(token)
        # attachment_headers["Content-Type"] = "text/swc"

        file_response = requests.put(url=url, files=file_obj, headers=attachment_headers).json()

    morphology_file_meta = {
        "file_name": file_response["_filename"],
        "file_size": file_response["_bytes"],
        "file_id": file_response["@id"],
        "content_url": file_response["_self"],
        "digest_value": file_response["_digest"]["_value"]}

    # Create morphology

    morphology_id = "https://bbp.epfl.ch/neurosciencegraph/data/neuronmorphology." + name

    create_morphology = False

    try:
        response = nexus.resources.fetch(org_label=org, project_label=project, resource_id=morphology_id)
    except nexus.HTTPError as e:
        if e.response.status_code == 404:
            create_morphology = True
        else:
            print(e.response.json())
            raise e

    if create_morphology:
        if brain_region_id is None:
            brain_region_id = "http://bbp.epfl.ch/neurosciencegraph/ontologies/brainregion/" + brain_region_label
        morphology = {
            "@context": "https://bbp.neuroshapes.org",
            "@type": [
                "InVitroWholeBrainReconstructedNeuronMorphology"
            ],
            "@id": morphology_id,
            "name": name,
            "identifier": identifier,
            "contribution": {
                "@type": "Contribution",
                "agent": {
                    "@id": "https://www.grid.ac/institutes/grid.263826.b",
                    "label": "Southeast University"
                }
            },
            "brainLocation": {
                "brainRegion": {
                    "@id": brain_region_id,
                    "label": brain_region_label
                }
            },
            "wasDerivedFrom": {
                "@id": image_id
            },
            "distribution": {
                "@type": "DataDownload",
                "contentSize": {
                    "unitCode": "bytes",
                    "value": morphology_file_meta['file_size']
                },
                "contentUrl": morphology_file_meta['content_url'],
                "digest": {
                    "algorithm": "SHA-256",
                    "value": morphology_file_meta['digest_value']
                },
                "encodingFormat": "text/swc",
                "name": morphology_file_meta['file_name']
            }
        }

        try:
            response = nexus.resources.create(data=morphology, org_label=org, project_label=project,
                                              schema_id='datashapes:invitrowholebrainreconstructedneuronmorphology')
        except nexus.HTTPError as e:
            print("---")
            print(nexus.tools.pretty_print(e.response.json()))

    return response['@id']


def create_mtype_annotation(morphology_id, mtype_label, mtype_id=None, comment=""):
    if mtype_id is None:
        mtype_id = "http://bbp.epfl.ch/neurosciencegraph/taxonomies/mtype/" + mtype_label
    mtype_annotation = {
        "@context": "https://bbp.neuroshapes.org",
        "@type": [
            "nsg:MorphologyAnnotation",
            "nsg:Annotation"
        ],
        "name": 'mtype classification',
        "hasTarget": {
            "@id": morphology_id,
            "@type": "nsg:AnnotationTarget"
        },
        "hasBody": {
            "@id": mtype_id,
            "@type": "nsg:AnnotationBody",
            "skos:note": comment,
            "label": mtype_label
        },
        "contribution": {
            "@type": "Contribution",
            "agent": {
                "@id": "https://www.grid.ac/institutes/grid.263826.b",
                "label": "Southeast University"
            }
        }
    }

    try:
        response = nexus.resources.create(data=mtype_annotation, org_label=org, project_label=project,
                                          schema_id='datashapes:annotation')
    except nexus.HTTPError as e:
        print("---")
        print(nexus.tools.pretty_print(e.response.json()))

    return response['@id']


def create_reconstruction(image_id, morphology_id):
    reconstruction = {
        "@context": "https://bbp.neuroshapes.org",
        "@type": [
            "prov:Activity",
            "nsg:ReconstructionFromImage"
        ],
        "used": [
            {
                "@id": image_id,
                "@type": [
                    "nsg:ImageStack",
                    "prov:Entity"
                ]
            }
        ],
        "generated": [
            {
                "@id": morphology_id,
                "@type": [
                    "nsg:ReconstructedCell",
                    "prov:Entity"
                ]
            }
        ]
    }

    try:
        response = nexus.resources.create(data=reconstruction, org_label=org, project_label=project,
                                          schema_id='datashapes:reconstructionfromimage')
    except nexus.HTTPError as e:
        print("---")
        print(nexus.tools.pretty_print(e.response.json()))

    return response['@id']


def ingest_data(metadata):
    subject_id = create_subject(metadata['subject_name'], metadata['subject_age'], metadata['subject_strain'])
    image_id = create_image(metadata['image_name'], metadata['slice_direction'], metadata['slice_width'],
                            metadata['slice_height'], metadata['number_of_slices'], metadata['slice_resolution'],
                            metadata['slice_interval'], subject_id)
    morphology_id = create_morphology(metadata['morphology_name'], metadata['identifier'], image_id,
                                      metadata['brain_region_label'], metadata['file_path'])
    reconstruction_id = create_reconstruction(image_id, morphology_id)

    if metadata['mtype_label'] is not None and metadata['mtype_label'] is not '':
        mtype_id = create_mtype_annotation(morphology_id, metadata['mtype_label'])

    ids = {
        "subject_id": subject_id,
        "image_id": image_id,
        "morphology_id": morphology_id
    }

    return ids


def main():
    init_nexus()
    metadata = json.load(open('metadata.json', 'r'))
    ids = ingest_data(metadata)

    print('\nData ingested successfully. The resulting Nexus IDs are: ')
    nexus.tools.pretty_print(ids)
    print('\nPlease email the resulting IDs to <patrycja.lurie@epfl.ch>')


if __name__ == "__main__":
    main()

