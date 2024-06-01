import json
import csv
from io import StringIO
import base64
import gspread
from google.oauth2.service_account import Credentials
import os

from data import prepare_data
from engine import match_engine


# open google sheet 'googleIntegrator'
def openGoogle():
    credentials_json_string = os.environ.get('credentials_json_string')
    credentials_json = json.loads(base64.b64decode(credentials_json_string))
    sheet_id = os.environ.get('sheet_id')

    # Collect all environment variables that start with 'param'
    params = {key: os.environ[key] for key in os.environ if key.startswith('param')}

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_info(credentials_json, scopes=scopes)
    client = gspread.authorize(creds)

    book = client.open_by_key(sheet_id)

    return book, params


def results_to_json(list_of_lists):
    # Transform the list of lists into a list of dictionaries
    transformed_data = [{"lead": item[0], "compliment": item[1]} for item in list_of_lists]

    # Convert the transformed data to a JSON string
    json_string = json.dumps(transformed_data, indent=4)
    return json_string


def results_to_csv(list_of_lists):
    output = StringIO()
    writer = csv.writer(output)

    # Write the data
    for item in list_of_lists:
        writer.writerow(item)

    # Get the CSV string from the StringIO object
    csv_string = output.getvalue()
    output.close()
    return csv_string


# Getting urls from Google sheet
book, params = openGoogle()
lead_url = params['param0']
compliment_url = params['param1']

# Making data lists
lead_list = prepare_data.get_file(lead_url)
compliment_list = prepare_data.get_file(compliment_url)

# Check integrity of data
checks = prepare_data.data_checks(lead_list, compliment_list)
if checks != 'All tests passed':
    # here goes code if data NOT OK
    # making json string of error message
    json_string = json.dumps([{'error': checks}], indent=4)
    book.worksheet('match').update_cell(2, 4, json_string)

else:
    couples, lead_summary, compliment_summary = match_engine.match(lead_list, compliment_list)
    print(couples)
    json_result = results_to_json(couples)
    csv_result = results_to_csv(couples)

    book.worksheet('match').update_cell(2,3, csv_result)
    book.worksheet('match').update_cell(2,4,json_result)
    book.worksheet('match').update_cell(4, 4, lead_summary[0])
    book.worksheet('match').update_cell(4, 5, lead_summary[1])
    book.worksheet('match').update_cell(5, 4, compliment_summary[0])
    book.worksheet('match').update_cell(5, 5, compliment_summary[1])


