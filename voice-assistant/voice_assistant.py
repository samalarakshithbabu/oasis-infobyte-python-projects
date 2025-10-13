#!/usr/bin/env python3

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import smtplib
import requests
import os
import re
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class VoiceAssistant:
    def __init__(self):
        # Speech components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # NLP patterns
        self.patterns = {
            'greeting': [r'hello', r'hi', r'hey'],
            'time': [r'time', r'clock'],
            'date': [r'date', r'today'],
            'weather': [r'weather', r'temperature'],
            'email': [r'email', r'send.*message'],
            'reminder': [r'remind', r'notification'],
            'search': [r'search', r'find'],
            'info': [r'tell.*about', r'what.*is'],
            'lights': [r'turn.*light', r'lights?.*on', r'lights?.*off'],
            'exit': [r'exit', r'quit', r'bye']
        }
        
        # Smart home devices
        self.devices = {
            'lights': {'living_room': False, 'bedroom': False, 'kitchen': False},
            'thermostat': {'temperature': 22}
        }
        
        # Custom commands
        self.custom_commands = {}
    
    def setup_voice(self):
        """Setup voice properties"""
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 150)
        except:
            pass
    
    def speak(self, text):
        """Text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Speech recognition"""
        try:
            with sr.Microphone() as mic:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = self.recognizer.listen(mic, timeout=3, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text.lower()
        except:
            return ""
    
    def sanitize_input(self, text):
        """Security: sanitize user input"""
        if not text:
            return ""
        sanitized = re.sub(r'[<>"\';\\]', '', str(text))
        return sanitized[:500].strip()
    
    def get_intent(self, text):
        """NLP: Get command intent"""
        text = text.lower().strip()
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        return 'unknown'
    
    def extract_params(self, text, intent):
        """NLP: Extract parameters"""
        params = {}
        text = text.lower()
        
        if intent == 'weather':
            match = re.search(r'weather.*in\s+([a-zA-Z\s]+)', text)
            if match:
                params['city'] = match.group(1).strip()
        
        elif intent == 'email':
            match = re.search(r'(?:email|send).*to\s+([^\s]+@[^\s]+)', text)
            if match:
                params['email'] = match.group(1)
        
        elif intent == 'reminder':
            time_match = re.search(r'(\d+)\s*minutes?', text)
            if time_match:
                params['minutes'] = int(time_match.group(1))
        
        elif intent == 'lights':
            room_match = re.search(r'(?:living room|bedroom|kitchen)', text)
            action_match = re.search(r'(on|off)', text)
            if room_match:
                params['room'] = room_match.group(0).replace(' ', '_')
            if action_match:
                params['action'] = action_match.group(0)
        
        elif intent in ['search', 'info']:
            patterns = [r'search.*for\s+(.+)', r'tell.*about\s+(.+)', r'what.*is\s+(.+)']
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    params['query'] = match.group(1).strip()
                    break
        
        return params
    
    def get_time(self):
        """Get current time"""
        return datetime.datetime.now().strftime("%I:%M %p")
    
    def get_date(self):
        """Get current date"""
        return datetime.datetime.now().strftime("%A, %B %d, %Y")
    
    def web_search(self, query):
        """Web search"""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching for: {query}"
    
    def get_wikipedia_info(self, topic):
        """Wikipedia search"""
        try:
            summary = wikipedia.summary(topic, sentences=2)
            return f"Here's what I found about {topic}: {summary}"
        except:
            return f"No information found for {topic}"
    
    def send_email(self, to_email, subject="Voice Assistant Message", body="Hello from voice assistant"):
        """Send email"""
        try:
            # Security validation
            to_email = self.sanitize_input(to_email)
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', to_email):
                return "Invalid email format"
            
            email_user = os.getenv('EMAIL_USER')
            email_pass = os.getenv('EMAIL_PASS')
            
            if not email_user or not email_pass:
                return "Email not configured"
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = email_user
            msg['To'] = to_email
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(email_user, email_pass)
                server.send_message(msg)
            
            return f"Email sent to {to_email}"
        except Exception as e:
            return f"Email failed: {str(e)}"
    
    def get_weather(self, city):
        """Get weather information"""
        try:
            city = self.sanitize_input(city)
            api_key = os.getenv('WEATHER_API_KEY')
            if not api_key:
                return "Weather API key missing"
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"{city}: {temp}°C, {desc}"
            return f"Weather unavailable for {city}"
        except Exception as e:
            return f"Weather error: {str(e)}"
    
    def control_lights(self, room, action):
        """Smart home: control lights"""
        if room in self.devices['lights']:
            state = action == 'on'
            self.devices['lights'][room] = state
            return f"{room.replace('_', ' ')} light turned {action}"
        return f"Room '{room}' not found"
    
    def set_reminder(self, minutes, message="Reminder"):
        """Set reminder (simplified)"""
        return f"Reminder set for {minutes} minutes: {message}"
    
    def add_custom_command(self, trigger, response):
        """Customization: add custom command"""
        self.custom_commands[trigger.lower()] = response
        return f"Custom command '{trigger}' added"
    
    def process_command(self, text):
        """Main command processing"""
        if not text:
            return True
        
        # Security check
        text = self.sanitize_input(text)
        
        # Get intent and parameters
        intent = self.get_intent(text)
        params = self.extract_params(text, intent)
        
        # Process commands
        if intent == 'greeting':
            self.speak("Hello! How can I help you?")
        
        elif intent == 'time':
            self.speak(f"Current time: {self.get_time()}")
        
        elif intent == 'date':
            self.speak(f"Today's date: {self.get_date()}")
        
        elif intent == 'weather':
            if 'city' in params:
                result = self.get_weather(params['city'])
                self.speak(result)
            else:
                self.speak("Which city?")
        
        elif intent == 'email':
            if 'email' in params:
                result = self.send_email(params['email'])
                self.speak(result)
            else:
                self.speak("What email address?")
        
        elif intent == 'reminder':
            if 'minutes' in params:
                result = self.set_reminder(params['minutes'])
                self.speak(result)
            else:
                self.speak("How many minutes?")
        
        elif intent == 'lights':
            if 'room' in params and 'action' in params:
                result = self.control_lights(params['room'], params['action'])
                self.speak(result)
            else:
                self.speak("Specify room and action")
        
        elif intent == 'search':
            if 'query' in params:
                result = self.web_search(params['query'])
                self.speak(result)
            else:
                self.speak("What to search for?")
        
        elif intent == 'info':
            if 'query' in params:
                result = self.get_wikipedia_info(params['query'])
                self.speak(result)
            else:
                self.speak("What topic?")
        
        elif intent == 'exit':
            self.speak("Goodbye!")
            return False
        
        else:
            # Check custom commands
            if text in self.custom_commands:
                self.speak(self.custom_commands[text])
            else:
                self.speak("I don't understand that command")
        
        return True
    
    def run(self):
        """Main assistant loop"""
        self.speak("Voice assistant ready!")
        
        while True:
            try:
                command = self.listen()
                if not self.process_command(command):
                    break
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()