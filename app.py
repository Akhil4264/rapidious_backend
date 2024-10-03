from flask import Flask, request, jsonify
from flask_cors import CORS
from controllers import *

app = Flask(__name__)
CORS(app)

@app.route('/get_all_ingredients', methods=['GET'])
def get_all_ingredients():
     return jsonify({
        "status": "success",
        "ingredients": get_all_ingredients_func()
    })


@app.route('/get_relevant_titles', methods=['GET'])
def get_relevant_titles():
    value = request.args.get('value', '')    
    return jsonify({
        "status": "success",
        "value" : value,
        "ingredients": get_relevant_titles_func(value)
    })


@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()  # Get JSON data from the request body
    dish_name = data.get('dish_name', '')
    ingredients = data.get('ingredients', [])
    ranges_apply = data.get('ranges_apply', False)
    min_rating = data.get('min_rating', 0)
    sodium_range = data.get('sodium_range', [0, 0])
    fat_range = data.get('fat_range', [0, 0])
    calories_range = data.get('calories_range', [0, 0])
    protein_range = data.get('protein_range', [0, 0])
    page = data.get('page', 1)
    sortby = data.get('sortby', '_score')
    order = data.get('order', "desc")

    print(type(ingredients))
    print(ingredients)

    # Implement logic to fetch recipes based on the provided data
    # For demonstration, this is a mock return structure
    # recipes = [{
    #     "title": "Tomato and Lettuce Salad",
    #     "ingredients": ["tomato", "lettuce", "olive oil"],
    #     "rating": 4.5
    # }] if dish_name else []
    fetched_data = {
        "dish_name": dish_name,
        "ingredients": ingredients,
        "ranges_apply": ranges_apply,
        "min_rating": min_rating,
        "sodium_range": sodium_range,
        "fat_range": fat_range,
        "calories_range": calories_range,
        "protein_range": protein_range,
        "sorted": sorted,
        "page": page,
        "sortby": sortby,
        "order": order
    }

    # print(fetched_data)

    return jsonify({
        "status": "success",
        "data" : get_recipies_func(dish_name,ingredients,ranges_apply,min_rating,sodium_range,fat_range,calories_range,protein_range,page,sortby,order)
        # "recipes": recipes

    })


@app.route('/', methods=['GET'])
def base():
    return "server running successfully"


if __name__ == '__main__':
    app.run(debug=True,port=80)
