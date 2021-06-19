"""Main module."""
from time import strftime

import requests

from font_hanken_grotesk import HankenGroteskBold
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont

# Train Constants
STATION_FROM = 'MZH'
STATION_TO = 'LBG'
ARRIVAL_NUM = 3

# Weather Constants
W_API_KEY = ""
LAT = 51.5085
LON = -0.1257
KELVIN_CONV = 273.15

inky_display = InkyWHAT('black')
inky_display.set_border(inky_display.WHITE)

im = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
d = ImageDraw.Draw(im)
fnt = ImageFont.truetype(HankenGroteskBold, 25)
fnt_w = ImageFont.truetype(HankenGroteskBold, 35)

response = requests.get('https://huxley2.azurewebsites.net/arrivals/' +
                        STATION_FROM + '/from/' + STATION_TO + '/' +
                        str(ARRIVAL_NUM))

data = response.json()
str0 = strftime('%a, %d %b %Y - %H:%M')

try:
    str1 = '1) ' + data['trainServices'][0]['origin'][0]['locationName'] \
        + ' - ' + data['trainServices'][0]['sta']
    str2 = '2) ' + data['trainServices'][1]['origin'][0]['locationName'] \
        + ' - ' + data['trainServices'][1]['sta']
    str3 = '3) ' + data['trainServices'][2]['origin'][0]['locationName'] \
        + ' - ' + data['trainServices'][2]['sta']
except KeyError:
    str1 = "Error"
    str2 = "Error"
    str3 = "Error"

d.text((10, 10), str0, inky_display.BLACK, fnt_w)
d.text((10, 60), str1, inky_display.BLACK, fnt)
d.text((10, 90), str2, inky_display.BLACK, fnt)
d.text((10, 120), str3, inky_display.BLACK, fnt)

response_w = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&exclude=minutely,hourly&appid={W_API_KEY}"
)

data_w = response_w.json()

try:
    str4 = ("{:.1f}".format(data_w['current']['temp'] - KELVIN_CONV) +
            u"\N{DEGREE SIGN}" + "C - " +
            data_w['current']['weather'][0]['main'])
    str5 = ("Today: " +
            "{:.1f}".format(data_w['daily'][0]['temp']['min'] - KELVIN_CONV) +
            u"\N{DEGREE SIGN}" + "C - " +
            "{:.1f}".format(data_w['daily'][0]['temp']['max'] - KELVIN_CONV) +
            u"\N{DEGREE SIGN}" + "C")
    str6 = (data_w['daily'][0]['weather'][0]['description'])
except KeyError:
    str4 = "Error"
    str5 = "Error"
    str6 = "Error"

d.text((10, 170), str4, inky_display.BLACK, fnt_w)
d.text((10, 220), str5, inky_display.BLACK, fnt)
d.text((10, 250), str6, inky_display.BLACK, fnt)

inky_display.set_image(im)
inky_display.show()
