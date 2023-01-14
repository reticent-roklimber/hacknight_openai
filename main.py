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
        input("In which city are you located?", name="location", type=TEXT),
        input("What is your travel budget(INR)", name="expense", type=NUMBER),
    ],
)
search_text="list of 5 best tourist locations near "+data['location']+"  for "+str(data['expense'])+" inr\n\n"
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=search_text,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
#print(response)
locations=response['choices'][0]['text'].split('\n')
locations = [ele for ele in locations if ele.strip()]
put_text("The Five nearby Places to Visit:")
places=[];des=[]
for loc in locations:
    places.append(loc.split(':')[0])
    des.append(loc.split(':')[-1])
put_table(
    [
        ["Destinations", places],
        ["Description", des]
    ]
)