from langchain.agents import Tool

def calculate_bmi(text):
    try:
        weight, height = map(float, text.split())
        bmi = weight / (height/100)**2
        return f"BMI: {bmi:.2f} — {'Overweight' if bmi > 25 else 'Normal' if bmi >= 18.5 else 'Underweight'}"
    except:
        return "Input format: '<weight_kg> <height_cm>'"

tool = Tool(
    name="BMI Calculator",
    func=calculate_bmi,
    description="Calculates BMI from weight (kg) and height (cm)."
)