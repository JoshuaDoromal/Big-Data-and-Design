# --- Import Libraries ---
import streamlit as st
import openai
import pandas as pd
import re
import random
import os
import fitz
import requests
import ollama
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage

# --- API Keys ---
openai.api_key = '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'
os.environ['OPENAI_API_KEY'] = "sk-proj-JjOmbe1PThun1ATUSHwNT3BlbkFJvhceXG53qqrBfy1Ap8U3"
os.environ['TAVILY_API_KEY'] = "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"

# --- Recipe Data Preprocessing ---
data = pd.read_csv('newrecipes.csv')
recipes_data = data[['recipe_name', 'ingredients', 'directions', 'url']].copy()
recipes_data.rename(columns={'recipe_name': 'Name', 'ingredients': 'Ingredients', 'directions': 'Directions', 'url': 'URL'}, inplace=True)

def clean_text(text):
    text = ' '.join(text.split())
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    return text

cleaned_recipes_data = recipes_data.copy()
cleaned_recipes_data['Ingredients'] = cleaned_recipes_data['Ingredients'].apply(clean_text)
cleaned_recipes_data['Directions'] = cleaned_recipes_data['Directions'].apply(clean_text)

# --- LangChain & OpenAI Setup ---
model = ChatOpenAI(model='gpt-4o', temperature=0.2)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly chef named Gordan Rhamsey with 20 years of experience in making recipes from ingredients."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

search = TavilySearchResults()
tools = [search]

agent = create_openai_functions_agent(llm=model, prompt=prompt, tools=tools)
agentExecutor = AgentExecutor(agent=agent, tools=tools)

# --- Functions ---

def process_chat(agentExecutor, user_input, chat_history):
    response = agentExecutor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return response["output"]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to generate response using gemma:2b model
def generate_response_gemma(prompt):
    try:
        response = ollama.generate(model='gemma:2b', prompt=prompt)
        return response['response']
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to generate response using llama2 model
def generate_response_llama(prompt):
    try:
        llm = Ollama(model="llama2")
        response = llm.invoke(prompt)
        return response
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to fetch the list of recognized ingredients from TheMealDB API
def fetch_ingredient_list():
    url = 'https://www.themealdb.com/api/json/v1/1/list.php?i=list'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['meals']
        except ValueError:
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"API request failed with status code {response.status_code}")
        return None

# Function to fetch the list of meal categories from TheMealDB API
def fetch_category_list():
    url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return [category['strCategory'] for category in response.json()['categories']]
        except ValueError:
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"API request failed with status code {response.status_code}")
        return None

# Function to fetch the list of meal areas from TheMealDB API
def fetch_area_list():
    url = 'https://www.themealdb.com/api/json/v1/1/list.php?a=list'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return [area['strArea'] for area in response.json()['meals']]
        except ValueError:
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"API request failed with status code {response.status_code}")
        return None

# Function to search recipes by category and area
def search_recipes_by_category_and_area(category, area):
    url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}&a={area}'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['meals']
        except ValueError:
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"API request failed with status code {response.status_code}")
        return None

# Function to get full details of a recipe by ID
def get_recipe_details(recipe_id):
    url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['meals'][0]
        except (ValueError, KeyError):
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"API request failed with status code {response.status_code}")
        return None

# --- Lumine Streamlit Application ---
st.set_page_config(
    page_title="Lumine",
    page_icon="🍳",
    layout="wide"
)

# --- Styling ---
st.markdown("""
<style>
/* ... your existing styles ... */
</style>
""", unsafe_allow_html=True)

st.title("Lumine: Your Culinary Companion")

tab1, tab2, tab3, tab4 = st.tabs(["Elena's Recipe Generator", "Giulia's ChefBot", "Josh Ramsay's Assistant", "A Man Deep's Recipe Mixer"])

