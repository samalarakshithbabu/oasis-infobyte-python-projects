# Personal Health BMI Tracker

Comprehensive health monitoring application with advanced analytics and data visualization.

## Core Features

### Basic Functionality
- BMI computation using weight and height measurements
- Health status classification system
- Input validation with error management
- Personalized health recommendations

### Advanced Capabilities
- **Interactive GUI**: Modern interface built with Tkinter framework
- **Data Persistence**: SQLite database for long-term storage
- **Multi-User System**: Individual tracking for multiple users
- **Historical Analysis**: Complete record viewing functionality
- **Trend Visualization**: Dynamic charts showing health progression
- **Analytics Dashboard**: Interactive graphs with health zone indicators

## Setup Instructions

1. Install dependencies:
```bash
pip install matplotlib
```

2. Launch application:
```bash
python run_advanced_bmi.py
```

## Application Usage

### Health Calculator Tab
1. Input personal details (name, weight, height)
2. Click "Process Health Data" for BMI calculation
3. View results with health status and guidance
4. Data automatically saved to database

### Health Records Tab
1. Select user from dropdown menu
2. Click "Display Records" to view history
3. Browse chronological health data entries

### Health Analytics Tab
1. Choose user for analysis
2. Click "Create Visualization" for trend chart
3. Analyze BMI progression with health zone overlays

## Project Structure

- `bmi_calculator.py` - Command-line version
- `advanced_bmi_calculator.py` - Full GUI application
- `health_tracker.db` - Database file (auto-generated)
- `requirements.txt` - Python dependencies

## Health Classifications

- **Below Normal Weight**: BMI < 18.5
- **Healthy Weight Range**: BMI 18.5-24.9
- **Above Normal Weight**: BMI 25-29.9
- **Moderate Obesity**: BMI 30-34.9
- **Severe Obesity**: BMI 35-39.9
- **Extreme Obesity**: BMI ≥ 40

## Technical Implementation

- **Database**: SQLite for local data management
- **GUI Framework**: Tkinter with ttk styling
- **Visualization**: Matplotlib for interactive charts
- **Data Validation**: Comprehensive input verification
- **Error Management**: Robust exception handling