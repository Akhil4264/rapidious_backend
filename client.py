import json
from opensearchpy import OpenSearch, helpers
from dotenv import load_dotenv
load_dotenv()
import os

ADMIN = os.getenv('ADMIN')
PASSWORD = os.getenv('PASSWORD')

client = OpenSearch(
    # hosts=[{'host': 'opensearch-net', 'port': 9200}],
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=(ADMIN, PASSWORD),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

INDEX_NAME = "recipies"

def load_data():
    """Yields data from json file."""
    with open("full_format_recipes.json", "r") as f:
        data = json.load(f)
        print("Data is being ingested...")
        for recipe in data:
            yield {"_index": INDEX_NAME, "_source": recipe}


indices_info = client.cat.indices(format="json")
count = 0
count = sum(1 for entry in indices_info if entry["index"] == "recipies")
if(count > 0):
    print("data is already ingested")
else:
    data = load_data()
    print(f"Ingesting {INDEX_NAME} data")
    response = helpers.bulk(client, data)
    print(f"Data sent to your OpenSearch.")


# if __name__=="__main__":

    # response = client.indices.delete(index=INDEX_NAME)



    # with open("indices.json",'w') as f:
    #     json.dump(indices_info,f,indent=4)


    

    # fields_mapping = client.indices.get_mapping(INDEX_NAME)
    # with open("mappings.json",'w') as f:
    #     json.dump(fields_mapping,f,indent=4)








