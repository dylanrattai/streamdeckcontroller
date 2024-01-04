# Streamdeck Controller

## Needs
PIP Modules
- streamdeck (Stream Deck functionality)
- pillow (images)
- pyntcore (networktables)

Program (Needed for HID Interfacing)
- [HIDAPI](https://github.com/libusb/hidapi)

Uses
- [Python Streamdeck by Dean Camera](https://github.com/abcminiuser/python-elgato-streamdeck)

## How it works
It uses Python Streamdeck to display images and activate functions. To send commands to the robot, it uses Python Networktables to modify variables in the network tables. The robot pulls these variables' values when needed. For example, a grid could be displayed on the Stream Deck, and buttons would send the target position on a 2D grid. On the robot side, the values from Networktables for the target pose would be pulled when the shooting sequence has started, so the robot knows what column & grid to drive to and which row to target.
