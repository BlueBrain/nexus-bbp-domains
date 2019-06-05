import urllib.request
import pandas as pd
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import Namespace, OWL
import json

pd.set_option('display.max_colwidth', -1)

# Utility functions to create sparql wrapper around a sparql endpoint

from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET, POSTDIRECTLY, CSV
import requests


SHACL = Namespace('http://www.w3.org/ns/shacl#')
VANN = Namespace('http://purl.org/vocab/vann/')
PROV = Namespace('http://www.w3.org/ns/prov#')
nxv = Namespace('https://bbp-nexus.epfl.ch/vocabs/nexus/core/terms/v0.1.0/')
nxv_v1 = Namespace('https://bluebrain.github.io/nexus/vocabulary/')
nxv_v0 = Namespace('https://bbp.epfl.ch/nexus/v0/vocabs/nexus/core/terms/v0.1.0/')
DCAT =Namespace("http://www.w3.org/ns/dcat#")
NSG_v1 = Namespace('https://neuroshapes.org/')
NSG = Namespace('https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/')
SKOS=Namespace('http://www.w3.org/2004/02/skos/core#')
SCHEMA=Namespace('http://schema.org/')

bindings={
"schema":"http://schema.org/",
"prov":"http://www.w3.org/ns/prov#",
"sh":SHACL,
"vann": VANN,
"skos":"http://www.w3.org/2004/02/skos/core#",
"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
"xml": "http://www.w3.org/XML/1998/namespace",
"xsd": "http://www.w3.org/2001/XMLSchema#",
"nsg" : "https://neuroshapes.org/",
"nxv": "https://bluebrain.github.io/nexus/vocabulary/",
"dcterms":"http://purl.org/dc/terms/",
"dc":"http://purl.org/dc/elements/1.1/",
"owl":OWL,
"context":"https://incf.github.io/neuroshapes/contexts/"

}
DATAFRAME = "DATAFRAME"

