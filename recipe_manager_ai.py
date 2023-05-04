
import json
import os
import openai
import tiktoken

# Set tiktoken encoding
enc = tiktoken.get_encoding("cl100k_base")

# Load credentials from secrets.json file
with open('secrets.json') as f:
    credentials = json.load(f)

# Define the directory where prompts will be stored
dir_prompt = './prompts'

# Define the order in which prompts will be loaded
prompt_load_order = ['prompt_role',
                     'prompt_environment',
                     'prompt_input_output_format',
                     'prompt_query']

# Define the recipe_manager class
class recipe_manager_ai:
    def __init__(self, credentials):
        # Set OpenAI API key
        openai.api_key = credentials["RecipeManager"]["OPENAI_KEY"]
        
        # Initialize list of ingredients
        self.ingredient_list = []
        
        # Set credentials
        self.credentials = credentials
        
        # Initialize messages list
        self.messages = []
        
        # Set maximum token length
        self.max_token_length = 8000
        
        # Set maximum completion length
        self.max_completion_length = 2000
        
        # Set temperature for text generation
        self.temperature = 0.8
        
        # Set number of completions to generate
        self.n=1
        
        # Set top p value for text generation
        self.top_p = 1
        
        # Set frequency penalty for text generation
        self.frequency_penalty = 0
        
        # Set presence penalty for text generation
        self.presence_penalty = 0
        
        # Set stop token for text generation
        self.stop = ""
        
        # Set streaming mode to False
        self.stream = False
        
        # Set number of best completions to return
        self.best_of = 1
        
        # Set logprobs to 0
        self.logprobs = 0
        
        # Set echo mode to False
        self.echo = False
        
        # Set model to use for text generation
        self.model = "text-ada-001" #"text-davinci-003"

    def run(self):
        """
        Run the recipe manager.
        """
        # Ask the user if they want to delete the list of ingredients from memory
        response = input("Do you want to delete the list of ingredients from memory? Enter 1 if you want to delete, otherwise leave it blank.")
        
        # If the user wants to delete the list of ingredients, call the delete_ingredients_to_local_memory function
        if response == "1":
            delete_ingredients_to_local_memory()
        while True:
            try:
                # Define valid responses
                valid_responses = {'': 'add_item', '1': 'add_item', '2': 'submit_recipe', '3': 'remove_item', '4': 'remove_all'}

                # Ask the user if they want to continue or submit the recipe
                response = input("Do you want to continue? (1: Yes, 2: Submit Recipe, 3: Remove an item from the list, 4: Remove all items from the list)")

                # Validate response input
                if response not in ['', '1', '2', '3', '4']:
                    raise Exception("Invalid input. Please enter '' or '1, 2, 3, 4'.")
                instructions = ""
                # Process response
                if response in valid_responses:
                    action = valid_responses[response]
                    if action == 'add_item':
                        # Ask the user to enter the name, quantity, and unit of measurement for the item
                        new_ingredient = input("Enter the name, quantity, and unit of measurement for the item (e.g. apples-2-pounds): ")
                        
                        # Validate the format of the input string
                        if verify_format(new_ingredient):
                            # Create a JSON item from the input string
                            json_ingredient = create_ingredient_json(new_ingredient)
                            # Check if the item is already in the list
                            if not has_ingredient(json_ingredient):
                                # Save the JSON item in local memory
                                save_ingredient_to_local_memory(json_ingredient)
                            else:
                                raise Exception("Item already in list")
                        else:
                            raise Exception("Invalid item format")        
                        continue
                    elif action == 'remove_item':
                        item_name = input("Enter the name of the item you want to remove: ")
                        delete_ingredient_to_local_memory(item_name)
                        continue
                    elif action == 'remove_all':
                        delete_ingredients_to_local_memory()
                        continue
                    elif action == 'submit_recipe':
                        instructions = input("Please provide the necessary instruction for the recipe, such as the type of dish, the region, allergies, cooking time, number of servings, and any ingredients to avoid. For example: type of dessert, Italian cuisine, gluten-free, nut allergy, no cinnamon, 6 servings, preparation time of no more than 60 minutes, microwave cooking. Leave blank if there are no instructions.")
                
                        is_strict_ingredients = 'yes'
                        while is_strict_ingredients not in ['yes', 'no']:
                            is_strict_ingredients = input("Should the ingredients be strict? Please enter 'yes' or 'no': ").lower()
                            if not is_strict_ingredients == 'yes' or not is_strict_ingredients == 'no':
                                raise Exception("Invalid input. Please enter 'yes' or 'no'.")
                        
                        # Create a recipe prompt using the input from the request question and the ingridient in ingredient list
                        recipe_prompt = create_recipe_prompt(self, get_ingredient_list(), instructions, is_strict_ingredients)

                        # Save the request to the database
                        save_request_to_db(recipe_prompt)

                        # Send the request to the server
                        response = create_recipe_from_ai(recipe_prompt)
                        
                        # Create an image prompt using the recipe
                        image_prompt = create_image_prompt(response)

                        # Check if the JSON response is valid
                        if is_json_valid(response):
                            # Save the response to the database
                            save_response_to_db(response)

                            # Send the response to the user
                            send_response_to_user(response)
                        else:
                            raise Exception("Invalid JSON response from server")
                    else:
                        raise Exception("Invalid response. Please leave it blank or '1', '2', '3', or '4'.") 
            except Exception as e:
                print(f"Error: {e}")
                continue

