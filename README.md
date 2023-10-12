# technical_showcase_LT
This is my work for the LT Technical Showcase

I chose to take the GUI approach to this program. I thought that this problem lent itself to a GUI because of its relation to images.

In order to run this program you need the following:

- Python 3.11.4
- requests library
- JSON library
- PySimpleGUI library

I believe that the rest of the libraries that I used in this project are part of the standard Python library. The easiest way to run this is to open it in VSCode and set the Python interpreter and then run it. Could also be run from the command line with "python albumViewer.py" assuming you are in the correct directory and Python is set to work with your command line terminal.

This program makes an initial request to bring in the JSON array and puts the title and id into a list. When searching for a specific album, a new request is made with that album number as the parameter. You can also display the thumbnail to the right of the GUI by searching the id that is listed to the left of the title in the list. Along with the image, you get the title and the album it is located in.

Thank you so much for your consideration.
