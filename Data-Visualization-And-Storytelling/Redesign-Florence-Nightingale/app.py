from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)


# --- Read Data ---
df = pd.read_csv(
    'C:\\Users\\afeen\\Documents\\MBAI\\Business Analytics\\FlaskProjects\\Data Visualization and Storytelling\\Assignment2\\data\\gabby_nightingale.csv'
)

df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Date'] < '1855-04-01'].copy()

# print(df.columns)
# print(df.head())

# Ensure Month and Year exist
if 'Month' not in df.columns or 'Year' not in df.columns:
    df['Month'] = df['Date'].dt.strftime('%b')
    df['Year'] = df['Date'].dt.year

@app.route('/')
def home():
    # Home page with links to all charts
    return render_template('index.html')

@app.route('/nightingale_coxcomb')
def nightingale():
    # Render the Nightingale chart
    return render_template('nightingale_chart.html')

@app.route('/get_dots/<death_type>/<month>/<year>')
def get_dots(death_type, month, year):
    """Return dots data for selected death type, month, and year."""
    # Convert year to integer to match df['Year'] type
    year_int = int(year)  
    # Filter the dataframe
    filtered = df[(df['Year'] == year_int) & (df['Month'] == month)]
    # Get the count for the selected death type
    count = int(filtered[death_type].values[0]) if not filtered.empty else 0   
    # Create list of dots
    dots = [{"x": i, "y": 1} for i in range(count)]
    
    return jsonify(dots)

@app.route('/nightingale_Impact_after_reform')
def nightingale_line():
    # Serve the line chart HTML from static folder
    return render_template('nightingale_impact_after_reform.html')

if __name__ == '__main__':
    app.run(debug=True)
