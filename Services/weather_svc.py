from Services.config.config import WX_API_KEY, WX_LOCATION, WX_UNITS_TEMP, WX_UNITS_WIND
from pyowm import OWM


class Weather:
    def __init__(self, api_key=None, units_temp=None, units_wind=None):
        self.manager = OWM(api_key or WX_API_KEY).weather_manager()
        self.default_location = WX_LOCATION
        self.units_temp = units_temp or WX_UNITS_TEMP
        self.units_wind = units_wind or WX_UNITS_WIND
        
    def get_weather_data(self, weather):
        return {
            "max": weather.temperature(self.units_temp)["temp_max"],
            "min": weather.temperature(self.units_temp)["temp_min"],
            "temp": weather.temperature(self.units_temp)["temp"],
            "wind": weather.wind(self.units_wind)["speed"],
            "pressure": weather.pressure["press"],
            "humidity": weather.humidity,
            "status": weather.detailed_status,
            "sun_rise": weather.srise_time,
            "sun_set": weather.sset_time,
            "rain": weather.rain,
            "time": weather.ref_time,
        }
        
    def current(self, location=None):
        try:
            obs = self.manager.weather_at_place(location or self.default_location)
            weather = obs.weather
            
            res = self.get_weather_data(weather)
            res["location"] = f"{obs.location.name} {obs.location.country}"
            return res
        except Exception as e:
            print(f"{location} not found")
        
    def forecast(self, location=None, interval='3h'):
        fcst = self.manager.forecast_at_place(location or self.default_location, interval)
        location = f"{fcst.forecast.location.name} {fcst.forecast.location.country}"
        
        return [
            {**self.get_weather_data(weather), **{"location": location}} for weather in fcst.forecast.weathers
        ]