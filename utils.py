import json
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from time import sleep


# Prefixes to use in SPARQL queries
prefixes = '''
prefix fcu:            <http://ontology.inrae.fr/frenchcropusage/>
prefix owl:            <http://www.w3.org/2002/07/owl#>
prefix rdf:            <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs:           <http://www.w3.org/2000/01/rdf-schema#>
prefix skos:           <http://www.w3.org/2004/02/skos/core#>
prefix skosxl:         <http://www.w3.org/2008/05/skos-xl#>
prefix taxrefp:        <http://taxref.mnhn.fr/lod/property/>
prefix taxrefrk:       <http://taxref.mnhn.fr/lod/taxrank/>
prefix xsd:            <http://www.w3.org/2001/XMLSchema#>
'''


def exec_sparql(endpoint, query):
    """
    Execute a SPARQL query and return results as a Pandas DataFrame.
    Invocation uses the HTTP POST method. Requested result format is JSON.

    In case of failure, the function retries up to MAX_ATTEMPTS attempts while waiting increasing time between each attempt.
    An empty DataFrame is returned in case no attempt is successful.
    """
    # Max number of time a SPARQL query can fail before giving up
    MAX_ATTEMPTS = 3

    sparql = SPARQLWrapper(endpoint)
    sparql.setMethod(POST)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    
    attempt = 1;
    success = False
    while not success and attempt <= MAX_ATTEMPTS:
        try:
            raw_results = sparql.query()
            results = raw_results.convert()
        except:
            print(f'Error while executing SPARQL query (attempt {attempt}/{MAX_ATTEMPTS}).', end=' ')
            if attempt < MAX_ATTEMPTS:
                # Wait a few seconds before next attempt (5, 10, 15, ...)
                print(f'Will retry in {attempt * 5}s.')
                sleep(attempt * 5)
        else:
            success = True
        finally:
            attempt = attempt + 1

    if success:
        if 'head' in results and 'results' in results:
            cols = results['head']['vars']
            out = []
            for row in results['results']['bindings']:
                item = []
                for c in cols:
                    item.append(row.get(c, {}).get('value'))
                out.append(item)
            return pd.DataFrame(out, columns=cols)
        else:
            print('Invalid SPARQL result. Will return empty DataFrame.\n' + str(results))
    else:
        print(f'Unable to execute SPARQL query after {MAX_ATTEMPTS} attempts. Will return empty DataFarme.')
                  
    return pd.DataFrame()            


def dataframe_preview(df, start=0, end=10):
    """
    Simple preview of a dataframe's stats and first lines
    """
    print("== Number of lines: " + str(df.shape[0]))
    print("== Number of unique values:")
    print(df.nunique())
    display(df[start:end])
