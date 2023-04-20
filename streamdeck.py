import os
import threading
from networktables import NetworkTables
from ntcore import *
from networktables.util import ntproperty
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

#button images path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

#networktables startup
NetworkTables.initialize(server = "10.70.28.2")

#target location ints for networktables
#sets up ints in their own networtables page labled "Target"
#default pose (0,0)
class NTValues():
    tgtColumn = ntproperty("/Target/Column", 0)
    tgtRow = ntproperty("/Target/Row", 0)

class Buttons():
    g0 = False #grid 0 
    g1 = False #grid 1
    g2 = False #grid 2
    c0l = False # column 0 low
    c0m = False # column 0 mid
    c0t = False # column 0 top
    c1l = False # column 1 low
    c1m = False # column 1 mid
    c1t = False # column 1 top
    c2l = False # column 2 low
    c2m = False # column 2 mid
    c2t = False # column 2 top

#indexes for all of the buttons
class Indexes():
    #empty indexes: 1, 6, 11

    g0 = 0 #grid 0
    g1 = 5 #grid 1
    g2 = 10 #grid 2
    c0t = 4 # column 0 top
    c1t = 9 # column 1 top
    c2t = 14 # column 2 top
    c0m = 3 # column 0 mid
    c1m = 8 # column 1 mid
    c2m = 13 # column 2 mid
    c0l = 2 # column 0 low
    c1l = 7 # column 1 low
    c2l = 12 # column 2 low

class TargetValues():
    grid = 0 #0 = left outer grid, 3 = co-op grid, 6 = right outer grid (driver pov)
    #added onto tgt column to get final pose as a column
    column = 0 #0 = leftmost column, 1 = middle column, 2 = rightmost column (driver pov)
    row = 0 #2 = lowest row, 1 = middle row, 0 = highest row (field pov)

#update networktables values
def updateNT():
    NTValues.tgtColumn = ntproperty("/Target/Column", (TargetValues.grid + TargetValues.column))
    NTValues.tgtRow = ntproperty("/Target/Row", TargetValues.row)

def getColumnValue(pose):
    if pose == "column0Top" or "column0Mid" or "column0Low":
        return 0
    elif pose == "column1Top" or "column1Mid" or "column1Low":
        return 1
    elif pose == "column2Top" or "column2Mid" or "column2Low":
        return 2
    else:
        print("Invalid pose value in getColumnValue.")
        return 0
    
def resetBools(erase):
    #reset button toggle bools to not selected
    if erase == "9x9":
        Indexes.c0l = False
        Indexes.c0m = False
        Indexes.c0t = False
        Indexes.c1l = False
        Indexes.c1m = False
        Indexes.c1t = False
        Indexes.c2l = False
        Indexes.c2m = False
        Indexes.c2t = False
    elif erase == "grid":
        Indexes.g0 = False
        Indexes.g1 = False
        Indexes.g2 = False

#return needed button image based on key and state
#appears as one image when toggle selected and another when not
#the "" is the image name
def setImgs(icon):
    if icon == "grid0":
        if Buttons.g0:
            return "grid1Tgt"
        else:
            return "grid1"
            
    elif icon == "grid1":
        if Buttons.g1:
            return "grid2Tgt"
        else:
            return "grid2"
            
    elif icon == "grid2":
        if Buttons.g2:
            return "grid3Tgt"
        else:
            return "grid3"
            
    elif icon == "column0Low":
        if Buttons.c0l:
            return "column1Tgt"
        else:
            return "column1"
            
    elif icon == "column1Low":
        if Buttons.c1l:
            return "column2Tgt"
        else:
            return "column2"
            
    elif icon == "column2Low":
        if Buttons.c2l:
            return "column3Tgt"
        else:
            return "column3"
            
    elif icon == "column0Mid":
        if Buttons.c0m:
            return "column1Tgt"
        else:
            return "column1"
            
    elif icon == "column1Mid":
        if Buttons.c1m:
            return "column2Tgt"
        else:
            return "column2"
            
    elif icon == "column2Low":
        if Buttons.c2m:
            return "column3Tgt"
        else:
            return "column3"
            
    elif icon == "column0Top":
        if Buttons.c0t:
            return "column1Tgt"
        else:
            return "column1"
            
    elif icon == "column1Top":
        if Buttons.c1t:
            return "column2Tgt"
        else:
            return "column2"
            
    elif icon == "column2Top":
        if Buttons.c2t:
            return "column3Tgt"
        else:
            return "column3"

# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 0, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(icon)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)


# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):

    if key == Indexes.g0:
        name = "grid0"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.g1:
        name = "grid1"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.g2:
        name = "grid2"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c0l:
        name = "column0Low"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c1l:
        name = "column1Low"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c2l:
        name = "column2Low"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c0m:
        name = "column0Mid"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c1m:
        name = "column1Mid"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c2m:
        name = "column2Mid"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c0t:
        name = "column0Top"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c1t:
        name = "column1Top"
        icon = "{}.png".format(setImgs(name))

    elif key == Indexes.c2t:
        name = "column2Top"
        icon = "{}.png".format(setImgs(name))

    else:
        #any indexes not set will set the image as a blank png
        name = "empty"
        icon = "{}.png".format("empty")

    #set text on keys to blank
    font = "Roboto-Regular.ttf"
    label = ""

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }

# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)


# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):

    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    #if any of the keys have been pressed
    if state:
        key_style = get_key_style(deck, key, state)

        #all the buttons toggle bool values
        #sets target values to which position is selected on the streamdeck
        if key_style["name"] == "grid0":
            resetBools("grid")
            Buttons.g0 = True
            TargetValues.grid = 0

        elif key_style["name"] == "grid1":
            resetBools("grid")
            Buttons.g1 = True
            TargetValues.grid = 3

        elif key_style["name"] == "grid2":
            resetBools("grid")
            Buttons.g2 = True
            TargetValues.grid = 6

        elif key_style["name"] == "column0Low":
            resetBools("9x9")
            Buttons.c0l = True
            TargetValues.column = 0
            TargetValues.row = 2

        elif key_style["name"] == "column1Low":
            resetBools("9x9")
            Buttons.c1l = True
            TargetValues.column = 1
            TargetValues.row = 2

        elif key_style["name"] == "column2Low":
            resetBools("9x9")
            Buttons.c2l = True
            TargetValues.column = 2
            TargetValues.row = 2

        elif key_style["name"] == "column0Mid":
            resetBools("9x9")
            Buttons.c0m = True
            TargetValues.column = 0
            TargetValues.row = 1

        elif key_style["name"] == "column1Mid":
            resetBools("9x9")
            Buttons.c1m = True
            TargetValues.column = 1
            TargetValues.row = 1

        elif key_style["name"] == "column2Mid":
            resetBools("9x9")
            Buttons.c2m = True
            TargetValues.column = 2
            TargetValues.row = 1

        elif key_style["name"] == "column0Top":
            resetBools("9x9")
            Buttons.c0t = True
            TargetValues.column = 0
            TargetValues.row = 0

        elif key_style["name"] == "column1Top":
            resetBools("9x9")
            Buttons.c1t = True
            TargetValues.column = 1
            TargetValues.row = 0

        elif key_style["name"] == "column2Top":
            resetBools("9x9")
            Buttons.c2t = True
            TargetValues.column = 2
            TargetValues.row = 0

        #update all key images
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        #update networktables values if any key on the streamdeck is pressed
        updateNT()
 
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

        # Set initial screen brightness to 80%.
        deck.set_brightness(80)

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
