import os
import threading
import ntcore
from networktables import NetworkTables
from ntcore import *
from networktables.util import ntproperty
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")

#targeting ints (perspective in comments = looking at grid from field NOT DRIVER STATION)
grid = 0 #0 = left outer grid, 3 = co-op grid, 6 = right outer grid
gridTgt = 0
column = 0 #0 = leftmost column, 1 = middle column, 2 = rightmost column
columnTgt = 0
row = 0 #0 = lowest row, 1 = middle row, 2 = highest row
rowTgt = 0

tmpVar1 = None
tmpVar2 = None

#networktables setup
NetworkTables.initialize(server = "10.70.28.2")
sd = NetworkTables.getTable("SmartDashboard")

#target vars for networktables
class NTValues():
    tgtColumnNT = ntproperty("/SmartDashboard/Target/Column", 0)
    tgtRowNT = ntproperty("/SmartDashboard/Target/Row", 0)

class Buttons():
    grid0 = False
    grid1 = False
    grid2 = False
    column0Low = False
    column0Mid = False
    column0Top = False
    column1Low = False
    column1Mid = False
    column1Top = False
    column2Low = False
    column2Mid = False
    column2Top = False

class Indexes():
    grid0Index = 3
    grid1Index = 8
    grid2Index = 13
    column0LowIndex = 0
    column0MidIndex = 5
    column0TopIndex = 10
    column1LowIndex = 1
    column1MidIndex = 6
    column1TopIndex = 11
    column2Index = 2
    column2Index = 7
    column2Index = 12
    toggleExitIndex = 4

def setImgs(icon):
    if icon == "grid0":
        if grid0 != True and gridTgt == 0:
            return "grid1Tgt"
        else:
            return "grid1"

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

        elif key_style["name"] == "setTgt":
            setTgtInts()
            setTgtF()
            NTValues.tgtColumnNT = ntproperty("/SmartDashboard/Target/Column", gridTgt + columnTgt)
            NTValues.tgtRowNT = ntproperty("/SmartDashboard/Target/Row", rowTgt)
            sd.putBoolean("TC" + str(columnTgt + gridTgt), True)
            sd.putBoolean("TR" + str(rowTgt), True)

        elif key_style["name"] == "removeTgt":
            setOthersFalse("tgt")
            NTValues.tgtColumnNT = ntproperty("/SmartDashboard/Target/Column", 999)
            NTValues.tgtRowNT = ntproperty("/SmartDashboard/Target/Row", 999)
            sd.putBoolean("TC" + str(columnTgt + gridTgt), False)
            sd.putBoolean("TR" + str(rowTgt), False)

        elif key_style["name"] == "fellLow":
            sd.putBoolean(str(columnTgt + gridTgt) + str(0), True)
            setOthersFalse("tgt")

        elif key_style["name"] == "madeShot":
            NTValues.tgtColumnNT = ntproperty("/SmartDashboard/Target/Column", 999)
            NTValues.tgtRowNT = ntproperty("/SmartDashboard/Target/Row", 999)
            sd.putBoolean(str(columnTgt + gridTgt) + str(rowTgt), True)
            sd.putBoolean("TC" + str(columnTgt + gridTgt), False)
            sd.putBoolean("TR" + str(rowTgt), False)
            setOthersFalse("tgt")

        #update key images
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

def setupSD():
    #MAKE ALL THE BOOLS
    print("Placeholder")

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