import sys
import gspread
from oauth2client.client import GoogleCredentials
import os
import io
import time
from oauth2client.client import SignedJwtAssertionCredentials

# Google Docs spreadsheet name and worksheet name
# The json file contains my credentials
WORKBOOK = 'Weather Station'
WORKSHEET = 'Raw Data'
JSON_FILE = "/home/weather/weather/test/gdoc.creds.json"
P12_FILE = "/home/weather/weather/test/Weather-Station-1d3e09b8f754.p12"
EMAIL = "166745707437-3tei9oihik35phk29j66kuuu5rkdhkvo@developer.gserviceaccount.com"
SCOPE = ["https://spreadsheets.google.com/feeds"]
#SCOPE = ["https://www.googleapis.com/auth/drive.file"]

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
            print("opening")
            with io.open(P12_FILE, mode='br') as f:
                private_key = f.read()
            print("opened")
            credentials = SignedJwtAssertionCredentials(EMAIL, private_key,
                    SCOPE)
            print("got credentials")
            gs = gspread.authorize(credentials)
            print("authorized")
            #self._worksheet = gs.open(WORKBOOK)
            self._worksheet = gs.open_by_key("1CcYvZ280VI8xxLKEaUugUju1IuGgzbT1JugutM_hNxc")
            print("opened")
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
            print('{0}: Append error, logging in again'.format(time.asctime()))
            self._worksheet = None
            if self.retry == False:
                self.retry = True
                self.log_readings(readings)
                self.retry = False
        return 

if __name__ == '__main__':
    # We are testing here
    s = Sheet()
    s.log_readings((1,2,3,4,5,6,7))
