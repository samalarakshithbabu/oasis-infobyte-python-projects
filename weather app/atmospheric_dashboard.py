import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from datetime import datetime, timedelta
import geocoder
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import threading
import json

load_dotenv()

class AtmosphericMonitoringInterface:
    def __init__(self, root_window):
        self.main_window = root_window
        self.main_window.title("Atmospheric Monitoring Dashboard")
        self.main_window.geometry("850x750")
        self.main_window.configure(bg='#f0f8ff')
        
        # Configuration parameters
        self.api_credentials = os.getenv('OPENWEATHER_API_KEY')
        self.weather_service_url = "https://api.openweathermap.org/data/2.5"
        self.measurement_system = "metric"
        
        # Animation control variables
        self.loading_indicator_active = False
        self.animation_cycle_counter = 0
        
        self.initialize_user_interface()
        
    def initialize_user_interface(self):
        # Create tabbed interface for different views
        interface_notebook = ttk.Notebook(self.main_window)
        interface_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Current conditions tab
        self.current_conditions_panel = ttk.Frame(interface_notebook)
        interface_notebook.add(self.current_conditions_panel, text="🌡️ Current Conditions")
        self.configure_current_conditions_tab()
        
        # Extended forecast tab
        self.extended_forecast_panel = ttk.Frame(interface_notebook)
        interface_notebook.add(self.extended_forecast_panel, text="📊 Extended Forecast")
        self.configure_forecast_tab()
        
    def configure_current_conditions_tab(self):
        # Location input section
        location_input_container = ttk.Frame(self.current_conditions_panel)
        location_input_container.pack(pady=15, fill=tk.X, padx=25)
        
        ttk.Label(location_input_container, text="🌍 Geographic Location:", 
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.location_input_variable = tk.StringVar()
        location_text_field = ttk.Entry(location_input_container, 
                                       textvariable=self.location_input_variable, 
                                       width=35, font=("Segoe UI", 10))
        location_text_field.pack(side=tk.LEFT, padx=8)
        location_text_field.bind('<Return>', lambda event: self.fetch_current_atmospheric_data())
        
        ttk.Button(location_input_container, text="🔍 Analyze Weather", 
                  command=self.fetch_current_atmospheric_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(location_input_container, text="📍 Auto-Locate", 
                  command=self.activate_geolocation_service).pack(side=tk.LEFT, padx=5)
        
        # Status indicator
        self.system_status_variable = tk.StringVar(value="🟢 System Ready")
        self.status_indicator_label = ttk.Label(self.current_conditions_panel, 
                                               textvariable=self.system_status_variable,
                                               font=("Segoe UI", 9))
        self.status_indicator_label.pack(pady=8)
        
        # Weather information display area
        self.atmospheric_data_container = ttk.LabelFrame(self.current_conditions_panel, 
                                                        text="🌤️ Atmospheric Conditions", 
                                                        padding=25)
        self.atmospheric_data_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
    def configure_forecast_tab(self):
        # Forecast controls
        forecast_control_panel = ttk.Frame(self.extended_forecast_panel)
        forecast_control_panel.pack(pady=15, fill=tk.X, padx=25)
        
        ttk.Label(forecast_control_panel, text="🌍 Location for Forecast:", 
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.forecast_location_variable = tk.StringVar()
        forecast_input_field = ttk.Entry(forecast_control_panel, 
                                        textvariable=self.forecast_location_variable, 
                                        width=35, font=("Segoe UI", 10))
        forecast_input_field.pack(side=tk.LEFT, padx=8)
        
        ttk.Button(forecast_control_panel, text="📈 Generate Forecast", 
                  command=self.generate_extended_forecast).pack(side=tk.LEFT, padx=5)
        
        # Forecast display container
        self.forecast_visualization_area = ttk.Frame(self.extended_forecast_panel)
        self.forecast_visualization_area.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
    def initiate_loading_sequence(self, status_message="Processing"):
        """Start animated loading indicator with custom message"""
        self.loading_indicator_active = True
        self.animation_cycle_counter = 0
        self.cycle_loading_animation(status_message)
        
    def cycle_loading_animation(self, status_message):
        """Animate loading dots in a cycling pattern"""
        if self.loading_indicator_active:
            animation_dots = "⚫" * (self.animation_cycle_counter % 4)
            self.system_status_variable.set(f"🔄 {status_message}{animation_dots}")
            self.animation_cycle_counter += 1
            self.main_window.after(600, lambda: self.cycle_loading_animation(status_message))
            
    def terminate_loading_sequence(self):
        """Stop the loading animation"""
        self.loading_indicator_active = False
        
    def activate_geolocation_service(self):
        """Automatically detect user's geographic location"""
        def execute_location_detection():
            try:
                self.initiate_loading_sequence("🌍 Detecting geographic coordinates")
                geolocation_service = geocoder.ip('me')
                if geolocation_service.ok:
                    detected_location = f"{geolocation_service.city}, {geolocation_service.country}"
                    self.location_input_variable.set(detected_location)
                    self.terminate_loading_sequence()
                    self.system_status_variable.set(f"📍 Location identified: {detected_location}")
                    self.fetch_current_atmospheric_data()
                else:
                    self.terminate_loading_sequence()
                    self.system_status_variable.set("❌ Geolocation service unavailable")
            except Exception as location_error:
                self.terminate_loading_sequence()
                self.system_status_variable.set(f"⚠️ Location Error: {str(location_error)}")
                
        threading.Thread(target=execute_location_detection, daemon=True).start()
        
    def fetch_current_atmospheric_data(self):
        """Retrieve current weather conditions for specified location"""
        target_location = self.location_input_variable.get().strip()
        if not target_location:
            messagebox.showerror("Input Error", "Please specify a geographic location")
            return
            
        def execute_weather_retrieval():
            try:
                self.initiate_loading_sequence("🌤️ Retrieving atmospheric data")
                
                # Current weather API call
                current_weather_params = {
                    'q': target_location,
                    'appid': self.api_credentials,
                    'units': self.measurement_system
                }
                
                current_response = requests.get(f"{self.weather_service_url}/weather", 
                                              params=current_weather_params, timeout=12)
                current_response.raise_for_status()
                current_weather_data = current_response.json()
                
                # Hourly forecast API call
                latitude, longitude = current_weather_data['coord']['lat'], current_weather_data['coord']['lon']
                hourly_forecast_params = {
                    'lat': latitude,
                    'lon': longitude,
                    'appid': self.api_credentials,
                    'units': self.measurement_system
                }
                
                hourly_response = requests.get(f"{self.weather_service_url}/forecast", 
                                             params=hourly_forecast_params, timeout=12)
                hourly_response.raise_for_status()
                hourly_forecast_data = hourly_response.json()
                
                self.terminate_loading_sequence()
                self.render_atmospheric_conditions(current_weather_data, hourly_forecast_data)
                self.system_status_variable.set("✅ Atmospheric data successfully retrieved")
                
            except Exception as retrieval_error:
                self.terminate_loading_sequence()
                self.system_status_variable.set(f"❌ Retrieval Error: {str(retrieval_error)}")
                
        threading.Thread(target=execute_weather_retrieval, daemon=True).start()
        
    def render_atmospheric_conditions(self, current_conditions, hourly_predictions):
        """Display current weather conditions with visual elements"""
        # Clear previous display content
        for display_widget in self.atmospheric_data_container.winfo_children():
            display_widget.destroy()
            
        atmospheric_metrics = current_conditions['main']
        weather_description = current_conditions['weather'][0]
        
        # Main information layout
        primary_info_frame = ttk.Frame(self.atmospheric_data_container)
        primary_info_frame.pack(fill=tk.X, pady=15)
        
        # Temperature display section
        temperature_display_frame = ttk.Frame(primary_info_frame)
        temperature_display_frame.pack(side=tk.LEFT)
        
        temperature_value_label = ttk.Label(temperature_display_frame, 
                                           text=f"{atmospheric_metrics['temp']:.1f}°C", 
                                           font=("Segoe UI", 28, "bold"),
                                           foreground="#2E86AB")
        temperature_value_label.pack()
        
        weather_description_label = ttk.Label(temperature_display_frame, 
                                            text=weather_description['description'].title(), 
                                            font=("Segoe UI", 14),
                                            foreground="#A23B72")
        weather_description_label.pack()
        
        # Detailed metrics section
        metrics_display_frame = ttk.Frame(primary_info_frame)
        metrics_display_frame.pack(side=tk.RIGHT, padx=25)
        
        atmospheric_details = [
            f"🌡️ Perceived Temperature: {atmospheric_metrics['feels_like']:.1f}°C",
            f"💧 Humidity Level: {atmospheric_metrics['humidity']}%",
            f"📊 Atmospheric Pressure: {atmospheric_metrics['pressure']} hPa",
            f"📍 Geographic Location: {current_conditions['name']}, {current_conditions['sys']['country']}"
        ]
        
        for detail_metric in atmospheric_details:
            ttk.Label(metrics_display_frame, text=detail_metric, 
                     font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
            
        self.generate_temperature_visualization(hourly_predictions)
        
    def generate_temperature_visualization(self, hourly_forecast_data):
        """Create temperature trend visualization chart"""
        time_intervals = []
        temperature_readings = []
        
        # Extract next 24 hours of data (8 intervals of 3 hours each)
        for interval_index in range(min(8, len(hourly_forecast_data['list']))):
            forecast_interval = hourly_forecast_data['list'][interval_index]
            interval_timestamp = datetime.fromtimestamp(forecast_interval['dt'])
            time_intervals.append(interval_timestamp.strftime('%H:%M'))
            temperature_readings.append(forecast_interval['main']['temp'])
            
        # Create matplotlib visualization
        visualization_figure, chart_axis = plt.subplots(figsize=(11, 4))
        chart_axis.plot(time_intervals, temperature_readings, 
                       marker='●', linewidth=3, markersize=8, 
                       color='#2E86AB', markerfacecolor='#F18F01')
        chart_axis.set_title('24-Hour Temperature Trend Analysis', 
                           fontsize=14, fontweight='bold', color='#2E86AB')
        chart_axis.set_ylabel('Temperature (°C)', fontsize=12, color='#A23B72')
        chart_axis.grid(True, alpha=0.4, linestyle='--')
        chart_axis.set_facecolor('#f8f9fa')
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()
        
        # Embed chart in tkinter interface
        chart_canvas = FigureCanvasTkinter(visualization_figure, self.atmospheric_data_container)
        chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=15)
        
    def generate_extended_forecast(self):
        """Generate multi-day weather forecast"""
        forecast_location = self.forecast_location_variable.get().strip()
        if not forecast_location:
            messagebox.showerror("Input Error", "Please specify location for forecast")
            return
            
        def execute_forecast_generation():
            try:
                forecast_parameters = {
                    'q': forecast_location,
                    'appid': self.api_credentials,
                    'units': self.measurement_system
                }
                
                forecast_response = requests.get(f"{self.weather_service_url}/forecast", 
                                               params=forecast_parameters, timeout=12)
                forecast_response.raise_for_status()
                forecast_dataset = forecast_response.json()
                
                self.visualize_extended_forecast(forecast_dataset)
                
            except Exception as forecast_error:
                messagebox.showerror("Forecast Error", f"Unable to generate forecast: {str(forecast_error)}")
                
        threading.Thread(target=execute_forecast_generation, daemon=True).start()
        
    def visualize_extended_forecast(self, forecast_dataset):
        """Display multi-day forecast visualization"""
        # Clear previous forecast display
        for forecast_widget in self.forecast_visualization_area.winfo_children():
            forecast_widget.destroy()
            
        # Organize forecast data by calendar days
        daily_forecast_groups = {}
        for forecast_entry in forecast_dataset['list']:
            forecast_date = datetime.fromtimestamp(forecast_entry['dt']).date()
            if forecast_date not in daily_forecast_groups:
                daily_forecast_groups[forecast_date] = []
            daily_forecast_groups[forecast_date].append(forecast_entry)
            
        # Display forecast for next 5 days
        for day_index, (forecast_date, daily_entries) in enumerate(list(daily_forecast_groups.items())[:5]):
            daily_forecast_frame = ttk.LabelFrame(self.forecast_visualization_area, 
                                                 text=f"📅 {forecast_date.strftime('%A, %B %d')}", 
                                                 padding=15)
            daily_forecast_frame.pack(fill=tk.X, pady=8)
            
            # Calculate daily temperature range
            daily_temperatures = [entry['main']['temp'] for entry in daily_entries]
            minimum_temperature = min(daily_temperatures)
            maximum_temperature = max(daily_temperatures)
            
            # Determine predominant weather condition
            weather_conditions = [entry['weather'][0]['description'] for entry in daily_entries]
            predominant_condition = max(set(weather_conditions), key=weather_conditions.count)
            
            # Display daily summary
            daily_summary = f"🌡️ High: {maximum_temperature:.1f}°C | Low: {minimum_temperature:.1f}°C | Conditions: {predominant_condition.title()}"
            ttk.Label(daily_forecast_frame, text=daily_summary, 
                     font=("Segoe UI", 11)).pack()

def launch_atmospheric_dashboard():
    """Initialize and launch the atmospheric monitoring application"""
    root_application = tk.Tk()
    atmospheric_interface = AtmosphericMonitoringInterface(root_application)
    root_application.mainloop()

if __name__ == "__main__":
    launch_atmospheric_dashboard()