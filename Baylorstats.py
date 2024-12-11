from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# Website URL and headers
url = 'https://cfbstats.com/2024/team/51/index.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

# Fetch webpage
req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

stats_table = soup.find('table', {'class': 'team-statistics'})
if not stats_table:
    raise ValueError("Unable to locate the table with class 'team-statistics'. Check the webpage structure.")

stats = {
    "Scoring Points/Game": "Scoring:  Points/Game",
    "Passing Yards": "Passing:  Yards",
    "3rd Down Conversion %": "3rd Down Conversions: Conversion %",
    "Field Goals Success %": "Field Goals:  Success %",
}
parsed_stats = {stat: [] for stat in stats.keys()}
years = list(range(2016, 2025))

def extract_stat(stat_name):
    row = stats_table.find('td', string=stat_name)
    if not row:
        print(f"Warning: {stat_name} not found in the table.")
        return []
    tds = row.find_next_siblings('td')
    if not tds:
        return []
    try:
        return [float(td.text.strip().replace(',', '').replace('%', '')) for td in tds[:1]]
    except ValueError:
        return []

for stat_key, stat_name in stats.items():
    parsed_stats[stat_key] = extract_stat(stat_name)

print("\nParsed Stats:")
for stat_name, values in parsed_stats.items():
    print(f"{stat_name}: {values}")
    if not values:
        print(f"Warning: No data found for {stat_name}. Check the webpage structure.")

print("\nBest and Worst Years Analysis:")
for stat_name, values in parsed_stats.items():
    if values:
        best_value = max(values)
        worst_value = min(values)
        best_year = years[values.index(best_value)]
        worst_year = years[values.index(worst_value)]
        print(f"\n{stat_name}:")
        print(f"  Best Year: {best_year} ({best_value})")
        print(f"  Worst Year: {worst_year} ({worst_value})")

schedule_table = soup.find('table', {'class': 'team-schedule'})
if not schedule_table:
    raise ValueError("Unable to locate the schedule table with class 'team-schedule'. Check the webpage structure.")

rows = schedule_table.find_all('tr')[1:]  
attendance_data = {}

for row in rows:
    cells = row.find_all('td')
    if len(cells) < 5:
        continue
    opponent = cells[1].text.strip()
    attendance = cells[4].text.strip().replace(',', '')

    try:
        attendance = int(attendance)
        if opponent in attendance_data:
            attendance_data[opponent] += attendance
        else:
            attendance_data[opponent] = attendance
    except ValueError:
        continue  


sorted_attendance = sorted(attendance_data.items(), key=lambda x: x[1], reverse=True)
top_5_teams = sorted_attendance[:5]

#plotly data
teams = [team[0] for team in top_5_teams]
attendances = [team[1] for team in top_5_teams]

#bar chart
fig = go.Figure(data=[go.Bar(x=teams, y=attendances, marker_color='green')])
fig.update_layout(
    title='Top 5 Teams with Highest Attendance Against Baylor',
    xaxis_title='Teams',
    yaxis_title='Total Attendance',
    template='plotly_white',
)
fig.show()

print("\nTop 5 Teams with Highest Attendance Against Baylor:")
for team, attendance in top_5_teams:
   