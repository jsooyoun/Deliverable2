import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Path to the CSV file (update this with the correct relative path)
csv_file = 'meets/37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.csv'

# Read and parse the CSV data
with open(csv_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Extract meet details and comments
meet_name = lines[0].strip()
meet_date = lines[1].strip()
team_results_link = lines[2].strip()
race_comments = lines[3].strip()

# Find the start and end of team and athlete results sections
teams_start = lines.index('Place,Team,Score\n') + 1
athletes_start = lines.index('Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic\n') + 1

# Read team results chunk from CSV
team_results_lines = lines[teams_start:athletes_start-1]
team_results = pd.DataFrame([line.strip().split(',') for line in team_results_lines], columns=['Place', 'Team', 'Score'])

# Read athlete results chunk from CSV
athlete_results_lines = lines[athletes_start:]
athlete_results = pd.DataFrame([line.strip().split(',') for line in athlete_results_lines], columns=['Place', 'Grade', 'Name', 'Athlete Link', 'Time', 'Team', 'Team Link', 'Profile Pic'])

# Transform data into dictionary format for template rendering
teams = team_results.to_dict(orient='records')
athletes = athlete_results.to_dict(orient='records')

# Setup Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader(searchpath="."))
template = env.get_template('template.html')

# Context data to pass to the template
context = {
    'meet_name': meet_name,
    'meet_date': meet_date,
    'team_results_link': team_results_link,
    'race_comments': race_comments,
    'teams': teams,
    'athletes': athletes
}

# Render the HTML content with context data
html_content = template.render(context)

# Write rendered HTML to 'index.html'
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML file 'index.html' generated successfully!")