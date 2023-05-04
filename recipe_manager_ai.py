
import json
import os
import re
import openai
import tiktoken

# Set tiktoken encoding
enc = tiktoken.get_encoding("cl100k_base")

# Load credentials from secrets.json file
with open('secrets.json', 'r') as f:
    credentials = json.load(f)

# Load credentials from configs.json file
with open('configs.json', 'r') as f:
    configs = json.load(f)
# Define the directory where prompts will be stored
dir_prompt = './prompts'

# Define the order in which prompts will be loaded
prompt_load_order = ['prompt_role',
                     'prompt_environment',
                     'prompt_input_output_format',
                     'prompt_query']


# Define the recipe_manager class
class recipe_manager_ai:
    def __init__(self, credentials, configs):
        # Set OpenAI API key
        openai.api_key = credentials["recipe_manager_ai"]["openai_api_key"]
        
        # Initialize list of ingredients
        self.ingredient_list = []
        
        # Set credentials
        self.credentials = credentials
        
        # Initialize messages list
        self.messages = []
        
        # get chat completion parameters in configs.json file
        chat_completion = configs['configs']['recipe_manager_ai']['chat_completion']
        # Set maximum token length
        self.chat_completion_max_token_length = chat_completion['max_token_length']
        
        # Set maximum completion length
        self.chat_completion_max_completion_length = chat_completion["max_completion_length"]
        
        # Set temperature for text generation
        self.chat_completion_temperature = chat_completion["temperature"]
        
        # Set number of completions to generate
        self.chat_completion_n= chat_completion["n"]
        
        # Set top p value for text generation
        self.chat_completion_top_p = chat_completion["top_p"]
        
        # Set frequency penalty for text generation
        self.chat_completion_frequency_penalty = chat_completion["frequency_penalty"]
        
        # Set presence penalty for text generation
        self.chat_completion_presence_penalty = chat_completion["presence_penalty"]
        
        # Set stop token for text generation
        self.chat_completion_stop = chat_completion["stop"]
        
        # Set streaming mode to False
        self.chat_completion_stream = chat_completion["stream"]
        
        # Set number of best completions to return
        self.chat_completion_best_of = chat_completion["best_of"]
        
        # Set logprobs to 0
        self.chat_completion_logprobs = chat_completion["logprobs"]
        
        # Set echo mode to False
        self.chat_completion_echo = chat_completion["echo"]
        
        # Set model to use for text generation
        self.chat_completion_model = chat_completion["model"]

        image_generation = configs['configs']['recipe_manager_ai']['image_generation']
        self.image_generation_n = image_generation["n"]
        self.image_generation_size = image_generation["size"]

    def run(self):
        """
        Run the recipe manager.
        """
        # Ask the user if they want to delete the list of ingredients from memory
        response = input("Do you want to delete the list of ingredients from memory? Enter 1 if you want to delete, otherwise leave it blank.: ")
        
        # If the user wants to delete the list of ingredients, call the delete_ingredients_to_local_memory function
        if response == "1":
            delete_ingredients_to_local_memory()
        while True:
            try:
                # Define valid responses
                valid_responses = {'': 'add_item', '1': 'add_item', '2': 'submit_recipe', '3': 'remove_item', '4': 'remove_all'}

                # Ask the user if they want to continue or submit the recipe
                response = input("Do you want to continue? (1: Yes, 2: Submit Recipe, 3: Remove an item from the list, 4: Remove all items from the list): ")

                # Validate response input
                if response not in ['', '1', '2', '3', '4']:
                    raise Exception("Invalid input. Please enter '' or '1, 2, 3, 4'.: ")
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
                        instructions = input("Please provide the necessary instruction for the recipe, such as the type of dish, the region, allergies, cooking time, number of servings, and any ingredients to avoid. For example: type of dessert, Italian cuisine, gluten-free, nut allergy, no cinnamon, 6 servings, preparation time of no more than 60 minutes, microwave cooking. Leave blank if there are no instructions.: ")
                
                        is_strict_ingredients = 'yes'
                        while is_strict_ingredients not in ['yes', 'no']:
                            is_strict_ingredients = input("Should the ingredients be strict? Please enter 'yes' or 'no': ").lower()
                            if not is_strict_ingredients == 'yes' or not is_strict_ingredients == 'no':
                                raise Exception("Invalid input. Please enter 'yes' or 'no'.: ")
                        
                        # Create a recipe prompt using the input from the request question and the ingridient in ingredient list
                        recipe_prompt_message = create_recipe_prompt(self, get_ingredient_list(), instructions, is_strict_ingredients)

                        # Save the request to the database
                        save_request_to_db(recipe_prompt_message)

                        # Send the request to the server
                        response = create_recipe_from_ai(self,recipe_prompt_message)
                        
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

