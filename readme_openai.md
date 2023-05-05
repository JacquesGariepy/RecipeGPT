use anaconda
conda install requirements.txt

Create OpenAI key : https://platform.openai.com/account/api-keys

Allez sur le site web d'OpenAI et créez un compte si vous n'en avez pas déjà un.
Allez à la page des clés API de votre compte et créez une nouvelle clé secrète.
Copiez la valeur de la clé secrète et enregistrez-la quelque part où vous pourrez la récupérer plus tard.
Pour assigner la clé API OpenAI à une variable d'environnement persistante, vous pouvez suivre l'une de ces méthodes :

Option 1: Définir la variable d'environnement via la ligne de commande sur Windows

Ouvrez l'invite de commande Windows
Tapez la commande suivante en remplaçant <yourkey> par votre clé secrète:
    setx OPENAI_API_KEY "<yourkey>"

To use ChatGPT, you will need to obtain API credentials from OpenAI. Here are the steps to obtain your API key:

Sign up for an OpenAI account at https://beta.openai.com/signup/.
Once you have signed up, go to the API dashboard at https://beta.openai.com/dashboard/api-credentials.
Click on the "Create new API key" button to generate a new API key.
Copy the API key and keep it in a safe place.
To use your API key in your Python code, you can create a file called .env in your project directory and add the following line:
    OPENAI_API_KEY=your_api_key_here


utilisation de la librairie, nltk (Natural Language Toolkit)
 https://www.nltk.org/
