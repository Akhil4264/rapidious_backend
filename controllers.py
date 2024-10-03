from client import *
import math

PAGE_SIZE = 10


def get_all_ingredients_func():
    query = {
        "size": 0,  # We are only interested in the aggregation result
        "aggs": {
            "distinct_ingredients": {
                "terms": {
                    "field": "categories.keyword",  # Use .keyword for exact matching of strings
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


def get_relevant_titles_func(value):
    query = {
        "size": 10,
        "query": {
            "match": {
                "title": value
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=query)
    # with open('distinct_ingredients.json', 'w') as f:
    #     json.dump(response, f, indent=4)
    with open('getTitles.json', 'w') as f:
        json.dump(response, f, indent=4)

    return response["hits"]["hits"]

    # distinct_ingredients = [
    #     bucket['key'] for bucket in response['aggregations']['distinct_ingredients']['buckets']
    #     if value.lower() in bucket['key'].lower()
    # ][:10]
    # return distinct_ingredients


def get_min_max_field_func(field):
    query = {
        "size": 0,  # No need for actual documents, just aggregations
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

    # Execute the search query
    response = client.search(index=INDEX_NAME, body=query)

    # Extract min and max values from the response
    min_calories = response['aggregations']['min_calories']['value']
    max_calories = response['aggregations']['max_calories']['value']

    # Display the results
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
                    "must": [],
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
                    "fat": {
                        "order": "desc"  
                    }
                }
            ],
            "query": {
                "bool": {
                    "must": [],
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
        dish_filter = {
            "match": {
                "title": dish_name
            }
        }
        query['query']['bool']["must"].append(dish_filter)

    # query = {
    #         "from": page*PAGE_SIZE,
    #         "size": PAGE_SIZE,
    #         "track_total_hits": True,
    #         "query": {
    #             "bool": {
    #                 "must": [
    #                     {"match": {"title": dish_name}},
    #                     {"range": {"rating": {"gte": min_rating}}},
    #                     {"terms_set": {
    #                         "categories.keyword": {
    #                             "terms": ingredients,
    #                             "minimum_should_match_script": {
    #                                 "source": str(len(ingredients))
    #                             }
    #                         }
    #                     }},
    #                 ]
    #                 + [
    #                     create_range_or_null_query_func(
    #                         "sodium", sodium_range),
    #                     create_range_or_null_query_func("fat", fat_range),
    #                     create_range_or_null_query_func(
    #                         "calories", calories_range),
    #                     create_range_or_null_query_func(
    #                         "protein", protein_range)
    #                 ],
    #             }
    #         }
    #     }

    response = client.search(index=INDEX_NAME, body=query)

    total_records = response["hits"]["total"]["value"]

    with open("get_recipies.json", 'w') as f:
        json.dump(response, f, indent=4)

        # print(total_records)
    return {"total_pages": math.ceil(total_records/PAGE_SIZE), "page": page, "data": response["hits"]["hits"]}

    # Print the results
    # with open('get_recipies.json', 'w') as f:
    #         json.dump(response, f, indent=4)
    # print(len(response["hits"]["hits"]))


# get_recipies_func()
