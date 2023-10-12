import PySimpleGUI as psg
import requests
import json
from io import BytesIO
from PIL import Image
import re

photos = []

def getSearch(search):
    x = requests.get('https://jsonplaceholder.typicode.com/photos?albumId=' + str(search)) #cat the album number to the end
    dataStream = json.loads(x.text) # load the response as json datastream
    current = int(search) # Set the current album position. Not necessary for the search function, but it keeps it consistent with the function later
    photos.append("Album: " + str(current)) # Make a nice header
    for item in dataStream: # For all items in the json array
        if(item["albumId"] > current): # If this is the next album
            current = item["albumId"] # make this the current album
            photos.append("Album: " + str(current)) # make a nice header
        photos.append("     [" + str(item["id"]) + "] " + str(item["title"])) # add the title and id to the list.
    return photos # return the list

def getImage(id):
    x = requests.get('https://jsonplaceholder.typicode.com/photos?id=' + str(id)) # Pull the specific image by id
    dataStream = json.loads(x.text) # Do the same as above
    y = requests.get(dataStream[0]["thumbnailUrl"]) # Pull the thumb url from that prior response
    img_data = y.content # Get content from that response
    pil_image = Image.open(BytesIO(img_data)) # Convert
    png_bio = BytesIO()
    pil_image.save(png_bio, format="PNG",size=(60,60)) # Make sure this is a PNG image
    png_data = png_bio.getvalue() # Get the data back
    return png_data, dataStream[0]["title"], dataStream[0]["albumId"], dataStream[0]["id"] # Return everything about the image


lst = psg.Listbox(photos, size=(70, 20), font=('Arial Bold', 14), expand_y=True, enable_events=True, key='-LIST-') # Make a list item and attach the photos list to it
#frame1 = psg.Frame("Photos",[lst,psg.Button('Load Selected Image')], title_color="green")
image, title, albumId, id = getImage(1) # Get this first image, just so there is something there
inner = [[psg.Image(data=image, key="-Image-", size=(150,150))],
         [psg.Text(title, key="-Title-",size=(150,1))],
         [psg.Text("From Album: " + str(albumId), key="-Album-")]] # Make the pieces to show the image, title and albumid in the right segment, stacked vertically
left = [[lst]] # Add the list item into an area for the left side
layout = [[psg.Text("Enter Album Number for Search:", key='label', font=('Arial Bold', 14), justification='left'),
          psg.Input(size=(20, 1), font=('Arial Bold', 14), expand_x=True, key='-INPUT-'),
   psg.Button('Search'),
   psg.Button('Exit')],
   [psg.Text("Enter Image Number To View:", key='imgNum', font=('Arial Bold', 14), justification='left'),
          psg.Input(size=(20, 1), font=('Arial Bold', 14), expand_x=True, key='-IMGNUM-'),
          psg.Button('Enter')],
   [psg.Column(left, vertical_alignment='top'), psg.VSeparator(), psg.Column(inner, vertical_alignment='top')],
   [psg.Text("", key='-MSG-', font=('Arial Bold', 14), justification='center')] # layout stacked vertically besides column exception. 
]
window = psg.Window("Alex Brown's Album Viewer", layout, size=(1280, 550), location=(0,0)) # Create window and add layout in
x = requests.get('https://jsonplaceholder.typicode.com/photos') # make initial request 


dataStream = json.loads(x.text)
current = 1
photos.append("Album: " + str(current))
for item in dataStream:
    if(item["albumId"] > current):
        current = item["albumId"]
        photos.append("Album: " + str(current))
    photos.append("     [" + str(item["id"]) + "] " + str(item["title"])) # From request to here works exactly like the getSearch function
    
while True: # Loop to run the GUI
   event, values = window.read() # Get events
   if event in (psg.WIN_CLOSED, 'Exit'): # If the exit button is pressed or the window is closed
      break # Break the loop so the program ends
   if event == 'Search': # If the search button is pressed
      photos.clear() # Clear the photos array
      try: # try to cast the string from the search bar to an int
          input = int(values['-INPUT-'])
      except(ValueError): # If it can't, default to album 1
          input = 1
      photos = getSearch(input) # Call search and save the list
      window['-LIST-'].update(photos) # Updat the list into the listbox
   if event == 'Enter': # When Enter is pressed
        try: # Try the casting like above
          input = int(values['-IMGNUM-'])
        except(ValueError):
          input = 1
        image, title, albumId, id = getImage(input) # Get that specific input and everything about it
        window['-Image-'].update(data=image,visible=True) # Update the image with what we just pulled
        window['-Title-'].update(title) # Update the title beneath the image
        window['-Album-'].update("From Album: " + str(albumId)) # Update the album tag
        window.refresh() # refresh the window to force it updates.
window.close() # If we break from an exit, close peacefully

