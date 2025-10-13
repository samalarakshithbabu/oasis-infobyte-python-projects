# Voice Assistant Project

A complete voice assistant implementation with basic and advanced features.

## Features

### Basic Features
- Speech recognition and text-to-speech
- Voice commands for time, date, greetings
- Web search and Wikipedia integration
- Natural conversation flow

### Advanced Features
- Natural Language Processing (NLP)
- Weather information via API
- Email sending functionality
- Smart reminder system
- Custom command creation

## Files

- `voice_assistant.py` - Complete voice assistant with all features
- `demo.py` - Requirements demonstration script
- `requirements.txt` - Dependencies
- `.env` - Configuration file

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Voice Assistant (Main)
```bash
python voice_assistant.py
```

### Demo (No Voice Required)
```bash
python demo.py
```

## Configuration

Create `.env` file with:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
WEATHER_API_KEY=your_openweathermap_key
```

## Voice Commands

- "Hello" - Greeting
- "What time is it?" - Current time
- "What's the date?" - Current date
- "Weather in [city]" - Weather information
- "Send email to [address]" - Email functionality
- "Remind me in [minutes] minutes" - Set reminder
- "Turn on [room] light" - Smart home control
- "Search for [query]" - Web search
- "Tell me about [topic]" - Wikipedia search
- "Exit" - Close assistant

## Project Status

✅ All requirements implemented and tested
✅ Beginner features: Greetings, Time, Date, Web Search, Wikipedia
✅ Advanced features: NLP, Email, Weather, Smart Home, Security
✅ Key concepts: Speech Recognition, Task Automation, Error Handling
✅ Minimal code implementation - no unnecessary features