def has_ingredient(ingredient):
    """
    Check if an ingredient is already in the ingredient list.
    
    Args:
        ingredient (str or dict): The ingredient to check. If provided as a string, it will be parsed
                                  as JSON. If provided as a dictionary, it will be used as-is.
    
    Returns:
        bool: True if the ingredient is already in the list, False otherwise.
    """
    
    # Check if the item is already in the list
    if isinstance(ingredient, str):
        _item = json.loads(ingredient)
    elif isinstance(ingredient, dict):
        _item = ingredient
    else:
        return False
        
    ingredient_list = get_ingredient_list()
    for tmp_item in ingredient_list:
        tmp_item = json.loads(tmp_item)
        if _item["name"] == tmp_item["name"]:
            return True
    return False


def verify_format(item):
    """
    Verify if the item format is valid.
    
    Args:
        item (str): The item to be verified.
        
    Returns:
        bool: True if the item format is valid, False otherwise.
    """

    # Verify if the item format is valid
    item_info = item.split("-")
    if len(item_info) == 3:
        try:
            float(item_info[1])
            return True
        except:
            return False
    else:
        return False
    
def create_ingredient_json(item):
    """
    Create a JSON item from the input string.

    Args:
        item (str): The item to be converted to JSON.

    Returns:
        str: The JSON item.
    """
    
    # Create a JSON item from the input string
    item_info = item.split("-")
    if len(item_info) >= 3:
        item_dict = {"name": item_info[0], "quantity": item_info[1], "unit_of_measure": item_info[2]}
    else:
        # Handle the error here, for example by setting item_dict to None or raising an exception
        raise Exception("Invalid item format")
    
    # Convert the item dictionary to a JSON string
    json_item = json.dumps(item_dict)
    return json_item

def save_ingredient_to_local_memory(json_item):
    """
    Save an ingredient to local memory.

    Args:
        json_item (str): The ingredient to be saved to local memory.

    Returns:
        None
    """

    # Load the list of ingredients from local memory
    ingredient_list = get_ingredient_list()

    # Append the new ingredient to the list
    ingredient_list.append(json_item)

    # Save the updated list back to local memory
    with open("items.json", "w") as f:
        json.dump(ingredient_list, f)

def delete_ingredients_to_local_memory():
    """
    Delete all ingredients in local memory.

    Args:
        None

    Returns:
        None
    """

    # Delete all items from the list in local memory
    with open("items.json", "w") as f:
        json.dump([], f)

def delete_ingredient_to_local_memory(item_name):
    """
    Delete an ingredient in local memory.

    Args:
        item_name (str): The ingredient to be deleted in local memory.

    Returns:
        None
    """

    # Load the list of items from local memory
    ingredient_list = get_ingredient_list()

    # Remove the item with the specified name from the list
    for item in ingredient_list:
        item = json.loads(item)
        if item["name"] == item_name:
            ingredient_list.remove(item)
    # Save the updated list back to local memory
    with open("items.json", "w") as f:
        json.dump(ingredient_list, f)

def create_recipe_prompt(self, ingredient_list, instruction, is_strict_ingredients):
    """
    Create a recipe prompt using the input from the request question and the ingridient in ingredient list.

    Args:
        ingredient_list (list): The list of ingredients.
        instruction (str): The instruction for the recipe.
        is_strict_ingredients (bool): Whether to use the ingredients in the ingredient list or not.
        
    Returns:
        str: The recipe prompt.
    """

    prompt = ""
    
    # load the prompt files in the specified order
    prompt_loading(prompt)

    # add instruction and is_strict_ingredients to the prompt
    ingredients_prompt = f'{{\n"instruction": "{instruction}"\n}}'
    ingredients_prompt += f'{{\n"is_strict_ingredients": "{is_strict_ingredients}"\n}}'
    
    for item in ingredient_list:
        item = json.loads(item)
        ingredients_prompt += f'{{\n  "name": "{item["name"]}",\n  "quantity": "{item["quantity"]}",\n  "unit_of_measure": "{item["unit_of_measure"]}"\n}}'
    
    # Replace the placeholder in the prompt with the ingredients
    # Add the start and end prompt
    prompt = f"\n<|im_start|>{prompt.replace('[INSTRUCTION]', ingredients_prompt)}\n<|im_end|>"

    if check_if_prompt_is_too_long(self, prompt):
        # find how to truncate the prompt - next version
        return ""

    print(prompt)

    return prompt