class SparqlViewHelper(object):

    def __init__(self, sparql_endpoint, environment=None,org=None, project=None, token=None):
        
        super(SparqlViewHelper, self).__init__()
        self.sparql_endpoint = sparql_endpoint
        self.sparqlview_wrapper = self.create_sparqlview_wrapper(sparql_endpoint=self.sparql_endpoint, token=token,http_query_method= POST, result_format=JSON)
        self.context_dict = self.load_context()
        self.bindings = bindings
        if environment:
            self.bindings["vocab"]="/".join([environment,"vocabs",org,project,""])


    def load_context(self):
        context_dict = {}
        #context_json = json.load("/Users/mfsy/dev/apps/forked/nexus/src/main/paradox/docs/bbptutorial/notebooks/context.json")
        with open('./context.json') as json_file:
            context_json = json.load(json_file)
            if context_json:
                context_json = context_json["@context"][0]
                for k, v in context_json.items():
                    context_dict[k]=v
        return context_dict


    def add_sparql_prefix(self,sparql_query):

        sparql_prefixes=""
        for k,v in self.bindings.items():
            sparql_prefixes += "PREFIX %s: <%s> \n" % (k,v)
        return sparql_prefixes+sparql_query

    def query_sparql(self, sparql_query, result_format=None,offset=0, page_size=20):
        try:
            sparql_query = self.add_sparql_prefix(sparql_query)
            #print(sparql_query)
            self.sparqlview_wrapper.setQuery(sparql_query)
            result_object = self.sparqlview_wrapper.query()
            if result_format:
                if result_format == "DATAFRAME":
                    return self.sparql2dataframe(result_object._convertJSON())
                else:
                    self.sparqlview_wrapper.setReturnFormat(result_format)
            
            if self.sparqlview_wrapper.returnFormat == JSON:
                return result_object._convertJSON()
            return result_object.convert()
            
        except Exception as e:
            raise SparqlQueryException("""Failed to execute the query %s.""" % (sparql_query)) from e
    
    
    def create_sparqlview_wrapper(self, sparql_endpoint, http_query_method=POST, result_format= JSON, token=None):
        sparql_client = SPARQLWrapper(sparql_endpoint)
        if token:
            sparql_client.addCustomHttpHeader("Authorization","Bearer {}".format(token))
        sparql_client.setMethod(http_query_method)
        sparql_client.setReturnFormat(result_format)
        if http_query_method == POST:
            sparql_client.setRequestMethod(POSTDIRECTLY)

        return sparql_client

    # Convert SPARQL results into a Pandas data frame
    def sparql2dataframe(self, json_sparql_results):
        cols = json_sparql_results['head']['vars']
        out = []
        for row in json_sparql_results['results']['bindings']:
            item = []
            for c in cols:
                item.append(row.get(c, {}).get('value'))
            out.append(item)
        return pd.DataFrame(out, columns=cols)

    # ..................
    # ENTITY Queries
    # ..................

    def get_entity_by_type(self, _type, result_format=None):
        """ Retrieve entities by type
        """
        sparlq_query= """Select DISTINCT ?s WHERE {
                   { ?s a <%s> }
               }
               """ % (_type)
        return self.query_sparql(sparlq_query,result_format)

    def get_dataset_contenturls(self, aURI, result_format=None):
        """ Retrieve entities by type
        """
        sparlq_query= """Select DISTINCT * WHERE {
                   { 
                   BIND (<%s> as ?dataset).
                   <%s> a schema:Dataset.
                     OPTIONAL {
                        <%s> schema:hasPart ?part.
                        ?part schema:distribution / schema:contentUrl ?partcontentUrl.
                        ?part schema:name ?name
                        
                     }
                     OPTIONAL {
                        <%s> schema:distribution / schema:contentUrl ?maincontentUrl.
                     }
                    }
               }
               """ % (aURI,aURI, aURI, aURI)
        return self.query_sparql(sparlq_query,result_format)

    def get_prefix_mapping(self, prefix, isliteral=False):
        print("iiiiiiii")
        print(prefix)
        print(isliteral)

        if prefix:
            if prefix in self.context_dict:
                return self.context_dict[prefix]
            else:
                if ":" not in prefix:
                    if isliteral:
                        print("isldsdsds")
                        print(prefix)
                        return prefix

                    else:
                        return "vocab:" + prefix
                else:
                    return prefix

        else:
            return prefix

    def get_entity_by_path_value(self, path, literal_value=None, uri_value=None, _type=None, retrieve_properties=None, result_format=None):
        """ Retrieve entities by path value
        """

        if literal_value and uri_value:
            raise ValueError("One value (either literal_value or uri_value) should be provided.")
        if not literal_value and not uri_value:
            raise ValueError("Exactly one value (either literal_value or uri_value) should be provided.")

        if literal_value:
            value = self.get_prefix_mapping(literal_value, isliteral=True)
        elif uri_value:
            value = self.get_prefix_mapping(literal_value, isliteral=False)

        type_filter = self._build_type_filter(_type)
        retrieve_properties_filter = self._build_retrieve_properties(retrieve_properties)
        sparlq_query= """Select DISTINCT * WHERE {
                     ?s %s %s.
                     %s.
                     %s
                     
               }
               """ % (self.get_prefix_mapping(path), self.get_prefix_mapping(value), type_filter, retrieve_properties_filter)
        return self.query_sparql(sparlq_query,result_format)
    
    def _build_type_filter(self, _type):
        type_filter= ""
        if _type:
            type_filter = """?s a <%s>""" % (self.get_prefix_mapping(_type))
        return type_filter
    
    def _build_retrieve_properties(self, retrieve_properties):
        retrieve_properties_filter= ""
        if retrieve_properties:
            if type(retrieve_properties) ==str:
                retrieve_properties = [retrieve_properties]
            for prop in retrieve_properties:
                retrieve_properties_filter += """?s %s ?%s_value . \n""" % (self.get_prefix_mapping(prop),prop)
        return retrieve_properties_filter
            
    

class SparqlQueryException(Exception):
    pass