def create_recipe_prompt(self, ingredient_list, instructions, is_strict_ingredients):
    """
    Create a recipe prompt using the input from the request question and the ingridient in ingredient list.

    Args:
        ingredient_list (list): The list of ingredients.
        instruction (str): The instruction for the recipe.
        is_strict_ingredients (bool): Whether to use the ingredients in the ingredient list or not.
        
    Returns:
        str: The recipe prompt.
    """
    
    # load the prompt files in the specified order
    prompt = prompt_loading()
    # add instruction and is_strict_ingredients to the prompt
    ingredients_prompt = f'{{"instruction":"{instructions}",'
    ingredients_prompt += f'"is_strict_ingredients":"{is_strict_ingredients}",'
    temp_ingredients = ""
    i = 0
    for item in ingredient_list:
        item = json.loads(item)
        if i != 0:
            temp_ingredients += ","
        temp_ingredients += f'{{"name":"{item["name"]}","quantity":"{item["quantity"]}","unit_of_measure":"{item["unit_of_measure"]}"}}'
        i+=1
    ingredients_prompt += f'"ingredients":[{temp_ingredients}]}}'

    if not is_json_valid(ingredients_prompt):
        print(ingredients_prompt)
        print("Invalid JSON format")
        return ""



    # for item in ingredient_list:
    #     item = json.loads(item)
    #     ingredients_prompt += f'\n"name":"{item["name"]}",\n"quantity":"{item["quantity"]}",\n"unit_of_measure":"{item["unit_of_measure"]}",\n'
    print(ingredients_prompt)
    # Replace the placeholder in the prompt with the ingredients
    # Add the start and end prompt

    prompt = prompt.replace(f"[ingredients_prompt]", f"[{ingredients_prompt}]")

    if check_if_prompt_is_too_long(self, prompt):
        # find how to truncate the prompt - next version
        return ""

    print(prompt)

    # Define regular expressions to match the tags and their corresponding messages
    # system_pattern = re.compile(r'\[system\]\s*(.+?)\s*(?=\[|$)')
    # user_pattern = re.compile(r'\[user\]\s*(.+?)\s*(?=\[|$)')
    # assistant_pattern = re.compile(r'\[assistant\]\s*(.+?)\s*(?=\[|$)')
    # system_pattern = re.compile(r'\[system\](.*?)\[')
    # user_pattern = re.compile(r'\[user\](.*?)\[')
    # assistant_pattern = re.compile(r'\[assistant\](.*?)\[')
    
    system_pattern = re.compile(r'\[system\]\s*(.+?)\s*(?=\[|$)')
    user_pattern = re.compile(r'\[user\]\s*(.+?)\s*(?=\[|$)')
    assistant_pattern = re.compile(r'\[assistant\]\s*(.+?)\s*(?=\[|$)')

    # Find all matches for the patterns in the string
    system_matches = system_pattern.findall(prompt)
    user_matches = user_pattern.findall(prompt)
    assistant_matches = assistant_pattern.findall(prompt)

    # Create a list of message dictionaries with the role and content for each message
    messages = []
    for message in system_matches:
        messages.append({'role': 'system', 'content': message})
    for message in user_matches:
        messages.append({'role': 'user', 'content': message})
    for message in assistant_matches:
        messages.append({'role': 'assistant', 'content': message})

    # Create a JSON object with the messages list
    json_string = json.dumps(messages, indent=2)

    print(json_string)

    return messages

def prompt_loading():
    """
    Load the prompt files in the specified order.

    Args:
        None

    Returns:
        None
    """
    prompt = ""
    for prompt_name in prompt_load_order:
        fp_prompt = os.path.join(dir_prompt, prompt_name + '.txt')
        with open(fp_prompt) as f:
            prompt += f"{f.read()}"
            prompt += "\n\n"
    return prompt

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
    if len(tokens) > self.chat_completion_max_token_length - \
                self.chat_completion_max_completion_length:
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

def save_request_to_db(recipe_prompt):
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
    request = {"recipe_prompt": recipe_prompt}
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
    response = openai.ChatCompletion.create(
            model = self.chat_completion_model,
            messages=[request],
            temperature=self.chat_completion_temperature,
            max_tokens=self.chat_completion_max_completion_length,
            top_p=self.chat_completion_top_p,
            frequency_penalty=self.chat_completion_frequency_penalty,
            presence_penalty=self.chat_completion_presence_penalty,
            n=self.chat_completion_n,
            stream=self.chat_completion_stream,
            best_of = self.chat_completion_best_of,
            logprobs=self.chat_completion_logprobs,
            echo=self.chat_completion_echo)
    return response

def generate_recipe_image(self,response):
    """
    Generate a recipe image using the AI.

    Args:
        request (dict): The request to be used in the recipe image.

    Returns:
        dict: The response from the AI.
    """
    image_url = ""
    # response = openai.Image.create(
    #     prompt=response,
    #     n=self.image_generation_n,
    #     size=self.image_generation_size
    # )
    # image_url = response['data'][0]['url']
    return image_url

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
recipe_manager_ai = recipe_manager_ai(credentials, configs)

# Run the application
recipe_manager_ai.run()