# Elena's tab
with tab1:
    st.markdown("<h1 style='text-align: center;'>Elena's Random Food Recipe Generator</h1>", unsafe_allow_html=True)

    # User input fields
    age = st.number_input("Enter your age", min_value=18, step=1)
    height = st.number_input("Enter your height (in centimeters)", min_value=140, step=1)
    weight = st.number_input("Enter your weight (in kilograms)", min_value=35, step=1)
    fitness_goals_options = ["Weight Loss", "Muscle Gain", "Maintaining Weight"]
    selected_fitness_goal = st.selectbox("Select your fitness goal", fitness_goals_options)
    protein_preference_options = ["Vegetarian", "Chicken", "Fish", "Shrimp", "Vegan", "Pork", "Beef"]
    selected_protein_preference = st.selectbox("Select food preference", protein_preference_options)
    cuisine_type_options = ["Asian", "Italian", "Mexican", "Mediterranean"]
    cuisine_type = st.selectbox("Select preferred cuisine type", cuisine_type_options)

    dietary_restrictions_options = ["Low-carb", "Nut-free", "Vegan", "Vegetarian", "None"]
    dietary_restrictions = st.selectbox("Select dietary restrictions or preferences", dietary_restrictions_options)

    num_recipes = st.number_input("Number of recipes to generate", min_value=1, max_value=5, step=1, value=1)

    # Button to generate recipes
    if st.button("Generate Recipes"):
        recipes = []

        # Loop to generate the specified number of recipes
        for _ in range(num_recipes):
            # Constructing the prompt
            prompt = f"Generate a recipe suitable for a {age}-year-old"
            if selected_fitness_goal:
                prompt += f" with a goal of {selected_fitness_goal.lower()}"
            if height and weight:
                prompt += f", {height} cm tall, and {weight} kg in weight"
            if selected_protein_preference:
                prompt += f" that is {selected_protein_preference.lower()}"
            if cuisine_type:
                prompt += f" and has a {cuisine_type.lower()} influence"
            if dietary_restrictions != "None":
                prompt += f" while being {dietary_restrictions.lower()}"
            prompt += ". Also, provide the nutritional information."

            # API call to generate the recipe
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )

            # Extracting and storing the recipe
            recipe = response.choices[0].message.content.strip()
            recipes.append(recipe)

        # Displaying the recipes
        for idx, recipe in enumerate(recipes, start=1):
            st.markdown(f"**Recipe {idx}:** {recipe}")

# Giulia's tab
with tab2:
    st.markdown("<h1 style='text-align: center;'>Giulia's ChefBot</h1>", unsafe_allow_html=True)

    # Load dataset (replace with your dataset path)
    data = pd.read_csv('newrecipes.csv')

    # Select relevant columns and rename them
    recipes_data = data[['recipe_name', 'ingredients', 'directions', 'url']].copy()
    recipes_data.rename(columns={'recipe_name': 'Name', 'ingredients': 'Ingredients', 'directions': 'Directions', 'url': 'URL'}, inplace=True)

    def clean_text(text):
        text = ' '.join(text.split())
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = text.lower()
        return text

    cleaned_recipes_data = recipes_data.copy()
    cleaned_recipes_data['Ingredients'] = cleaned_recipes_data['Ingredients'].apply(clean_text)
    cleaned_recipes_data['Directions'] = cleaned_recipes_data['Directions'].apply(clean_text)

    def suggest_recipes(data, num=3):
        sample_recipes = data.sample(num)
        st.write("ChefBot: How about trying one of these recipes?")
        for index, row in sample_recipes.iterrows():
            recipe_info = f"**Recipe:** {row['Name']}\n\n**Ingredients:** {row['Ingredients']}\n\n**Directions:** {row['Directions']}"
            if 'URL' in row and pd.notna(row['URL']):
                recipe_info += f"\n\n**URL:** {row['URL']}"
            st.markdown(recipe_info)

    def suggest_recipes_by_ingredient(data, ingredient, num=3):
        ingredient = clean_text(ingredient)
        matching_recipes = data[data['Ingredients'].str.contains(ingredient)]
        if not matching_recipes.empty:
            sample_recipes = matching_recipes.sample(min(num, len(matching_recipes)))
            st.write(f"ChefBot: Here are some recipes that include {ingredient}:")
            for index, row in sample_recipes.iterrows():
                recipe_info = f"**Recipe:** {row['Name']}\n\n**Ingredients:** {row['Ingredients']}\n\n**Directions:** {row['Directions']}"
                if 'URL' in row and pd.notna(row['URL']):
                    recipe_info += f"\n\n**URL:** {row['URL']}"
                st.markdown(recipe_info)
        else:
            st.write(f"ChefBot: Sorry, I couldn't find any recipes with {ingredient}. How about a random suggestion?")
            suggest_recipes(data)

    def handle_input(data, user_input):
        user_input = user_input.lower().strip()
        if user_input in ['hi', 'hello']:
            st.write("ChefBot: Hi there! How can I help you today?")
        elif 'cook' in user_input or 'recipe' in user_input or 'something' in user_input:
            st.write("ChefBot: Sure! Let's get started.")
            suggest_recipes(data)
        elif 'exit' in user_input:
            st.write("ChefBot: Goodbye! Happy cooking!")
            return False
        else:
            suggest_recipes_by_ingredient(data, user_input)
        return True

    st.write("ChefBot: Hi! Let's whip up something yummy together!")
    st.write("ChefBot: How can I help you today?")

    user_input = st.text_input("Enter your request")
    if user_input:
        handle_input(cleaned_recipes_data, user_input)

# Josh's tab
with tab3:
    st.markdown("<h1 style='text-align: center;'>Chef Josh Ramsay's Assistant</h1>", unsafe_allow_html=True)

    chat_history = []

    user_input = st.text_input("You:")
    if user_input:
        if user_input.lower() == 'exit':
            st.stop()

        response = process_chat(agentExecutor, user_input, chat_history)

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        st.write(f"Chef Ramsay: {response}")

