def compute_body_mass_index(mass_kg, height_m):
    return mass_kg / (height_m * height_m)

def determine_health_status(bmi_value):
    if bmi_value < 18.5: return "Below Normal Weight"
    elif bmi_value < 25: return "Healthy Weight Range"
    elif bmi_value < 30: return "Above Normal Weight"
    elif bmi_value < 35: return "Moderate Obesity"
    elif bmi_value < 40: return "Severe Obesity"
    else: return "Extreme Obesity"

def collect_user_data(message, lower_limit=0, upper_limit=None):
    while True:
        try:
            user_input = float(input(message))
            if user_input <= lower_limit or (upper_limit and user_input > upper_limit):
                print(f"Please enter value between {lower_limit} and {upper_limit or 'no limit'}")
                continue
            return user_input
        except ValueError:
            print("Invalid input. Please enter a numeric value")

def execute_bmi_program():
    print("Personal Health BMI Assessment Tool")
    
    body_weight = collect_user_data("Enter your weight in kg: ", 1, 500)
    body_height = collect_user_data("Enter your height in meters: ", 0.5, 2.5)
    
    calculated_bmi = compute_body_mass_index(body_weight, body_height)
    health_classification = determine_health_status(calculated_bmi)
    
    print(f"\nYour BMI Result: {calculated_bmi:.2f} | Classification: {health_classification}")
    
    health_recommendations = {
        "Below Normal Weight": "Focus on healthy weight gain strategies",
        "Healthy Weight Range": "Continue your current healthy habits",
    }
    print(health_recommendations.get(health_classification, "Consider consulting healthcare professionals"))

if __name__ == "__main__":
    execute_bmi_program()