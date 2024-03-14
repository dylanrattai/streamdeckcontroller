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

#networktables setup
NetworkTables.initialize(server = "RIO IP ADDRESS ex: 10.70.28.2 or roborio-XXXX-frc.local")
sd = NetworkTables.getTable("SmartDashboard") #interact w/ smartdashboard
sdv = NetworkTables.getTable("Streamdeck") #make table for values to be changed from this script

#bools for if the button is in a toggled state, make ButtonBools.get/set_b_value a int 1-15
class ButtonBools:
    def __init__(self):
        self.b_values = [False] * 15

    def set_b_value(self, index, value):
        self.b_values[index - 1] = value
    
    def get_b_value(self, index):
        return self.b_values[index - 1]

#indexes for all of the buttons on the streamdeck
#top left is index 0, bottom right is index 14
class ButtonIndexes:
    def __init__(self):
        self.values = tuple(range(15))

    def get_index(self, index):
        if 1 <= index <= 15:
            return self.values[index - 1]
        else:
            return ValueError("Requested invalid index")
        
buttonBools = ButtonBools()
buttonIndexes = ButtonIndexes()
    
def reset_bools():
    buttonBools.set_b_value(1, False)
    buttonBools.set_b_value(2, False)
    buttonBools.set_b_value(3, False)
    buttonBools.set_b_value(4, False)
    buttonBools.set_b_value(5, False)
    buttonBools.set_b_value(6, False)
    buttonBools.set_b_value(7, False)
    buttonBools.set_b_value(8, False)
    buttonBools.set_b_value(9, False)
    buttonBools.set_b_value(10, False)
    buttonBools.set_b_value(11, False)
    buttonBools.set_b_value(12, False)
    buttonBools.set_b_value(13, False)
    buttonBools.set_b_value(14, False)
    buttonBools.set_b_value(15, False)

#return needed button image based on key and state
#the return is the image name
#images should be 80px by 80px
def setImgs(icon):
    if icon == "Bool Example" and buttonBools.get_b_value(1):
        return "red"
    else:
        return "empty"

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
    #draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)


# Returns styling information for a key based on its position and state.
# this is run everytime a key is pressed & released
def get_key_style(deck, key, state):

    #set key info
    if key == buttonIndexes.get_index(1):
        name = "Bool Example"
        icon = "{}.png".format(setImgs(name))
        label = ""

    else:
        #any indexes not set will set the image as a blank png
        name = "empty"
        icon = "{}.png".format("empty")
        label = ""

    #set text on keys to blank, uncomment the 2 lines under this if you dont want to use text labels, you can then remove label from the above if statements
    font = "Roboto-Regular.ttf"
    #label = ""

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

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    #if any of the keys have been pressed
    if state:

        #update all key images
        key_style = get_key_style(deck, key, state)

        #button 1 toggles bool values, add elifs to add keys here
        if key_style["name"] == "Bool Example":
            buttonBools.set_b_value(1, not buttonBools.get_b_value(1))
            sdv.putBoolean("boolExample", buttonBools.get_b_value(1))

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