# Amandeep's tab
with tab4:
    st.markdown("<h1 style='text-align: center;'>A Man Deep's Recipe Mixer</h1>", unsafe_allow_html=True)

    # --- Chat with Chef ---

    def chatbot_tab():
        st.title("Chat with Chef 🤖")

        st.markdown("""
        This AI Chatbot is your kitchen sidekick! From researching recipes to detailed step-by-step instructions, it's got you covered. Want to explore wild food combos? Just ask! Boost your culinary game with tips on ingredients, techniques, and more. Get ready to cook up some fun! 🍳👩‍🍳🔪
        """)

        # Initialize session state to keep track of the conversation
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ""


        # Model selection
        model_choice = st.selectbox(
            "Choose a Chef:",
            ("Chef De-Code", "Chef App-etizer")
        )

        # User input with pre-written text
        default_text = "Could you suggest me a recipe with chicken, potatoes and vegetables?"
        user_input = st.text_input("Aspiring Chef:", value=default_text, key="input", on_change=lambda: st.session_state.update(user_input=st.session_state.input))

        # Generate response when the user submits input
        if st.button("Let's Cook"):
            if user_input:
                # Clear previous conversation
                st.session_state.history = []

                # Append user input to history
                st.session_state.history.append(f"Aspiring Chef: {user_input}")

                # Show loading spinner and status message
                with st.spinner("Lumine's cooking up a response... Almost ready! 🍳✨"):
                    # Generate response based on the selected model
                    if model_choice == "gemma:2b":
                        bot_response = generate_response_gemma(user_input)
                    else:
                        bot_response = generate_response_llama(user_input)

                # Append bot response to history
                st.session_state.history.append(f"Culinary Luminary: {bot_response}")

                # Clear input
                st.session_state.user_input = ""

        # Display the conversation history
        for message in st.session_state.history:
            if message.startswith("Aspiring Chef:"):
                st.write(message)
            elif message.startswith("Culinary Luminary:"):
                st.success(message)
    chatbot_tab()  # Call the chatbot function
    st.markdown("---")  # Separator

    # --- Recipe Roulette ---

    def select_filters_tab():
        st.title("Recipe Roulette 🎲")
        st.header("Feeling indecisive about your culinary cravings?")
        st.write("""
        Let's roll the dice and spice up your day with a randomly delicious dish! Choose your food category and area to surprise your taste buds today!
        """)
        # Fetch categories and areas for the filters
        with st.spinner("Fetching lumine's food categories and areas..."):
            categories = fetch_category_list()
            areas = fetch_area_list()

        selected_category = st.selectbox("Choose a food category", ["All"] + categories)
        selected_area = st.selectbox("Choose an area", ["All"] + areas)

        if st.button("Let's Spice Things Up", key="filter_get_recipes"):
            with st.spinner("Fetching Lumine's 'recipes..."):
                if selected_category != "All" or selected_area != "All":
                    recipes = search_recipes_by_category_and_area(selected_category, selected_area)
                else:
                    st.error("Pick a Food Category or Area for Recommendations.")
                    return

            if recipes:
                st.success("Recipes unlocked! Head to the Magic Recipe Mixer 🍲 for the perfect match.")

                # Find the best matching recipe
                best_recipe = recipes[0] if recipes else None
                if best_recipe:
                    st.session_state['best_recipe'] = get_recipe_details(best_recipe['idMeal'])
            else:
                st.write("Oops! No recipes found with those ingredients. Time to get creative or try a different combo!")

    select_filters_tab()  # Call the recipe filter function
    st.markdown("---")  # Separator

    # --- Magic Recipe Mixer ---

    def recipe_page():
        st.title("Magic Recipe Mixer 🍲")
        best_recipe = st.session_state.get('best_recipe')
        if best_recipe:
            st.title(best_recipe['strMeal'])
            col1, col2 = st.columns([1, 0.5])
            with col1:
                st.image(best_recipe['strMealThumb'], width=450)
            with col2:
                st.write("### Ingredients")
                ingredients = []
                for i in range(1, 21):
                    ingredient = best_recipe.get(f'strIngredient{i}')
                    measure = best_recipe.get(f'strMeasure{i}')
                    if ingredient and measure:
                        ingredients.append(f"{measure} {ingredient}")
                # Using markdown to list ingredients with bullet points
                st.markdown("\n".join([f"- {ingredient}" for ingredient in ingredients]))

            st.write("### Instructions")
            st.write(best_recipe['strInstructions'])

            st.write("### Source")
            st.write(f"[{best_recipe.get('strSource', 'No link available')}]({best_recipe.get('strSource', '#')})")
        else:
            st.write("No recipe selected! Head back to the Recipe Roulette 🎲 for some culinary inspiration.")
    recipe_page()  # Call the recipe display function







