import requests
import sys
import os
from datetime import datetime

class ClimateForecastSystem:
    def __init__(self, authentication_token=None):
        self.auth_token = authentication_token or os.environ.get('OPENWEATHER_API_KEY')
        self.weather_endpoint = "http://api.openweathermap.org/data/2.5/weather"
        self.temperature_scale = "metric"
        
    def verify_credentials(self):
        if not self.auth_token:
            print("Authentication Error: Missing API credentials!")
            print("Setup Instructions:")
            print("• Obtain free API key: https://openweathermap.org/api")
            print("• Set environment variable: OPENWEATHER_API_KEY")
            print("• Alternative: python climate_tracker.py --token YOUR_KEY")
            return False
        return True
    
    def retrieve_climate_data(self, geographic_location):
        if not self.verify_credentials():
            return None
            
        request_parameters = {
            'q': geographic_location,
            'appid': self.auth_token,
            'units': self.temperature_scale
        }
        
        try:
            api_response = requests.get(self.weather_endpoint, params=request_parameters, timeout=15)
            api_response.raise_for_status()
            return api_response.json()
        except requests.exceptions.RequestException as network_error:
            print(f"Network Error: {network_error}")
            return None
    
    def extract_climate_metrics(self, raw_climate_data):
        if not raw_climate_data:
            return None
            
        try:
            atmospheric_data = raw_climate_data['main']
            weather_conditions = raw_climate_data['weather'][0]
            wind_metrics = raw_climate_data.get('wind', {})
            
            return {
                'current_temperature': atmospheric_data['temp'],
                'perceived_temperature': atmospheric_data['feels_like'],
                'moisture_level': atmospheric_data['humidity'],
                'atmospheric_pressure': atmospheric_data['pressure'],
                'weather_summary': weather_conditions['description'].title(),
                'wind_velocity': wind_metrics.get('speed', 0),
                'wind_bearing': wind_metrics.get('deg', 0),
                'location_name': raw_climate_data['name'],
                'country_identifier': raw_climate_data['sys']['country'],
                'data_timestamp': datetime.fromtimestamp(raw_climate_data['dt'])
            }
        except KeyError as missing_field:
            print(f"Data Processing Error: Missing field {missing_field}")
            return None
    
    def present_climate_information(self, climate_metrics):
        if not climate_metrics:
            return
            
        print("\n" + "="*60)
        print(f"Climate Report: {climate_metrics['location_name']}, {climate_metrics['country_identifier']}")
        print(f"Last Updated: {climate_metrics['data_timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        degree_symbol = "°C" if self.temperature_scale == "metric" else "°F"
        
        print(f"Current Temperature: {climate_metrics['current_temperature']:.1f}{degree_symbol}")
        print(f"Feels Like: {climate_metrics['perceived_temperature']:.1f}{degree_symbol}")
        print(f"Conditions: {climate_metrics['weather_summary']}")
        print(f"Humidity: {climate_metrics['moisture_level']}%")
        print(f"Pressure: {climate_metrics['atmospheric_pressure']} hPa")
        print(f"Wind Speed: {climate_metrics['wind_velocity']} m/s")
        
        if climate_metrics['wind_bearing']:
            compass_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            direction_index = int((climate_metrics['wind_bearing'] + 11.25) / 22.5) % 16
            print(f"Wind Direction: {compass_directions[direction_index]}")
        
        print("="*60)
    
    def execute_interactive_session(self):
        print("🌤️ Climate Forecast System")
        print("Commands: Enter location | 'scale' (toggle units) | 'exit'")
        
        while True:
            try:
                user_command = input("\n📍 Enter location: ").strip()
                
                if user_command.lower() == 'exit':
                    print("Session terminated. Goodbye!")
                    break
                elif user_command.lower() == 'scale':
                    self.temperature_scale = "imperial" if self.temperature_scale == "metric" else "metric"
                    scale_name = "Fahrenheit" if self.temperature_scale == "imperial" else "Celsius"
                    print(f"Temperature scale changed to {scale_name}")
                    continue
                
                if not user_command:
                    continue
                
                print(f"🔍 Retrieving climate data for {user_command}...")
                climate_response = self.retrieve_climate_data(user_command)
                
                if climate_response:
                    processed_data = self.extract_climate_metrics(climate_response)
                    self.present_climate_information(processed_data)
                else:
                    print("❌ Unable to retrieve climate data. Verify location and try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as unexpected_error:
                print(f"⚠️ Unexpected error: {unexpected_error}")

def initialize_application():
    import argparse
    
    argument_parser = argparse.ArgumentParser(description='Climate Forecast System - Real-time weather information')
    argument_parser.add_argument('--token', help='OpenWeatherMap authentication token')
    argument_parser.add_argument('--place', help='Geographic location for weather query')
    argument_parser.add_argument('--scale', choices=['metric', 'imperial'], default='metric',
                               help='Temperature measurement system (metric=Celsius, imperial=Fahrenheit)')
    
    parsed_args = argument_parser.parse_args()
    
    climate_system = ClimateForecastSystem(parsed_args.token)
    climate_system.temperature_scale = parsed_args.scale
    
    if parsed_args.place:
        print(f"🔍 Retrieving climate data for {parsed_args.place}...")
        climate_response = climate_system.retrieve_climate_data(parsed_args.place)
        if climate_response:
            processed_data = climate_system.extract_climate_metrics(climate_response)
            climate_system.present_climate_information(processed_data)
        else:
            print("❌ Unable to retrieve climate data.")
    else:
        climate_system.execute_interactive_session()

if __name__ == "__main__":
    initialize_application()