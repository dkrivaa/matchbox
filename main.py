import json
import csv
from io import StringIO

from data import prepare_data
from engine import match_engine

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
        row = [item[0]] + item[1]
        writer.writerow(row)

    # Get the CSV string from the StringIO object
    csv_string = output.getvalue()
    output.close()
    return csv_string


# Getting urls from Google sheet

lead_url =
compliment_url =

# Making data lists
lead_list = prepare_data.get_file(lead_url)
compliment_list = prepare_data.get_file(compliment_url)

# Check integrity of data
checks = prepare_data.data_checks(lead_list, compliment_list)
if checks != 'All tests passed':
    # here goes code if data NOT OK

couples = match_engine.match(lead_list, compliment_list)

json_result = results_to_json(couples)
csv_result = results_to_csv(couples)

