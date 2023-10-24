from elasticsearch import Elasticsearch

INDEX = 'poems_9'
client = Elasticsearch("http://localhost:9200", verify_certs=False, basic_auth=['elastic', '2xv2thxzCm51jguHSy*e'],)

def fundamental_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    query_body = q
    res = client.search(index=INDEX, body=query_body)
    return res

def basic_multiple_filter_search(fields):
    """
    example of query
    {
        "query": {
            "bool" : {
            "must" : [
                {"term" : { "Author" : "வாலி" }},
                {"range" : {"Year" : { "gte" : 1968, "lte" : 2023 }}}
            ]
            }
        }
        }
    """
    q = {}
    q["query"] = {}
    q["query"]["bool"] = {}
    q["query"]["bool"]["must"] = []
    
    for field in fields:
        if field == 'Year':
            q["query"]["bool"]["must"].append({"range":{field:fields[field]}})
        else:
            q["query"]["bool"]["must"].append({"match":{field:fields[field]}})

    print(q)

    res = client.search(index=INDEX, body=q)
    return res


def search_advanced_query(query):
    qus = {
       "query": {
            "wildcard": {
                "Metaphorical Name": "*"+query+"*"
            }
        }
    }

    res = client.search(index=INDEX, body=qus)
    print(res)

    return res


def multi_match(query, fields=['Poem'], operator='or'):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    return q


def agg_target_domain(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "aggs": {
            "target_domain": {
                "terms": {
                    "field": "Target Domain",
                    "size": 100
                }
            }
        }
    }
    return q