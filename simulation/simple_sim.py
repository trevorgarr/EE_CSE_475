import time
#from rpi_ws281x import PixelStrip, Color
import argparse
#import serial
import requests
import json
import socketio
import asyncio
#from led_strip import led_strip
from paintApp import paintingApp
from tictactoeApp import tictactoeApp
from chessApp import chessApp
import numpy as np
from PIL import Image
from neopixel_neomatrix import Adafruit_NeoMatrix

deviceID = 0
#ser = serial.Serial("/dev/ttyS0", 115200)    #Open port with baud rate
touchArr = [0]*192
sio = socketio.AsyncClient()
ip = 'http://192.168.0.11:5000/'
gridLoc = [0,0]
lastPressedIndex = -1
pressedIndex = -1
strip = 0

async def connectToServer():
    await sio.connect(ip)
    await sio.sleep(1)

json_array = {"array": touchArr}

gridSelect = 1

async def simulationInput(strip, pApp):
    while True:
        if (strip.new_touch == 1):
            pApp.paint(strip.new_touch_cord[0], strip.new_touch_cord[1])
            strip.pixels.gui.new_touch = 0
        await asyncio.sleep(0.1)

data_array = []

def arrayConvert(grid):
    blankArray = [(0,0,0)]*192
    for i in range(12):
        for j in range(16):
            blankArray[convert(i,j)] = grid[i+j*12]
    return blankArray
    #return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]

def gridMake():
    global data_array, data_rotate
    image = Image.open('../images/pixel.png')
    image = image.rotate(180)
    # convert image to numpy array
    image = image.convert('RGB')
    data = image.getdata()
    data_array = list(data)
    print(data_array)
    data_array = arrayConvert(data_array)
    image = image.save("mario.png")
    print(data_array)


def convert(x, y):
    # if in an odd column, reverse the order
    if (x % 2 != 0):
        y = 15 - y
    return (x * 16) + y

# https://stackoverflow.com/questions/5661725/format-ints-into-string-of-hex
def rgbToHex(r, g, b):
    numbers = [r, g, b]
    return '#' + ''.join('{:02X}'.format(a) for a in numbers)

DRAWING = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[200,200,200],[200,200,200],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[200,200,200],[200,200,200],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
           [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

storedGrid = []
async def mainProgram(strip, pApp):
    while True:
        global gridSelect, storedGrid
        if (gridSelect == 1):
            selectedGrid = pApp.touchGrid
        elif (gridSelect == 0):
            selectedGrid = data_array
        loop = asyncio.get_event_loop()
        if (storedGrid != selectedGrid):
            await strip.update_buffer(selectedGrid)
            strip.json_array["array"] = arrayConvert(strip.touch_array)
            r = requests.post(ip + '/array?id='+str(deviceID), json=json.dumps(strip.json_array))
            storedGrid = selectedGrid.copy()
        await asyncio.sleep(0.1)

async def updateSim(strip):
    while True:
        strip.show()
        await asyncio.sleep(0.1)

async def main(strip, pApp):
    await connectToServer()
    asyncio.create_task(mainProgram(strip, pApp))
    asyncio.create_task(updateSim(strip))
    asyncio.create_task(simulationInput(strip, pApp))

@sio.on('my_response')
async def catch_all(data):
    if (data['data']['deviceID'] == deviceID):
        print("Okay: ", data)
        readFrom = data['data']
        print("okay 2: ", readFrom)
        readColor = readFrom['color']
        newColor = (int(readColor[1:3], 16), int(readColor[3:5], 16), int(readColor[5:7], 16))
        pApp.webPaint(readFrom['index'], newColor)

@sio.on('connected')
async def onConnected(data):
    global deviceID
    print(data)
    deviceID = data['deviceID']

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    pApp = paintingApp()
    # Create led_strip object with appropriate configuration.
    strip = Adafruit_NeoMatrix()
    gridMake()
    strip.show()
    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    try:
        loop = asyncio.get_event_loop()
        #loop.add_reader(ser, readUART, pApp)
        loop.run_until_complete(main(strip, pApp))
        loop.run_forever()


    except KeyboardInterrupt:
        if args.clear:
            strip.color_wipe(strip, Color(0, 0, 0))