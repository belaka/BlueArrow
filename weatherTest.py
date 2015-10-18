import pywapi
import pprint
pp = pprint.PrettyPrinter(indent=4)

result = pywapi.get_weather_from_yahoo('RSXX0199', 'metric')
pp.pprint(result)
