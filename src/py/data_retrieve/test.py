import pysheets
import pandas as pd
from rdflib import Graph, Namespace, URIRef
import gspread
from oauth2client.service_account import ServiceAccountCredentials

df = pd.read_csv('src/py/data_retrieve/MARCO-BOLO_Metadata_Dataset_Record_WP5.csv')

marineinfo_subjects = [ link.replace("http://www.emodnet-biology.eu/data-catalog?module=dataset&dasid=", "http://dev.marineinfo.org/id/dataset/") for link in df['DataLandingPageURL']]


#define namespaces
dct = Namespace("http://purl.org/dc/terms/")

DatasetTitle = []
DatasetDescription = []
InProgressDataDate = []

for subject in marineinfo_subjects:
    g = Graph()
    print(subject)
    try:
        g.parse(subject+".ttl")
        
        title_results = g.query(
            """
            SELECT DISTINCT ?title
            WHERE {
                <%s> dct:title ?title .
                FILTER (lang(?title) = 'en')
            }
            """ % subject
        )
        
        if title_results:
            for i,row in enumerate(title_results):
                print("title: ", i, row.title)
                DatasetTitle.append(str(row.title))
        else: 
            DatasetTitle.append("no result")
        
        description_results = g.query(
            """
            SELECT DISTINCT ?description
            WHERE {
                <%s> dct:description ?description .
                FILTER (lang(?description) = 'en')
            }
            """ % subject
        )
        
        if description_results:
            for i,row in enumerate(description_results):
                print("description: ", i, row.description)
                DatasetDescription.append(str(row.description))
        else: 
            DatasetDescription.append("no result")

        progress_results = g.query(
            """
            SELECT DISTINCT ?progress
            WHERE {
                <%s> dct:temporal / mi:progress ?progress .
            }
            """ % subject
        )
        
        if progress_results:
            for i,row in enumerate(progress_results):
                print("progress: ", i, row.progress)
                InProgressDataDate.append(str(row.progress))
        else: 
            InProgressDataDate.append("no result")

    except Exception as e:
        DatasetTitle.append("error")
        DatasetDescription.append("error")
        InProgressDataDate.append("error")

print(DatasetTitle)
print(len(DatasetTitle))
df['DatasetTitle'] = DatasetTitle

print(len(DatasetDescription))
print(DatasetDescription)
df['DatasetDescription'] = DatasetDescription

print(len(InProgressDataDate))
print(InProgressDataDate)
df['InProgressDataDate'] = InProgressDataDate

print(len(marineinfo_subjects))

# Define the scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('./eternal-ruler-417805-abc596523486.json', scope)

# Authorize the client using the credentials
client = gspread.authorize(credentials)

# Create a new Google Sheet
new_sheet = client.open('MBO_test')

# Access the first sheet of the new Google Sheet
sheet = new_sheet.sheet1

# Convert float columns to strings
for column in df.select_dtypes(include=['float64']).columns:
    df[column] = df[column].astype(str)

# Write the DataFrame to Google Sheet
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("Data has been written to the new Google Sheet.")