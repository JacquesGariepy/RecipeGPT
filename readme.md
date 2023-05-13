# Recipe Generator Application

The Recipe Generator Application is a Python-based application that uses natural language processing and AI technologies to generate personalized recipes based on available ingredients. The application utilizes OpenAI's ChatGPT API and DALL-E to generate unique and creative recipes. 

## Installation

To install the Recipe Generator Application, you can use conda to install the required dependencies from the `requirements.txt` file:

conda create --name recipe-generator python=3.8
conda activate recipe-generator
pip install -r requirements.txt

## OpenAI
### To create an OpenAI API key, follow these steps:

1- Go to the OpenAI website and create an account if you don't already have one https://beta.openai.com/signup/..
2- Navigate to the API Keys page of your account and create a new secret key https://beta.openai.com/dashboard/api-credentials.
3- Copy the value of the secret key and save it somewhere you can retrieve it later.
4- To assign the OpenAI API key to a persistent environment variable, you can follow one of these methods:

### To add your OpenAI API key to the secret.json file:

Locate the `secret.json` file in the root 
Open the file in a text editor.
Replace the placeholder text `<yourkey>` with your OpenAI API key.
Save the file.
Note: Make sure to keep the secret.json file safe and do not share it with anyone.

## Usage

To use the Recipe Generator Application, simply run the `recipe_manager_ai.py` script with your desired ingredients as arguments:

`python recipe_manager_ai.py`

### Configuration
By default, PNG images and the recipe result in JSON format are created in the 'c:\temp' directory. Please modify the path in the 'configs.json' file at the root of the application. It is also possible to configure other properties, such as the name of the model used, the maximum length of tokens, the temperature of the AI, etc.

### Database
The database is simply a set of JSON files serving as a cache for the system. The saved queries, responses, and used ingredients are kept in memory and stored in the JSON files in the 'db' directory.

### Steps

Step 1: Accessing the System - Start by accessing the system and choose whether to start the experience from scratch or use the ingredients already present.

Step 2: Entering New Ingredients - If you choose to start from scratch, you will be prompted to enter new ingredients by typing them into the system. Exemple Chicken-200-g, potatoes-500-g, etc.

Step 3: Submitting the Recipe - Once you have entered the ingredients, you can submit the recipe by following the prompts. The AI will generate a recipe based on the ingredients you have entered.

Step 4: Recipe Generation - The AI will generate a recipe, which will be returned in a valid JSON format and saved to a file.

Step 5: Generating an Image - A second prompt will be created to generate an image based on the recipe. The image will be saved in png format for future use.

Step 6: Accessing the Recipe Information - You will be able to access the recipe information, which includes the ingredients used for the recipe, the steps to create the recipe, a note, and the list of ingredients with remaining quantities based on the amount of ingredients used for the recipe.

Step 7: 

## Future modifications
Future modifications to the application may include adding additional AI models to generate recipes, incorporating user feedback to improve recipe recommendations, and integrating with external APIs to retrieve ingredient and nutritional information.

The system can prompt the user for feedback on the recipe, such as whether they like it, what changes they would make, and any additional ingredients they would like to include. This feedback can be used to further refine the recipe recommendation algorithm.

Using Langchain
Using gpt4all or other open source model
Using the nltk (Natural Language Toolkit) library https://www.nltk.org/ for our application. 
using FastApi to create a Python API
using uvicorn for the ASGI web server implementation for Python. 
Using React to call the Python API.

