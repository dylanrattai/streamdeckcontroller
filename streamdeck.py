import os
import threading

from networktables import NetworkTables
from ntcore import *
from networktables.util import ntproperty

from PIL import Image, ImageDraw, ImageFont
import ntcore
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

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
removeMarkIndex = 14

#targeting ints (perspective in comments = looking at grid from field NOT DRIVER STATION)
grid = None #0 = left outer grid, 3 = co-op grid, 6 = right outer grid
gridTgt = None
column = None #0 = leftmost column, 1 = middle column, 2 = rightmost column
columnTgt = None
row = None #0 = lowest row, 1 = middle row, 2 = highest row
rowTgt = None

#networktables setup
NetworkTables.initialize(server = "10.70.28.2")
sd = NetworkTables.getTable("SmartDashboard")

#target vars for networktables
class NTValues():
    tgtColumnNT = ntproperty("/SmartDashboard/TgtColumn", None)
    tgtRowNT = ntproperty("/SmartDashboard/TgtColumn", None)

def setTgtInts():
    global grid
    global column
    global row

    try:
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
    except:
        print("Missing Value in setTgtInts")

def setTgtF():
    global tgt
    global gridTgt
    global columnTgt
    global rowTgt

    try:
        gridTgt = grid
        columnTgt = column
        rowTgt = row
    except:
        print("Missing Value in setTgtInts (sent from setTgtF)")

def setImgs(icon):
    if icon == "grid0":
        if grid0 and gridTgt == 0:
            return "grid1TgtMrk"
        elif grid0 and gridTgt != 0:
            return "grid1Mrk"
        elif grid0 != True and gridTgt == 0:
            return "grid1Tgt"
        else:
            return "grid1"
            
    elif icon == "grid1":
        if grid1 and gridTgt == 3:
            return "grid2TgtMrk"
        elif grid1 and gridTgt != 3:
            return "grid2Mrk"
        elif grid1 != True and gridTgt == 3:
            return "grid2Tgt"
        else:
            return "grid2"
            
    elif icon == "grid2":
        if grid2 and gridTgt == 6:
            return "grid3TgtMrk"
        elif grid2 and gridTgt != 6:
            return "grid3Mrk"
        elif grid2 != True and gridTgt == 6:
            return "grid3Tgt"
        else:
            return "grid3"
            
    elif icon == "column0":
        if column0 and columnTgt == 0:
            return "column1TgtMrk"
        elif column0 and columnTgt != 0:
            return "column1Mrk"
        elif column0 != True and columnTgt == 0:
            return "column1Tgt"
        else:
            return "column1"
            
    elif icon == "column1":
        if column1 and columnTgt == 1:
            return "column2TgtMrk"
        elif column1 and columnTgt != 1:
            return "column2Mrk"
        elif column1 != True and columnTgt == 1:
            return "column2Tgt"
        else:
            return "column2"
            
    elif icon == "column2":
        if column2 and columnTgt == 2:
            return "column3TgtMrk"
        elif column2 and columnTgt != 2:
            return "column3Mrk"
        elif column2 != True and columnTgt == 2:
            return "column3Tgt"
        else:
            return "column3"
            
    elif icon == "row0":
        if row0 and rowTgt == 0:
            return "row1TgtMrk"
        elif row0 and rowTgt != 0:
            return "row1Mrk"
        elif row0 != True and rowTgt == 0:
            return "row1Tgt"
        else:
            return "row1"
            
    elif icon == "row1":
        if row1 and rowTgt == 1:
            return "row2TgtMrk"
        elif row1 and rowTgt != 1:
            return "row2Mrk"
        elif row1 != True and rowTgt == 1:
            return "row2Tgt"
        else:
            return "row2"
            
    elif icon == "row2":
        if row2 and rowTgt == 2:
            return "row3TgtMrk"
        elif row2 and rowTgt != 2:
            return "row3Mrk"
        elif row2 != True and rowTgt == 2:
            return "row3Tgt"
        else:
            return "row3"

