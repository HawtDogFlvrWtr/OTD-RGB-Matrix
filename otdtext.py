#!/usr/bin/env python
from samplebase import SampleBase
#from rgbmatrix import graphics
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image
import requests
import time
import json

class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

    def run(self):
      canvas = self.matrix
      white = graphics.Color(255, 255, 255)
      gray = graphics.Color(192, 192, 192)
      red = graphics.Color(241, 65, 108)
      green = graphics.Color(80, 205, 137)
      blue = graphics.Color(0, 163, 255)
      font = graphics.Font()
      font.LoadFont("/opt/4x6.bdf")
      with open('/boot/api_key.txt') as api_file:
          lines = api_file.readlines()
          api_key = lines[0]
      print("Found api key %s" % api_key)
      while True:
        canvas.Clear()
        url = 'https://beta.ownthedip.com/api/pull_orders/%s' % api_key.rstrip()
        print(url)
        get_json = requests.get(url)
        if get_json.status_code != 200:
          time.sleep(60)
          continue
        orders = get_json.json()
        print(orders)
        line = 5
        if len(orders) == 0: # Don't show if we have enough orders to fill the screen
          graphics.DrawText(canvas, font, 0, 5, white, "No Open Orders")
        for order in orders:
          symbol = order['symbol']
          percent = order['percent']

          # Calculate where percent is on the screen
          if float(percent) <= -10 or float(percent) >= 10:
            rl = 45
          elif float(percent) >= 100:
            rl = 35
          else:
            rl = 45

          # Symbol
          graphics.DrawText(canvas, font, 0, line, gray, symbol)

          # Percent
          if float(percent) < 0:
              if float(percent) == -80085:
                graphics.DrawText(canvas, font, rl, line, green, "Open")
              else:
                percent = str(percent).replace('-','')
                graphics.DrawText(canvas, font, rl, line, red, percent+"%")
          else:
            graphics.DrawText(canvas, font, rl, line, green, str(percent)+"%")

          # Recalc line location with 4x6 font  
          line = line + 6

        # Print OTD at the bottom
        if len(orders) < 10: # Don't show if we have enough orders to fill the screen
          graphics.DrawText(canvas, font, 12, 64, blue, "OwnTheDip.com")
        time.sleep(30)



# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
