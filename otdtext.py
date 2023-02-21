#!/usr/bin/env python
import time
import sys
import os
import requests
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.brightness = 40
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

white = graphics.Color(255, 255, 255)
gray = graphics.Color(192, 192, 192)
red = graphics.Color(241, 65, 108)
green = graphics.Color(80, 205, 137)
blue = graphics.Color(0, 163, 255)
font = graphics.Font()
font.LoadFont("/opt/OTD-RGB-Matrix/4x6.bdf")
try:
  with open('/boot/api_key.txt') as api_file:
    lines = api_file.readlines()
    api_key = lines[0]
    print("Found api key %s" % api_key)

    print("Press CTRL-C to stop.")
    canvas_off = matrix.CreateFrameCanvas()
    url = 'https://beta.ownthedip.com/api/pull_orders/%s' % api_key.rstrip()
    print(url)
    while True:
      canvas_off.Clear()
      get_json = requests.get(url)
      if get_json.status_code != 200:
        time.sleep(60)
        continue
      orders = get_json.json()
      print(orders)
      line = 5
      if len(orders) == 0: # Don't show if we have enough orders to fill the screen
        graphics.DrawText(canvas_off, font, 0, 5, white, "No Open Orders")
      for order in orders:
        symbol = order['symbol']
        percent = order['percent']
        side = order['side']

        # Calculate where percent is on the screen
        if float(percent) <= -10 or float(percent) >= 10:
          rl = 45
        elif float(percent) >= 100:
          rl = 35
        else:
          rl = 45

        # Symbol
        graphics.DrawText(canvas_off, font, 0, line, gray, symbol)

        # Percent
        if float(percent) < 0:
          if float(percent) == -80085:
            if side == 'sell':
              text = 'Sell'
              text_color = blue
            else:
              text = 'Buy'
              text_color = green
            graphics.DrawText(canvas_off, font, rl, line, text_color, text)
          else:
            percent = str(percent).replace('-','')
            graphics.DrawText(canvas_off, font, rl, line, red, percent+"%")
        else:
          graphics.DrawText(canvas_off, font, rl, line, green, str(percent)+"%")

        # Recalc line location with 4x6 font  
        line = line + 6

        # Print OTD at the bottom
        if len(orders) < 10: # Don't show if we have enough orders to fill the screen
          graphics.DrawText(canvas_off, font, 7, 64, gray, "OwnTheDip.com")
      #canvases.append(canvas)
      canvas_off = matrix.SwapOnVSync(canvas_off)
      time.sleep(30)
except KeyboardInterrupt:
  sys.exit(0)
