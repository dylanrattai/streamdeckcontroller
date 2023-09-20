# Streamdeck Controller

## Needs
PIP Modules
- streamdeck (streamdeck functionality)
- pillow (images)
- pyntcore

Program (Needed for HID Interfacing)
- [HIDAPI](https://github.com/libusb/hidapi)

Uses
- [Python Streamdeck by Dean Camera](https://github.com/abcminiuser/python-elgato-streamdeck)

## How it works
Uses Python Streamdeck to display images and activate functions. To send commands to the robot, it uses Python Networktables to modify variables in the network tables. The robot pulls these variables' values when needed. For example, this project is just for sending target position in a 2D grid. Robot side, the robot pulls the values from Networktables for the target pose when the shooting sequence has started, so it knows what column & grid to drive to and which row to target.
