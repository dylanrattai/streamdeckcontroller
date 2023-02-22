import os
import threading

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont

#button bools
grid0 = False
grid1 = False
grid2 = False
column0 = False
column1 = False
column2 = False
row0 = False
row1 = False
row2 = False
setTgt = False
markGrid = False
toggleMark = False
fellLow = False
resetTgt = False

#targeting ints (perspective in comments = looking at grid from field NOT DRIVER STATION)
grid = None #0 = left outer grid, 3 = co-op grid, 6 = right outer grid
column = None #0 = leftmost column, 1 = middle column, 2 = rightmost column
row = None #0 = lowest row, 1 = middle row, 2 = highest row
selectedNode = [None, None] #use to hold pose in only columns and rows
tgt = [None, None] #Column, Row

def setTgtInts():
  #set the grid num to an int that can be added w/ column to equal the column index 
  #for the total of all grids
  if(grid0):
    grid = 0
  elif(grid1):
    grid = 3
  elif(grid2):
    grid = 6
  #set the column num to the one selected
  if(column0):
    column = 0
  elif(column1):
    column = 1
  elif(column2):
    column = 2
  #set the row num to the one selected
  if(row0):
    row = 0
  elif(row1):
    row = 1
  elif(row2):
    row = 2

  #set the selected node tot eh column and row indexes
  selectedNode = [grid + column, row]

def setTgtF():
  try:
    tgt = [grid + column, row]
  except:
    return None

#def updateNetworktable():
  #send target node to table
  #send commands to networktable

def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)
  
# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    #set key indexes
    grid0Index = 0
    grid1Index = 5
    grid2Index = 10
    column0Index = 1
    column1Index = 6
    column2Index = 11
    row0Index = 12
    row1Index = 7
    row2Index = 2
    setTgtIndex = 3
    markToggleIndex = 13
    removeTgtIndex = 8
    madeShotIndex = 4
    fellLowIndex = 9
    #EMPTY INDEXES - 14

    if key == setTgtIndex:
      name = "Set TGT"
      #icon = "{}.png".format("down img" if setTgt else "not pressed img")
      #font = "Roboto-Regular.ttf"

    return {
        "name": name,
        #"icon": os.path.join(ASSETS_PATH, icon),
        #"font": os.path.join(ASSETS_PATH, font),
        #"label": label
    }

def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        deck.set_key_image(key, image)

def key_change_callback(deck, key, state):
    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)

        # when set target button pressed set ints and tgt
        if key_style["name"] == "Set TGT":
          setTgt = True
          setTgtInts()
          setTgtF()

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass
else:
  print("Failed to find Stream Deck")