def prompt_loading(prompt):
    """
    Load the prompt files in the specified order.

    Args:
        None

    Returns:
        None
    """

    for prompt_name in prompt_load_order:
        fp_prompt = os.path.join(dir_prompt, prompt_name + '.txt')
        with open(fp_prompt) as f:
            prompt += f"{f.read()}"

def check_if_prompt_is_too_long(self, prompt):
    """
    Truncate the prompt if it's too long.

    Args:
        None

    Returns:
        None
    """
    #Encodes a string into tokens.
    tokens = enc.encode(prompt)
    if len(tokens) > self.max_token_length - \
                self.max_completion_length:
            print('Prompt too long. truncated.')
            # truncate the prompt by removing the oldest two messages
            self.messages = self.messages[2:]
            return True
    return False

def create_image_prompt(recipe_prompt):
    """
    Create an image prompt using the input from the recipe prompt.

    Args:
        recipe_prompt (str): The recipe prompt to be used in the image prompt.

    Returns:
        str: The image prompt.
    """ 

    # Create an image prompt
    image_prompt = f"Please take a picture of the following recipe:\n\n{recipe_prompt}"
    return image_prompt

def save_request_to_db(request_question, recipe_prompt):
    """
    Create a JSON object for the request and save it to the database.
    
    Args:
        request_question (str): The question of the request.
        recipe_prompt (str): The recipe prompt of the request.

    Returns:
        dict: The request.
    """

    # Create a JSON object for the request and save it to the database
    ingredient_list = get_ingredient_list()
    request = {"question": request_question, "ingredient_list" : ingredient_list,  "recipe_prompt": recipe_prompt}
    with open("requests.json", "a") as f:
        f.write(json.dumps(request) + "\n")
    return request

def create_recipe_from_ai(self, request):
    """
    Create a recipe using the AI.

    Args:
        request (dict): The request to be used in the recipe.

    Returns:
        dict: The response from the AI.
    """

    # Generate a recipe using the AI
    response = openai.Completion.create(
            model = self.model,
            prompt=request,
            temperature=self.temperature,
            max_tokens=self.max_completion_length,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            n=self.n,
            stream=self.stream,
            best_of = self.best_of,
            logprobs=self.logprobs,
            echo=self.echo,
            stop=["<|im_end|>"])
    return response

def generate_recipe_image(request):
    """
    Generate a recipe image using the AI.

    Args:
        request (dict): The request to be used in the recipe image.

    Returns:
        dict: The response from the AI.
    """

    # TODO: Implement this function to send the request and image prompt to the server
    pass

def get_response():
    """
    Get the latest response from the database.

    Args:
        None

    Returns:
        dict: The latest response from the database.
    """

    # Load the list of responses from the database
    with open("responses.json", "r") as f:
        response_list = f.readlines()

    # Return the latest response
    return json.loads(response_list[-1])

def is_json_valid(json_string):
    """
    Check if a JSON string is valid.

    Args:
        json_string (str): The JSON string to be checked.

    Returns:
        bool: True if the JSON string is valid, False otherwise.
    """

    # Check if the JSON string is valid
    try:
        json.loads(json_string)
        return True
    except:
        return False

def save_response_to_db(response):
    """
    Save a response to the database.

    Args:
        response (dict): The response to be saved.

    Returns:
        None
    """
    # Save the response to the database
    with open("responses.json", "a") as f:
        f.write(json.dumps(response) + "\n")

def send_response_to_user(response):
    """
    Send a response to the user.
    
    Args:
        response (dict): The response to be sent.

    Returns:
        None
    """
    # Print the response to the user
    print(response["text"])

def get_ingredient_list():
    """
    Get the list of ingredients from local memory.

    Args:
        None

    Returns:    
        list: The list of ingredients.
    """

    # Read the items from local memory
    try:
        with open("items.json", "r") as f:
            ingredient_list = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist yet, return an empty list
        ingredient_list = []
    return ingredient_list

# Create an instance of RecipeManager
recipe_manager_ai = recipe_manager_ai(credentials)

# Run the application
recipe_manager_ai.run()