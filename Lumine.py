import streamlit as st
import requests
import pandas as pd

# =============================================================================
# Spoonacular API Configuration
# =============================================================================

# Spoonacular API key
API_KEY = '03c67b90880241ac9b7a7f936d066690'

# =============================================================================
# Function Definitions
# =============================================================================

# Function to get recipes based on user input
def get_recipes(params):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    headers = {'Content-Type': 'application/json'}
    params['apiKey'] = API_KEY
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to get recipe details
def get_recipe_details(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
        'includeNutrition': True
    }
    response = requests.get(url, params=params)
    return response.json()

# Function to get meal types
def get_meal_types():
    return ['Breakfast', 'Lunch', 'Dinner']

# Function to call Spoonacular Image Analysis API
def analyze_image(image_path, api_key):
    url = "https://api.spoonacular.com/food/images/analyze"
    files = {'file': open(image_path, 'rb')}
    params = {'apiKey': api_key}
    response = requests.post(url, files=files, params=params)
    return response.json()

# Function to get similar recipes
def get_similar_recipes(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/similar'
    params = {
        'apiKey': API_KEY,
        'number': 5  # Number of similar recipes to fetch
    }
    response = requests.get(url, params=params)
    return response.json()

# Function to save favorite recipes
def save_favorite(recipe_id):
    favorites = st.session_state.get('favorites', [])
    if recipe_id not in favorites:
        favorites.append(recipe_id)
    st.session_state['favorites'] = favorites

# Function to get favorite recipes
def get_favorites():
    favorites = st.session_state.get('favorites', [])
    favorite_recipes = []
    for recipe_id in favorites:
        recipe_details = get_recipe_details(recipe_id)
        favorite_recipes.append(recipe_details)
    return favorite_recipes

# Function to generate grocery list
def generate_grocery_list(recipes):
    grocery_list = {}
    for recipe in recipes:
        for ingredient in recipe['extendedIngredients']:
            name = ingredient['name']
            amount = ingredient['amount']
            unit = ingredient['unit']
            if name in grocery_list:
                grocery_list[name]['amount'] += amount
            else:
                grocery_list[name] = {'amount': amount, 'unit': unit}
    return grocery_list

# =============================================================================
# Streamlit Interface Setup
# =============================================================================

st.title('Recipe and Meal Planner')

# Creating tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Recipe Generator", "Classify Image", "Favorite Recipes", "Grocery List", "Meal Planner"])

with tab1:
    st.header('Select Your Preferences')

    # User input fields for recipes
    selected_ingredients = st.text_input('Enter ingredients (comma separated)', '')
    meal_types = get_meal_types()
    meal_type = st.selectbox('Meal Type', meal_types)
    max_ready_time = st.slider('Max Ready Time (minutes)', 10, 120, 30)

    # Button to generate recipes
    if st.button('Generate Recipes'):
        params = {
            'includeIngredients': selected_ingredients,
            'type': meal_type,
            'maxReadyTime': max_ready_time,
            'number': 3,  # Number of recipes to fetch
            'instructionsRequired': True,
            'addRecipeInformation': True
        }

        with st.spinner('Generating recipes...'):
            recipes = get_recipes(params)

        if recipes.get('results'):
            st.header('Recipes')
            for recipe in recipes['results']:
                recipe_details = get_recipe_details(recipe['id'])
                if 'title' in recipe_details:
                    price_per_serving_usd = recipe_details.get('pricePerServing', 0) / 100  # pricePerServing is in cents
                    st.subheader(f"{recipe_details['title']} (${price_per_serving_usd:.2f} per serving)")
                    st.write(f"*Ready in {recipe_details['readyInMinutes']} minutes. Servings: {recipe_details['servings']}*")
                    st.image(recipe_details['image'], use_column_width=True)

                    st.write("### Ingredients")
                    ingredients = "\n".join([f"- {ingredient['original']}" for ingredient in recipe_details['extendedIngredients']])
                    st.write(ingredients)

                    st.success("### Instructions")
                    instructions = "\n".join([f"{step['number']}. {step['step']}" for step in recipe_details['analyzedInstructions'][0]['steps']])
                    st.write(instructions)

                    st.write("### Nutrition Information")
                    nutrition_data = recipe_details['nutrition']['nutrients']
                    nutrition_df = pd.DataFrame(nutrition_data)[['name', 'amount', 'unit', 'percentOfDailyNeeds']]
                    nutrition_df.columns = ['Name', 'Amount per Serving', 'Unit', 'Daily Value (%)']
                    st.table(nutrition_df)

                    if st.button('Save Recipe', key=recipe['id']):
                        save_favorite(recipe['id'])

                    st.markdown(f"[View Recipe]({recipe_details['sourceUrl']})")
                else:
                    st.write("Recipe details not found.")
        else:
            st.write("No recipes found. Please adjust your preferences and try again.")

with tab2:
    st.header("Classify Image")

    # Upload image
    uploaded_file = st.file_uploader("Upload a food picture and see what happens...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Save uploaded image to a temporary file
        with open("temp_classify_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Call Spoonacular API to analyze image
        with st.spinner('Analyzing image...'):
            classify_response = analyze_image("temp_classify_image.jpg", API_KEY)

        if 'category' in classify_response:
            food_category = classify_response['category']['name']
            probability = classify_response['category']['probability']
            st.write(f"I think this is {food_category} - I'm almost certain with a probability of {probability:.2f}!")

            # Display nutrition profile
            if 'nutrition' in classify_response:
                st.write("### Nutrition profile of the average dish")
                nutrition_profile = classify_response['nutrition']
                st.write(f"{nutrition_profile['calories']['value']} calories")
                st.write(f"{nutrition_profile['fat']['value']}g fat")
                st.write(f"{nutrition_profile['protein']['value']}g protein")
                st.write(f"{nutrition_profile['carbs']['value']}g carbs")

            # Display matching recipes
            if 'recipes' in classify_response:
                st.write("Hungry now? Try one of these:")
                for recipe in classify_response['recipes']:
                    st.subheader(recipe['title'])
                    st.image(f"https://spoonacular.com/recipeImages/{recipe['id']}-312x231.{recipe['imageType']}", use_column_width=True)
                    st.markdown(f"[View Recipe]({recipe['sourceUrl']})")
        else:
            st.write("Could not classify the image. Please try another one.")

with tab3:
    st.header("Favorite Recipes")

    favorite_recipes = get_favorites()

    if favorite_recipes:
        for recipe in favorite_recipes:
            st.subheader(recipe['title'])
            st.image(recipe['image'], use_column_width=True)
            st.write(f"*Ready in {recipe['readyInMinutes']} minutes. Servings: {recipe['servings']}*")
            st.write("### Ingredients")
            ingredients = "\n".join([f"- {ingredient['original']}" for ingredient in recipe['extendedIngredients']])
            st.write(ingredients)
            st.success("### Instructions")
            instructions = "\n".join([f"{step['number']}. {step['step']}" for step in recipe['analyzedInstructions'][0]['steps']])
            st.write(instructions)
            st.markdown(f"[View Recipe]({recipe['sourceUrl']})")
    else:
        st.write("You have no favorite recipes yet.")

with tab4:
    st.header("Grocery List Generator")

    if 'favorites' in st.session_state and st.session_state['favorites']:
        favorite_recipes = get_favorites()
        grocery_list = generate_grocery_list(favorite_recipes)

        st.write("### Grocery List")
        for item, details in grocery_list.items():
            st.write(f"{item}: {details['amount']} {details['unit']}")
    else:
        st.write("You need to have favorite recipes to generate a grocery list.")

with tab5:
    st.header("Meal Planner")

    if 'favorites' in st.session_state and st.session_state['favorites']:
        favorite_recipes = get_favorites()
        days = st.number_input("Enter the number of days for meal planning", min_value=1, max_value=7, value=7)

        st.write("### Your Meal Plan")
        for day in range(1, days + 1):
            st.subheader(f"Day {day}")
            for recipe in favorite_recipes:
                st.write(f"#### {recipe['title']}")
                st.image(recipe['image'], use_column_width=True)
                st.write(f"*Ready in {recipe['readyInMinutes']} minutes. Servings: {recipe['servings']}*")
                st.write("### Ingredients")
                ingredients = "\n".join([f"- {ingredient['original']}" for ingredient in recipe['extendedIngredients']])
                st.write(ingredients)
                st.success("### Instructions")
                instructions = "\n".join([f"{step['number']}. {step['step']}" for step in recipe['analyzedInstructions'][0]['steps']])
                st.write(instructions)
                st.markdown(f"[View Recipe]({recipe['sourceUrl']})")
    else:
        st.write("You need to have favorite recipes to create a meal plan.")
