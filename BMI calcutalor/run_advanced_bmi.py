#!/usr/bin/env python3
"""
Launcher for Advanced BMI Calculator
Run this file to start the GUI application
"""

try:
    from advanced_bmi_calculator import main
    print("Starting Advanced BMI Calculator...")
    main()
except ImportError as e:
    print(f"Error: Missing dependency - {e}")
    print("Please install required packages:")
    print("pip install matplotlib")
except Exception as e:
    print(f"Error starting application: {e}")
    input("Press Enter to exit...")