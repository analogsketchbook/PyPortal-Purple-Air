"""
Modified Adafruit code to work with Purple Air data

Original Adafruit tutorial here:
https://learn.adafruit.com/pyportal-air-quality-display

Setup:
1) Follow the steps in their tutorial to setup your PyPortal and add the libraries they suggest
2) Add the fonts you want to the pyportal's font dir and change the font ref below to match (paths to .bdf files)
3) Find the Purple Air sensor you want to query by going to www.purpleair.com and going to the map.
   On the map find a sensor near you. To find it's ID click on the sensor's circle and look at the URL.
   The sensor's ID will be a five digit number right after it says select= (i.e. ...select=60019...)
   Also make note of the name of the sensor in the box that pops up (although it's not critical)
4) Change the SENSOR_ID and SENSOR_NAME variables below to those of the sensor you want to query
5) Save this code file to your PyPortal

Note: The Purple Air raw data is given in raw PM2.5 which isn't the same
as the EPA Air Quality Index(AQI). Converting to the EPA numbers requires looking
up the values on an index list, but specifically the formula is:
AQI = ((epaHigherIndex-epaLowerIndex)/(rawHigherIndex-rawLowerIndex))*(rawPM - rawLowerIndex) + epaLowerIndex
Formula source: https://en.wikipedia.org/wiki/Air_quality_index
"""
import time
import board
from adafruit_pyportal import PyPortal

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Purple air sensors are scattered throughout your area, find the ID by visiting the site
# and mouse over the sensor to find the ID, click on it to find the name
# Purple air doesn't currently require an API key but they ask that you don't do too many requests an hour
SENSOR_ID = "19671"
SENSOR_NAME = "Civic Center(ish)"

# Set up where we'll be fetching data from
DATA_SOURCE = "https://www.purpleair.com/data.json?show="
DATA_SOURCE += SENSOR_ID
DATA_LOCATION = ["data", 0, 1]

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]

# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x550055,
                    text_font=cwd+"/fonts/ChunkFive-Regular-100.bdf",
                    text_position=(110, 110),
                    text_color=0x111111,
                    caption_text="AQI for "+SENSOR_NAME,
                    caption_font=cwd+"/fonts/Arial-16.bdf",
                    caption_position=(15, 220),
                    caption_color=0x000000,)

def convertToEPAAQI(value):
    """Converts raw PM2.5 data to EPA AQI values"""
    epaIndices = [(0,50),(51,100),(101,150),(151,200),(201,300), (301,500)]
    pm25Indices = [(0.0, 12.0),(12.1,35.4),(35.5,55.4),(55.5,150.4),(150.5,250.4),(250.5,350.4),(350.5,500.4)]

    epaMin, epaMax, pm25min, pm25max = 0, 0, 0, 0
    i = 0
    while i < len(pm25Indices):
        if (value >= min(pm25Indices[i])) and (value <= max(pm25Indices[i])):
            pm25min, pm25max = pm25Indices[i]
            epaMin, epaMax = epaIndices[i]       
        i += 1

    AQI = ((epaMax - epaMin)/(pm25max - pm25min)) * (value - pm25min) + epaMin

    return int(AQI)

while True:
    try:
        value = pyportal.fetch()

        AQI = convertToEPAAQI(value)
        pyportal.set_text(AQI,0)

        if 0 <= AQI <= 50:
            pyportal.set_background(0x66bb6a)  # good
        if 51 <= AQI <= 100:
            pyportal.set_background(0xffeb3b)  # moderate
        if 101 <= AQI <= 150:
            pyportal.set_background(0xf39c12)  # sensitive
        if 151 <= AQI <= 200:
            pyportal.set_background(0xff5722)  # unhealthy
        if 201 <= AQI <= 300:
            pyportal.set_background(0x8e24aa)  # very unhealthy
        if 301 <= AQI <= 500:
            pyportal.set_background(0xb71c1c ) # hazardous
        time.sleep(10*60)  # wait 10 minutes before getting again

    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
        time.sleep(5) # if we get a failure of the query, try again in five seconds
