
# Quick Start


## Overview

This example-driven tutorial presents 5 steps to get started with Blue Brain Nexus to build and query a simple [knowledge graph](../../knowledge-graph/thinking-in-graph.html).
The goal is to go over some capabilities of Blue Brain Nexus enabling:

* The creation of a project as a protected data space to work with
* An easy ingestion of a dataset
* Querying a dataset to retrieve various information
* Sharing a dataset by making it public

For that we will work with the small version of the [Global Research Identifier Database (GRID) dataset](../dataset/index.html) containing a set of:

* institutes (institutes.csv)
* their acronyms (acronyms.csv)
* their addresses (addresses.csv)
* their urls  (links.csv)
* and their relationships (relationships.csv)

An overview of this dataset can be found [here](../dataset/index.html).

@@@ note
* We will be using [Blue Brain Nexus CLI](https://github.com/BlueBrain/nexus-cli), a python client throughout this quick start tutorial. 
* This tutorial assumes you've installed and configured the CLI. If not, please follow the set up instructions.
@@@

Let's get started.


## Create a project

Projects in BlueBrain Nexus are spaces where data can be:

* **managed**: created, updated, deprecated, validated, secured;
* **accessed**: directly by ids or through various search interfaces;
* **shared**: through fine grain Access Control List.

A **project** is always created within an **organization** just like a git repository is created in a github organization. Organizations can be understood as accounts hosting multiple projects.

### Select an organization

@@@ note
A public organization named **[demo](https://sandbox.bluebrainnexus.io/web/demo)** is already created for the purpose of this tutorial. All projects will be created under this organization.
@@@

The following command should list the organizations you have access to. The **demo** organization should be listed and tagged as non-deprecated in the output.

Command
:   @@snip [list-orgs-cmd.sh](../assets/list-orgs-cmd.sh)

Output
:   @@snip [list-orgs-out.sh](../assets/list-orgs-out.sh)


Let select the **demo** organization.

Command
:   @@snip [select-orgs-cmd.sh](../assets/select-orgs-cmd.sh)

Output
:   @@snip [select-orgs-out.sh](../assets/select-orgs-out.sh)


### Create a project

A project is created with a label and within an organization. The label should be made of alphanumerical characters and its length should be between 3 and 32 (it should match the regex: [a-zA-Z0-9-_]{3,32}).

Pick a label (hereafter referred to as $PROJECTLABEL) and create a project using the following command.
It is recommended to use your github username to avoid collision of projects labels within an organization.

Command
:   @@snip [create-project-cmd.sh](../assets/create-project-cmd.sh)

Output
:   @@snip [create-project-out.sh](../assets/create-project-out.sh)

By default, created projects are private meaning that only the project creator (you) has read and write access to it. We'll [see below](#share-data) how to make a project public.

The output of the previous command shows the list of projects you have read access to. The project you just created should be the only one listed at this point. Let select it.

Command
:   @@snip [select-project-cmd.sh](../assets/select-project-cmd.sh)

Output
:   @@snip [select-project-out.sh](../assets/select-project-out.sh)

We are all set to bring some data within the project we just created.

## Ingest data


### Load the dataset

Let first list the files that made the small version of the GRID dataset.
  
Command
:   @@snip [downloadmovielens-cmd.sh](../assets/downloadmovielens-cmd.sh)

Output
:   @@snip [downloadmovielens-out.sh](../assets/downloadmovielens-out.sh)


The data to be ingested come in 5 csv files (see the output of the above command) containing each a partial description of the organizations. A single command allows
to load the organisations within the institutes.csv file and merge it with all the other csv files.

```shell
nexus resources create --file institutes.csv --type Organization --format csv \
 --idcolumn grid_id --idnamespace http://www.grid.ac/institutes/ \
 --mergewith links.csv --mergewith addresses.csv --mergewith relationships.csv --mergewith acronyms.csv \
 --mergeon grid_id \
 --max-connections 4
```


## Access data

### View data in Nexus Web

Nexus is deployed with a developer oriented web application allowing to browse organizations, projects, data and schemas you have access to.
You can go to the address https://sandbox.bluebrainnexus.io/web/demo and browse the data you just loaded.

### List data

The simplest way to accessed data within Nexus is by listing them. The following command lists 5 resources:


Command
:   @@snip [list-res-cmd.sh](../assets/list-res-cmd.sh)


The full payload of the resources are not retrieved when listing them: only identifier, type as well as Nexus added metadata are.
But the result list can be scrolled and each resource fetched by identifier. 

Let fetch the EPFL organization identified by http://www.grid.ac/institutes/grid.5333.6

Command
:   @@snip [fetch-res-id-cmd.sh](../assets/fetch-res-id-cmd.sh)

Output
:   @@snip [fetch-res-id-out.sh](../assets/fetch-res-id-out.sh)

Whenever a resource is created, Nexus injects some useful metadata. The table below details some of them:

| Metadata | Description                                                                                                                          | Value Type |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------|------------|
| @id                  | Generated resource identifier. The user can provide its own identifier.                                                              | URI        |
| @type                | The type of the resource if provided by the user.                                                                                    | URI        |
| \_self               | The resource address within Nexus. It contains the resource management details such as the organization, the project and the schema. | URI        |
| \_createdAt          | The resource creation date.                                                                                                          | DateTime   |
| \_createdBy          | The resource creator.                                                                                                                | DateTime   |

Note that Nexus uses [JSON-LD](../../knowledge-graph/understanding-jsonld.html) as data exchange format.

Filters are available to list specific resources. For example a list of resources of type Organization can be retrieved by running the following command:

Command
:   @@snip [list-res-filter-cmd.sh](../assets/list-res-filter-cmd.sh)

Output
:   @@snip [list-res-filter-out.sh](../assets/list-res-filter-out.sh)



### Query data

Listing is usually not enough to select specific subset of data. Data ingested within each project can be searched through two complementary search interfaces called [views](../../../api/1.0/kg/kg-views-api.md).

View              | Description
------------------|---------------
ElasticSearchView | Exposes data in [ElasticSearch](https://www.elastic.co/products/elasticsearch), a document oriented search engine and provide access to it using the [ElasticSearch query language](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html).
SparqlView        | Exposes data as a [graph](../../knowledge-graph/thinking-in-graph.html) and allows to navigate and explore the data using the [W3C Sparql query language](../../knowledge-graph/querying-knowledge-graph.html).

#### Query data using the ElasticSearchView

The ElasticSearchView URL is available at the address https://sandbox.bluebrainnexus.io/v1/views/demo/$PROJECTLABEL/documents/_search.

The query below selects 5 organizations sorted by creation date in descending order.


Select queries
:   @@snip [select_elastic.sh](../assets/select_elastic.sh)



#### Query data using the SparqlView

The SparqlView is available at the address [https://sandbox.bluebrainnexus.io/v1/views/demo/$PROJECTLABEL/graph/sparql].
The following diagram shows how the MovieLens data is structured in the default Nexus SparqlView. Note that the ratings, tags and movies are joined by the movieId property.

The query below selects 5 organizations sorted by creation date in descending order.

Select queries
:   @@snip [select_sparql.sh](../assets/select_sparql.sh)


## Share data

Making a dataset public means granting read permissions to "anonymous" user.

```shell
$ nexus acls make-public
```

To check that the dataset is now public:

* Ask the person next to you to list resources in your project.
* Or create and select another profile named public-tutorial (following the instructions in the [Set up](../setup/index.html).
You should see the that the public-tutorial is selected and its corresponding token column is None.

Output
:   @@snip [select-profile-public-out.sh](../assets/select-profile-public-out.sh)


* Resources in your project should be listed with the command even though you are not authenticated.

Command
:   @@snip [list-res-org-proj-cmd.sh](../assets/list-res-org-proj-cmd.sh)