def setOthersFalse(notFalseKey):
    global grid0
    global grid1
    global grid2
    global column0
    global column1
    global column2
    global row0
    global row1
    global row2
    global tgt
    global gridTgt
    global columnTgt
    global rowTgt

    if notFalseKey == "all":
        grid0 = False
        grid1 = False
        grid2 = False
        column0 = False
        column1 = False
        column2 = False
        row0 = False
        row1 = False
        row2 = False
        print("all")
    elif notFalseKey == "tgt":
        print("tgt")
        gridTgt = None
        columnTgt = None
        rowTgt = None
    elif notFalseKey == "grid0":
        grid1 = False
        grid2 = False
    elif notFalseKey == "grid1":
        grid0 = False
        grid2 = False
    elif notFalseKey == "grid2":
        grid0 = False
        grid1 = False
    elif notFalseKey == "column0":
        column1 = False
        column2 = False
    elif notFalseKey == "column1":
        column0 = False
        column2 = False
    elif notFalseKey == "column2":
        column0 = False
        column1 = False
    elif notFalseKey == "row0":
        row1 = False
        row2 = False
    elif notFalseKey == "row1":
        row0 = False
        row2 = False
    elif notFalseKey == "row2":
        row0 = False
        row1 = False

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

    if key == grid0Index:
        name = "grid0"
        icon = "{}.png".format(setImgs("grid0"))
    elif key == grid1Index:
        name = "grid1"
        icon = "{}.png".format(setImgs("grid1"))
    elif key == grid2Index:
        name = "grid2"
        icon = "{}.png".format(setImgs("grid2"))
    elif key == column0Index:
        name = "column0"
        icon = "{}.png".format(setImgs("column0"))
    elif key == column1Index:
        name = "column1"
        icon = "{}.png".format(setImgs("column1"))
    elif key == column2Index:
        name = "column2"
        icon = "{}.png".format(setImgs("column2"))
    elif key == row0Index:
        name = "row0"
        icon = "{}.png".format(setImgs("row0"))
    elif key == row1Index:
        name = "row1"
        icon = "{}.png".format(setImgs("row1"))
    elif key == row2Index:
        name = "row2"
        icon = "{}.png".format(setImgs("row2"))
    elif key == setTgtIndex:
        name = "setTgt"
        icon = "{}.png".format("target")
    elif key == markToggleIndex:
        name = "markGrid"
        icon = "{}.png".format("conecube")
    elif key == removeMarkIndex:
        name = "removeGridMark"
        icon = "{}.png".format("xconecube")
    elif key == removeTgtIndex:
        name = "removeTgt"
        icon = "{}.png".format("miss")
    elif key == madeShotIndex:
        name = "madeShot"
        icon = "{}.png".format("check")
    elif key == fellLowIndex:
        name = "fellLow"
        icon = "{}.png".format("felllow")
    else:
        name = "empty"
        icon = "{}.png".format("empty")

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
    global grid0
    global grid1
    global grid2
    global column0
    global column1
    global column2
    global row0
    global row1
    global row2
    global setTgt 
    global markGrid 
    global toggleMark
    global fellLow 
    global resetTgt 

    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)

        # When an exit button is pressed, close the application. NOT IN USE
        if key_style["name"] == "exit":
            # Use a scoped-with on the deck to ensure we're the only thread
            # using it right now.
            with deck:
                # Reset deck, clearing all button images.
                deck.reset()

                # Close deck handle, terminating internal worker threads.
                deck.close()
                
        #all the buttons toggle bool values
        elif key_style["name"] == "grid0":
            grid0 = not grid0
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "grid1":
            grid1 = not grid1
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "grid2":
            grid2 = not grid2
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "column0":
            column0 = not column0
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "column1":
            column1 = not column1
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "column2":
            column2 = not column2
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "row0":
            row0 = not row0
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "row1":
            row1 = not row1
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "row2":
            row2 = not row2
            setOthersFalse(key_style["name"])

        elif key_style["name"] == "setTgt":
            setTgtInts()
            setTgtF()
            NTValues.tgtColumnNT = gridTgt + columnTgt
            NTValues.tgtRowNT = rowTgt
            sd.putNumber("tgtColumn", gridTgt + columnTgt)
            sd.putNumber("tgtRow", rowTgt)
            sd.putBoolean(str(columnTgt) + str(columnTgt), False)

        elif key_style["name"] == "removeTgt":
            setOthersFalse("tgt")
            NTValues.tgtColumnNT = None
            NTValues.tgtRowNT = None
            sd.putNumber("tgtColumn", None)
            sd.putNumber("tgtRow", None)

        elif key_style["name"] == "fellLow":
            sd.putBoolean(str(columnTgt) + str(0), True)
            setOthersFalse("tgt")

        elif key_style["name"] == "madeShot":
            NTValues.tgtColumnNT = None
            NTValues.tgtRowNT = None
            sd.putNumber("tgtColumn", None)
            sd.putNumber("tgtRow", None)
            sd.putBoolean(str(columnTgt) + str(columnTgt), True)
            setOthersFalse("tgt")

        elif key_style["name"] == "markGrid":
            setTgtInts()
            sd.putBoolean(str(column) + str(row), True)
            setOthersFalse("all")

        elif key_style["name"] == "removeGridMark":
            setTgtInts()
            sd.putBoolean(str(column) + str(row), None)
            setOthersFalse("all")

        #update key images
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

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
        sd.putBoolean("Streamdeck Connected", True)
else:
    sd.putBoolean("Streamdeck Connected", False)