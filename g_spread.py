import sys
import gspread
from oauth2client.client import GoogleCredentials
import os

# Google Docs spreadsheet name and worksheet name
# The json file contains my credentials
WORKBOOK = 'Weather Station'
WORKSHEET = 'Raw Data'
JSON_FILE = "/home/weather/weather/config/gdoc.creds.json"

'''
    Go here for instuctions on how to generate the .json credentials file:
    https://developers.google.com/identity/protocols/OAuth2
    Very simple class. You only need to call log_readings - it handles login 
    if needed. It will log any tuple to the workbook / worksheet listed
    above
'''
class Sheet(object):

    def __init__(self):
        self._worksheet = None
        self.retry = False
        # Use the below because the standard method either doesn't work
        # or there is major user error on my part. Regardless, this works
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = JSON_FILE
        return 

    """
        Using oauth2 see https://gspread.readthedocs.org/en/latest/oauth2.html
        User does not need to call this. It is called by log_readings if needed
    """
    def login_open_sheet(self):
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        gs = None
        try:
            scope = ["https://spreadsheets.google.com/feeds"]
            credentials = GoogleCredentials.get_application_default()
            credentials = credentials.create_scoped(scope)
            gs = gspread.authorize(credentials)
            self._worksheet = gs.open(WORKBOOK)
            self._worksheet = self._worksheet.worksheet(WORKSHEET)
        except Exception as e:
            print('Unable to login and get spreadsheet')
            print(e)
            sys.exit(1)
        return 

    """
        Takes a tuple of the following:
        <time secs> <human time> <temp (f)> <light level> <humid> <power>
    """
    def log_readings(self, readings):
        # Login if necessary.
        if self._worksheet is None:
            self.login_open_sheet()

        # Append the data in the spreadsheet, including a timestamp
        try:
            #_worksheet.append_row((datetime.datetime.now(), temp, humidity))
            self._worksheet.append_row(readings)
        except:
            # Error appending data, most likely because credentials are stale.
            # Null _worksheet so a login is performed at the top of the loop.
            print('Append error, logging in again')
            self._worksheet = None
            if self.retry == False:
                self.retry = True
                self.log_readings(readings)
                self.retry = False
        return 
