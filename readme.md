8# RecipeGPT

#### Description:
The RecipeGPT is a Python-based application that uses prompt engineering, natural language processing and AI technologies to generate personalized recipes based on available ingredients. The application utilizes OpenAI's ChatGPT API and DALL-E to generate unique and creative recipes. My goal is to create a personalized and unique recipe based on available ingredients (ingredient name, quantity, and unit of measurement), user preferences such as meal type, region, gluten-free, nationality, etc., and also to determine if the AI should be strict or lenient in ingredient selection.

I hope that my project will be useful to cooking enthusiasts and inspire the use of AI in software development and new culinary creations.

To achieve my goal, I followed several key steps. First, I collected examples of recipes and ingredients to serve as a test base. Then, I used prompt engineering techniques and trial and error to arrive at results that can be repeated.

In terms of technical implementation, I used Python and the following libraries: OpenAI API for the natural language processing model, DALL-E for image processing, Tokenizer for text-to-token conversion to validate the token limit to use, and HTTP tool. I also used DALL-E's API to generate images of the created recipe.

Currently, my application is a console-based one, but I plan to possibly migrate it to an API with FastAPI for web-based use.

More about the Application :
Once the recipe data has been properly structured and stored in a JSON format, the next step is to use this data to generate recipe preparation instructions. To do this, we will use prompt techniques to convert the stored data into written text in the form of a conversation between the assistant and the user. Prompt templates are created in JSON and introduced into the system to enable structured conversation.

One of the NLP techniques we will use is Natural Language Generation (NLG), which involves using machine learning models to generate text in natural language similar to that of a native speaker. The output format is in JSON, which will allow it to be used via other applications in the future.

To accomplish this, we will use natural language AI models such as OpenAI's GPT-3.5 turbo and DALL-E, which have demonstrated their ability to generate realistic text and images from input data. It is possible to select another model to limit costs or to test usability. For the purposes of accuracy, GPT-3.5 turbo is selected in this demonstration. We will train this model on pre-existing recipe data, a desired request and response format, and to learn to generate recipe preparation instructions consistently and accurately.

Finally, we will integrate the API into a Python application, which will allow users to enter their recipe data in a JSON format, generate recipe preparation instructions, and physically save them in a JSON file and the image in PNG format. The application also allows for saving ingredients in memory for future use and deleting one or more ingredients.

#### Project success criteria:
We will consider the project successful if the application is capable of generating accurate and consistent recipe preparation instructions from input data, if it is easy to use and accessible to a wide audience, and if it provides a well-formatted and valid JSON output as desired.

#### Video Demo:  <https://youtu.be/ZtPvRUagBa8>

## Installation

To install the Recipe Generator Application, you can use conda to install the required dependencies from the `requirements.txt` file:
```
conda create --name recipe-generator python=3.8

conda activate recipe-generator

pip install -r requirements.txt

```
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

Step 2: Entering New Ingredients - If you choose to start from scratch, you will be prompted to enter new ingredients by typing them into the system. Exemple `Chicken-200-g`
`potatoes-500-g` 
etc.

Step 3: Submitting the Recipe - Once you have entered the ingredients, you can submit the recipe by following the prompts. The AI will generate a recipe based on the ingredients you have entered.

Step 4: Recipe Generation - The AI will generate a recipe, which will be returned in a valid JSON format and saved to a file.

Step 5: Generating an Image - A second prompt will be created to generate an image based on the recipe. The image will be saved in png format for future use.

Step 6: Accessing the Recipe Information - You will be able to access the recipe information, which includes the ingredients used for the recipe, the steps to create the recipe, a note, and the list of ingredients with remaining quantities based on the amount of ingredients used for the recipe.

