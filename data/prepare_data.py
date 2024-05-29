import requests
import chardet
from io import StringIO
import pandas as pd


def get_file(url):

    response = requests.get(url)
    if response.status_code == 200:
        # Identifying encoding
        encoding = chardet.detect(response.content)
        # decode the response content accordingly
        data_string = response.content.decode(encoding['encoding'])
        # reading csv string to dataframe
        df = read_csv(data_string)
        data_list = [[str(row[0]), list(map(str, row[1:]))] for row in df.itertuples(index=False, name=None)]
        return data_list


# CSV FILES
def read_csv(csv_string):
    df = pd.read_csv(StringIO(csv_string))
    return df


# Function to check the integrity of the uploaded data
def data_checks(lead_list, compliment_list):
    # number of leads and compliments
    if len(lead_list) > len(compliment_list):
        return 'ERROR - Too few leads compared to compliments'

    # identical entries in prefs
    # leads
    if [len(x[1]) == len(set(x[1])) for x in lead_list][0] :
        pass
    else:
        return 'ERROR - Identical entries in lead prefs'
    # compliments
    if [len(x[1]) == len(set(x[1])) for x in compliment_list][0] :
        pass
    else:
        return 'ERROR - Identical entries in compliment prefs'

    # Making sure that prefs are defined correctly (names exist)
    leads = [x[0] for x in lead_list]
    compliments = [y[0] for y in compliment_list]
    # lead names
    print([[[x for x in sublist[1]] for sublist in compliment_list] in leads][0])
    if [[[x for x in sublist[1]] for sublist in compliment_list] in leads][0]:
        pass
    else:
        return 'ERROR - Prefs in compliments are not consistent with lead names'
    # compliment names
    if [[[x for x in sublist[1]] for sublist in lead_list] in compliments][0]:
        pass
    else:
        return 'ERROR - Prefs in leads are not consistent with compliment names'

    return 'All tests passed'



url = 'https://download-files.wixmp.com/ugd/76f9f0_d76aafee15e849e78246fb86366c9296.csv?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46YXBwOmU2NjYzMGU3MTRmMDQ5MGFhZWExZjE0OWIzYjY5ZTMyIiwic3ViIjoidXJuOmFwcDplNjY2MzBlNzE0ZjA0OTBhYWVhMWYxNDliM2I2OWUzMiIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sImlhdCI6MTcxNjczMTE5NiwiZXhwIjoxNzE2NzY3MjA2LCJqdGkiOiJmZWUxZDkyYS1lMjcxLTQwYTMtODQ1YS1lNjM1NjZkM2Q2OTYiLCJvYmoiOltbeyJwYXRoIjoiL3VnZC83NmY5ZjBfZDc2YWFmZWUxNWU4NDllNzgyNDZmYjg2MzY2YzkyOTYuY3N2In1dXSwiZGlzIjp7ImZpbGVuYW1lIjoiZW5jb2RlZC10ZXN0MyAoMSkuY3N2IiwidHlwZSI6ImF0dGFjaG1lbnQifX0.ewIhDZu1kjTB8P3x1YO_hB99IDaY6aUSVcX_fPuOtDA'
get_file(url)

