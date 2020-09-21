# PyPortal-Purple-Air

Modified Adafruit's PyPortal Air Quality Monitor project to work with purpleair.com

Original Adafruit tutorial here:
https://learn.adafruit.com/pyportal-air-quality-display

# Setup:
1) Follow the steps in their tutorial to setup your PyPortal and add the libraries they suggest
2) Add the fonts you want to the pyportal's font dir and change the font ref below to match (paths to .bdf files)
3) Find the Purple Air sensor you want to query by going to www.purpleair.com and going to the map.
   On the map find a sensor near you. To find it's ID click on the sensor's circle and look at the URL.
   The sensor's ID will be a five digit number right after it says select= (i.e. ...select=60019...)
   Also make note of the name of the sensor in the box that pops up (although it's not critical)
4) Change the SENSOR_ID and SENSOR_NAME variables below to those of the sensor you want to query
5) Save this code file to your PyPortal

# Note: 
The Purple Air raw data is given in raw PM2.5 which isn't the same
as the EPA Air Quality Index(AQI). Converting to the EPA numbers requires looking
up the values on an index list, but specifically the formula is:
AQI = ((epaHigherIndex-epaLowerIndex)/(rawHigherIndex-rawLowerIndex))*(rawPM - rawLowerIndex) + epaLowerIndex
Formula source: https://en.wikipedia.org/wiki/Air_quality_index
