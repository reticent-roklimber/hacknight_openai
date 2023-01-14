from pywebio.input import *
from pywebio.output import *
import yaml
import openai

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

openai.api_key = config['openai']['api_key']

put_image(open("assets/tropikality_logo.png",'rb').read())

data = input_group(
    "User data",
    [
        input("Choose travel destination", name="location", type=TEXT),
        input("What is your budget for stay?(INR)", name="expense", type=NUMBER),
    ],
)

search_text_stay="list of 3 top places to stay in or near "+data['location']+"  for budget of "+str(data['expense'])+" INR sorted by popularity.\n\n"
# search_text_attraction="list of 3 top places to stay in or near "+data['location']+"  for budget of "+str(data['expense'])+" INR sorted by popularity.\n\n"


def get_response(search_text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=search_text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
            )
    return response

locations=get_response(search_text_stay)['choices'][0]['text'].split('\n')
locations = [location for location in locations if location.strip()]

put_text(locations[0])
put_text(locations[1])
put_text(locations[2])

# places=[];des=[]
# for loc in locations:
#     places.append(loc.split(':')[0])
#     des.append(loc.split(':')[-1])
# put_table(
#     [
#         ["Destinations", places],
#         ["Description", des]
#     ]
# )