Step 7: Show the json recipe and image at `c:\temp`
Exemple recipe json response from model : 
`
{'recipe_name': 'Beef, Vermicelli, and Vegetable Stir-Fry', 'dateTime_utc': '2021-12-03T14:45:00Z', 'preparation_time': 30, 'cooking_time': 20, 'total_cooking_time': 50, 'servings': 6, 'ingredients': [{'name': 'filet de boeuf', 'quantity': '500', 'unit_of_measure': 'g'}, {'name': 'vermicelle de riz', 'quantity': '400', 'unit_of_measure': 'g'}, {'name': 'citronelle', 'quantity': '2', 'unit_of_measure': 'tige'}, {'name': 'germes de soja', 'quantity': '400', 'unit_of_measure': 'g'}, {'name': 'feuilles de salade', 'quantity': '20', 'unit_of_measure': ''}, {'name': 'concombre', 'quantity': '3', 'unit_of_measure': ''}, {'name': 'oignons', 'quantity': '2', 'unit_of_measure': ''}, {'name': 'Oeufs', 'quantity': '6', 'unit_of_measure': 'unités'}, {'name': 'Farine', 'quantity': '500', 'unit_of_measure': 'grammes'}, {'name': 'Sucre', 'quantity': '250', 'unit_of_measure': 'grammes'}, {'name': 'Sel', 'quantity': '5', 'unit_of_measure': 'grammes'}, {'name': 'Beurre', 'quantity': '200', 'unit_of_measure': 'grammes'}, {'name': 'Lait', 'quantity': '1', 'unit_of_measure': 'litre'}, {'name': 'Levure chimique', 'quantity': '2', 'unit_of_measure': 'cuillères à café'}, {'name': 'Poivre noir', 'quantity': '1', 'unit_of_measure': 'pincée'}, {'name': 'Huile olive', 'quantity': '50', 'unit_of_measure': 'millilitres'}, {'name': 'Citron', 'quantity': '1', 'unit_of_measure': 'unité'}, {'name': 'apples', 'quantity': '2', 'unit_of_measure': 'pounds'}, {'name': 'chicken', 'quantity': '200', 'unit_of_measure': 'g'}, {'name': 'oignon', 'quantity': '1', 'unit_of_measure': 'g'}], 'prepSteps': ['Cook the vermicelli according to the package instructions, then drain and set aside.', 'In a bowl, whisk together the flour, salt, and baking powder. Stir in the sugar, then add the milk and eggs and whisk until smooth.', 'Heat the butter in a large skillet over medium heat. Dip apple slices into the batter, allowing any excess to drip off, then place in the skillet and cook until golden brown on both sides. Repeat with remaining apple slices.', 'In a separate skillet, heat the olive oil over medium-high heat. Add the beef and cook until browned on all sides. Remove from the skillet and set aside.', 'Add the onion and lemongrass to the skillet and cook until the onion is translucent. Add the chicken and cook until browned on all sides.', 'Add the soybean sprouts and cucumber to the skillet and cook for an additional 2-3 minutes, stirring occasionally.', 'Return the beef to the skillet and cook for an additional 2-3 minutes, stirring occasionally.', 'Serve the beef and vegetable stir-fry over the cooked vermicelli.'], 'notes': 'This recipe is gluten-free and nut-free, but cinnamon is not included. If a sweeter dish is desired, you can add a sprinkle of cinnamon to the apple slices before frying.', 'remaining_Ingredients': [{'name': 'oignon', 'quantity': '1', 'unit_of_measure': 'g'}], 'category': 'Main Course', 'keywords': ['Italian', 'beef', 'vermicelli', 'vegetables', 'stir-fry', 'gluten-free', 'nut-free']}
`

## Future modifications
- Future modifications to the application may include adding additional AI models to generate recipes, incorporating user feedback to improve recipe recommendations, and integrating with external APIs to retrieve ingredient and nutritional information.

- The system can prompt the user for feedback on the recipe, such as whether they like it, what changes they would make, and any additional ingredients they would like to include. This feedback can be used to further refine the recipe recommendation algorithm.

- Using Langchain
- Using gpt4all or other open source model
- Using the nltk (Natural Language Toolkit) library https://www.nltk.org/ for our application. 
- using FastApi to create a Python API
- Using uvicorn for the ASGI web server implementation for Python. 
- Using React to call the Python API.

