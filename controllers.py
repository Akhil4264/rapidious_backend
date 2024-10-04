from client import *
import math
import re


PAGE_SIZE = 10


def get_all_ingredients_func():
    query = {
        "size": 0,
        "aggs": {
            "distinct_ingredients": {
                "terms": {
                    "field": "categories.keyword",
                    "size": 100000
                }
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=query)
    with open('distinct_ingredients.json', 'w') as f:
        json.dump(response, f, indent=4)

    distinct_ingredients = [bucket['key']
                            for bucket in response['aggregations']['distinct_ingredients']['buckets']]
    return distinct_ingredients


def get_relevant_ings_func(value):
    query = {
        "size": 10,
        "query": {
            "match": {
                "categories.keyword": value
            }
        }
    }
    response = client.search(index=INDEX_NAME, body=query)
    with open('rel_ind.json', 'w') as f:
        json.dump(response, f, indent=4)


def get_relevant_titles_func(value):
    terms = re.split('[,"\s]+', value)  # This regex now correctly splits on space characters as well
    print(terms)
    query = {
        "size": 10,
        "query": {
            "bool": {
                "should": [],
                "minimum_should_match": 1
            }
        }
    }
     
    for term in terms:
        query["query"]["bool"]["should"].append({"match": {"title": {"query" : term , "fuzziness": "AUTO"}}})
    response = client.search(index=INDEX_NAME, body=query)
    with open('get_titles.json','w') as f:
        json.dump(response,f,indent=4)
    titles = [hit["_source"]["title"] for hit in response["hits"]["hits"]]
    return titles


def get_min_max_field_func(field):
    query = {
        "size": 0,
        "aggs": {
            "min_calories": {
                "min": {
                    "field": field
                }
            },
            "max_calories": {
                "max": {
                    "field": field
                }
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=query)
    min_calories = response['aggregations']['min_calories']['value']
    max_calories = response['aggregations']['max_calories']['value']
    print(f"Minimum {field}: {min_calories}")
    print(f"Maximum {field}: {max_calories}")


def create_range_or_null_query_func(field_name, value_range):
    if value_range[0] == 0 and value_range[1] == 0:
        return {"bool": {"must_not": {"exists": {"field": field_name}}}}
    else:
        return {"range": {field_name: {"gte": value_range[0], "lte": value_range[1]}}}


def get_recipies_func(dish_name, ingredients, ranges_apply, min_rating, sodium_range, fat_range, calories_range, protein_range, page, sortby, order):
    query = {}
    if (ranges_apply):
        query = {
            "from": (page-1) * PAGE_SIZE,
            "size": PAGE_SIZE,
            "track_total_hits": True,
            "sort": [
                {
                    sortby: {
                        "order": order
                    }
                }
            ],
            "query": {
                "bool": {
                    "should": [],
                    "minimum_should_match" : None,
                    "filter": [
                        {
                            "range": {
                                "rating": {
                                    "gte": min_rating
                                }
                            }
                        },
                        create_range_or_null_query_func(
                            "sodium", sodium_range),
                        create_range_or_null_query_func("fat", fat_range),
                        create_range_or_null_query_func(
                            "calories", calories_range),
                        create_range_or_null_query_func(
                            "protein", protein_range)
                    ]
                }
            }
        }

    else:
        query = {
            "from": (page-1) * PAGE_SIZE,
            "size": PAGE_SIZE,
            "track_total_hits": True,
            "sort": [
                {
                    sortby: {
                        "order": order
                    }
                }
            ],
            "query": {
                "bool": {
                    "should": [],
                    "minimum_should_match": None,
                    "filter": [
                        {
                            "range": {
                                "rating": {
                                    "gte": min_rating
                                }
                            }
                        }
                    ]
                }
            }
        }

    if (ingredients and len(ingredients) > 0):
        ingredients_filter = {
            "terms_set": {
                "categories.keyword": {
                    "terms": ingredients,
                    "minimum_should_match_script": {
                        "source": str(len(ingredients))
                    }
                }
            }
        }
        query['query']['bool']['filter'].append(ingredients_filter)

    if (dish_name != ""):
        terms = re.split('[,"\s]+', dish_name) 
        for term in terms:
            query["query"]["bool"]["should"].append({"match": {"title": {"query" : term , "fuzziness": "AUTO"}}})
        # query['query']['bool']["must"].append(dish_filter)
        query["query"]["bool"]["minimum_should_match"] = 1

    response = client.search(index=INDEX_NAME, body=query)

    total_records = response["hits"]["total"]["value"]
    # return response
    return {"total_pages": math.ceil(total_records/PAGE_SIZE), "page": page, "data": response["hits"]["hits"]}


# get_relevant_titles_func("chick fhy ")
