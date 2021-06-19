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
LAT = 51.5085
LON = -0.1257
EXCL = 'minutely,hourly'
W_API_KEY = ""
KELVIN_CONV = 273.15

inky_display = InkyWHAT('black')
inky_display.set_border(inky_display.BLACK)

img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font_s = ImageFont.truetype(HankenGroteskBold, 25)
font_l = ImageFont.truetype(HankenGroteskBold, 35)

response_train = requests.get(
    'https://huxley2.azurewebsites.net/arrivals/'
    f'{STATION_FROM}/from/{STATION_TO}/{ARRIVAL_NUM}')

payload_weather = {'lat': LAT, 'lon': LON, 'exclude': EXCL, 'appid': W_API_KEY}

response_weather = requests.get(
    'https://api.openweathermap.org/data/2.5/onecall?', params=payload_weather)

data_t = response_train.json()
data_w = response_weather.json()

str_date_time = strftime('%a %d %b %Y - %H:%M')

try:
    str_train1 = '1) ' + \
        data_t['trainServices'][0]['origin'][0]['locationName'] + \
        ' - ' + data_t['trainServices'][0]['sta']
    str_train2 = '2) ' + \
        data_t['trainServices'][1]['origin'][0]['locationName'] + \
        ' - ' + data_t['trainServices'][1]['sta']
    str_train3 = '3) ' + \
        data_t['trainServices'][2]['origin'][0]['locationName'] + \
        ' - ' + data_t['trainServices'][2]['sta']
except KeyError:
    str_train1 = "Error"
    str_train2 = "Error"
    str_train3 = "Error"

try:
    str_w_curr = ("{:.1f}".format(data_w['current']['temp'] - KELVIN_CONV) +
                  u"\N{DEGREE SIGN}" + "C - " +
                  data_w['current']['weather'][0]['main'])
    str_w_today = (
        "Today: " +
        "{:.1f}".format(data_w['daily'][0]['temp']['min'] - KELVIN_CONV) +
        u"\N{DEGREE SIGN}" + "C - " +
        "{:.1f}".format(data_w['daily'][0]['temp']['max'] - KELVIN_CONV) +
        u"\N{DEGREE SIGN}" + "C")
    str_w_desc = (data_w['daily'][0]['weather'][0]['description'])
except KeyError:
    str_w_curr = "Error"
    str_w_today = "Error"
    str_w_desc = "Error"

draw.text((10, 170), str_w_curr, inky_display.BLACK, font_l)
draw.text((10, 220), str_w_today, inky_display.BLACK, font_s)
draw.text((10, 250), str_w_desc, inky_display.BLACK, font_s)
draw.text((10, 10), str_date_time, inky_display.BLACK, font_l)
draw.text((10, 60), str_train1, inky_display.BLACK, font_s)
draw.text((10, 90), str_train2, inky_display.BLACK, font_s)
draw.text((10, 120), str_train3, inky_display.BLACK, font_s)

inky_display.set_image(img)
inky_display.show()
