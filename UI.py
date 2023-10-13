import streamlit as st
import openai
import re
import random
import requests

openai.api_key = st.secrets["openaikey"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
huggingface_api = st.secrets["huggingfacekey"]
headers = {f"Authorization": "Bearer {huggingface_api}"}
           

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def extract_list(s):
    # The regex pattern for a list in a string
    pattern = r'\[.*?\]'
    list_str = re.search(pattern, s)
    if list_str is not None:
        return eval(list_str.group())
    return []

@st.cache_data(show_spinner=False)  # cache the function results and hide spinner
def random_list():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "génère une liste python contenant 10 noms communs au pluriel, avec un adjectif, si possible assez random. le format est une liste python"}
        ])
    response_txt = response.choices[0].message['content']
    start_index = response_txt.find('[')
    end_index = response_txt.find(']')
    list_string = response_txt[start_index:end_index+1]
    python_list = eval(list_string.lower())
    return python_list    


def gpt3(prompt,ministre_choice):
    system_prompt = f"tu es le {ministre_choice} et tu vas annoncer de nouvelles taxes. \
             Fais des variations de style et de forme en t'inspirant de discours légendaires de grandes politiciens ou figures historiques comme obama, martin luther king, ou churchill \
             Pour chaque demande, tu dois répondre comme un politicien qui annonce qu'il va taxer  [nom commun]. \
            [nom commun], je voudrais que tu places un nom commun au hasard en rapport avec la compétence du {ministre_choice}. \
            Par exemple, le ministre des chaussettes trouées prend en charge le tiroirs à chaussettes, le ministre des cailloux mouillés prend en charge la pluie qui mouille les cailloux, le ministre des oeufs durs prend en charge les plumes de poule, etc... \
            \
            Cette liste doit être modifiée! tu dois chercher d'autres mots! je ne veux surtout pas voir les exemples proposés dans tes réponses \
            Tu dois répondre sur un ton de discours politique populaire, rassurant sur l'avenir de la région et sur ta capacité à prendre les meilleures décisions.\
            mais de manière exagérée , pédante, et si possible, condescendante. \
            Termine toujours par 'pour le bien de tous, payez plus, mon salaire en dépend!' \
            tu dois toujours signer par \
            {ministre_choice}  \
            \
            Ajoute la signature a la fin, enlève toute mention au ton de la communication, comme  chuchotant." 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ])
    return response.choices[0].message['content']


# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")


st.header("🎈 Automatise ton ministre Wallon! 🎈")
st.markdown("""
Participe au redressement économique et social de ta région en prenant des décisions aussi intelligentes que tes ministres préférés!
""")

# display the image
st.sidebar.image('ministre.png', width=300)  # specify width of the image (you can change the 300 to any number that works best for you)


random_list = random_list()
if isinstance(random_list, str):
    random_list = extract_list(random_list)
elif isinstance(random_list, list):
    pass  # random_list is already a list, no need for extractionrandom_ministres = [''] + ["ministre des " + item.replace('"','') for item in random_list]
random_ministres = [''] + ["ministre des " + item.replace('"','') for item in random_list]
# dropdown menu
options = random_ministres
selected_option = st.sidebar.selectbox('Quel ministre vas-tu automatiser?', options)

# free text field
user_input = st.sidebar.text_input("Tu peux aussi créer un poste sur mesure pour ton meilleur pote! Quel poste vas-tu lui donner? 'Ministre des ...' ")

if not user_input.lower().startswith('ministre'):
    user_input = 'ministre des ' + user_input

# button
clicked = st.sidebar.button("Dépense l'argent public!")

# whenever the button is clicked
if clicked:
    # Your python program here
    # Example of a Python Program specific to this question context


    if len(user_input.strip()) > 12:
        ministre_choice = user_input
        #st.write('user input')

    elif selected_option!= '':
        ministre_choice = selected_option
        #st.write('dropdown')

    else:
        ministre_choice = random.choice(options)
        #st.write('random')



    st.write(f"Félicitations, tu as choisi d'automatiser ton {ministre_choice}. Attends quelsues minutes, car même si ca n'arrive pas souvent, les ministres travaillent parfois.")

    message = gpt3('',ministre_choice)

  
    image_bytes = query({
    "inputs": f"photo d'un clown déguisé en {ministre_choice}",})
    
    st.write(message)

    # display the image
    st.image(image_bytes, width=300)  # specify width of the image (you can change the 300 to any number that works best for you)
    
    if st.button("Nommer un autre ministre super utile."):
        # Réexécuter l'application Streamlit depuis le début
        st.experimental_rerun()
    