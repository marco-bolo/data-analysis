import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('./eternal-ruler-417805-abc596523486.json', scope)

# Authorize the client using the credentials
client = gspread.authorize(credentials)

# Create a new Google Sheet
new_sheet = client.open('MBO_test')

# Access the first sheet of the new Google Sheet
sheet = new_sheet.sheet1

# Write data to the sheet
data = [
    ["Name", "Age", "Location"],
    ["John", 30, "New York"],
    ["Alice", 25, "London"],
    ["Bob", 35, "Paris"]
]
for row in data:
    sheet.append_row(row)

print("Data has been written to the new Google Sheet.")
