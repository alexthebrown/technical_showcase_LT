import PySimpleGUI as psg
import requests
import json
from io import BytesIO
from PIL import Image
import re

photos = []
ids = []

def getSearch(search):
    x = requests.get('https://jsonplaceholder.typicode.com/photos?albumId=' + str(search))
    dataStream = json.loads(x.text)
    current = int(search)
    photos.append("Album: " + str(current))
    ids.append("Album Header")
    for item in dataStream:
        if(item["albumId"] > current):
            current = item["albumId"]
            photos.append("Album: " + str(current))
            ids.append("Album Header")
        photos.append("     [" + str(item["id"]) + "] " + str(item["title"]))
        ids.append(item["id"])

    return photos, ids

def getImage(id):
    x = requests.get('https://jsonplaceholder.typicode.com/photos?id=' + str(id))
    dataStream = json.loads(x.text)
    y = requests.get(dataStream[0]["thumbnailUrl"])
    img_data = y.content
    pil_image = Image.open(BytesIO(img_data))
    png_bio = BytesIO()
    pil_image.save(png_bio, format="PNG",size=(60,60))
    png_data = png_bio.getvalue()
    return png_data, dataStream[0]["title"], dataStream[0]["albumId"], dataStream[0]["id"]


lst = psg.Listbox(photos, size=(70, 20), font=('Arial Bold', 14), expand_y=True, enable_events=True, key='-LIST-')
#frame1 = psg.Frame("Photos",[lst,psg.Button('Load Selected Image')], title_color="green")
image, title, albumId, id = getImage(1)
inner = [[psg.Image(data=image, key="-Image-", size=(150,150))],
         [psg.Text(title, key="-Title-",size=(150,1))],
         [psg.Text("From Album: " + str(albumId), key="-Album-")]]
left = [[lst]]
layout = [[psg.Text("Enter Album Number for Search:", key='label', font=('Arial Bold', 14), justification='left'),
          psg.Input(size=(20, 1), font=('Arial Bold', 14), expand_x=True, key='-INPUT-'),
   psg.Button('Search'),
   psg.Button('Exit')],
   [psg.Text("Enter Image Number To View:", key='imgNum', font=('Arial Bold', 14), justification='left'),
          psg.Input(size=(20, 1), font=('Arial Bold', 14), expand_x=True, key='-IMGNUM-'),
          psg.Button('Enter')],
   [psg.Column(left, vertical_alignment='top'), psg.VSeparator(), psg.Column(inner, vertical_alignment='top')],
   [psg.Text("", key='-MSG-', font=('Arial Bold', 14), justification='center')]
]
window = psg.Window("Alex Brown's Album Viewer", layout, size=(1280, 550), location=(0,0))
x = requests.get('https://jsonplaceholder.typicode.com/photos')


dataStream = json.loads(x.text)
current = 1
photos.append("Album: " + str(current))
ids.append("Album Header")
for item in dataStream:
    if(item["albumId"] > current):
        current = item["albumId"]
        photos.append("Album: " + str(current))
        ids.append("Album Header")
    photos.append("     [" + str(item["id"]) + "] " + str(item["title"]))
    ids.append(item["id"])
    
while True:
   event, values = window.read()
   print(event, values)
   if event in (psg.WIN_CLOSED, 'Exit'):
      break
   if event == 'Search':
      photos.clear()
      photos, ids = getSearch(int(values['-INPUT-']))
      window['-LIST-'].update(photos)
   if event == 'Enter':
        image, title, albumId, id = getImage(values['-IMGNUM-'])
        window['-Image-'].update(data=image,visible=True)
        window['-Title-'].update(title)
        window['-Album-'].update("From Album: " + str(albumId))
        window.refresh()
window.close()

