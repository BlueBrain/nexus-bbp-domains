# Nexus morphology integration


## Step 1: Configure the Blue Brain Nexus Environment

Go to Nexus Web (https://bbp.epfl.ch/nexus/web) and obtain the access token. 
Fill the config.json with the deployment url, organization and project name 
as well as the token. 

## Step 2: Fill the metadata of the morphology
Fill the metadata.json with all the fields except mtype which is an optional field. 

## Step 3: Ingest data
Run the ```nexus-morphology-integration.py``` to ingest data in the terminal. 
If the ingestion succeeds, it would return the Nexus IDs of the ingested entities.
```bash
$ python nexus-morphology-integration.py $metadata.json
Nexus instance connected

Data ingested successfully. The resulting Nexus IDs are: 
{
  "image_id": "https://bbp.epfl.ch/neurosciencegraph/data/imagestack.18454",
  "subject_id": "https://bbp.epfl.ch/neurosciencegraph/data/subject.Ai82;Ai140-37336",
  "morphology_id": "https://bbp.epfl.ch/neurosciencegraph/data/neuronmorphology.z3718-x10944-y12141"
}

Please email the resulting IDs to <patrycja.lurie@epfl.ch>

```


## Step 4: Notify data curator
Notify the morphology curator at EPFL by email to <patrycja.lurie@epfl.ch>.