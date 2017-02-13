import sys
import gspread
from oauth2client.client import GoogleCredentials
import os
import time
import logging

# Google Docs spreadsheet name and worksheet name
# The json file contains my credentials
WORKBOOK = 'Weather Station 2'
WORKSHEET = 'Raw Data'
JSON_FILE = "/home/weather/weather/config/gdoc.creds.json"
NUM_RETRIES = 5
#Number of seconds to pause before trying to log in again if failed
RETRY_TIME = 30

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
        self.login_attempts = 0
        logging.basicConfig(format="%(asctime)s: %(message)s",
                level=logging.DEBUG)
        # Use the below because the standard method either doesn't work
        # or there is major user error on my part. Regardless, this works
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = JSON_FILE
        logging.info("Google sheets access configured")
        return 

    """
        Using oauth2 see https://gspread.readthedocs.org/en/latest/oauth2.html
        User does not need to call this. It is called by log_readings if needed
    """
    def login_open_sheet(self):
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        logging.info("Trying to log in to google")
        gs = None
        try:
            scope = ["https://spreadsheets.google.com/feeds"]
            credentials = GoogleCredentials.get_application_default()
            credentials = credentials.create_scoped(scope)
            gs = gspread.authorize(credentials)
            self._worksheet = gs.open(WORKBOOK)
            self._worksheet = self._worksheet.worksheet(WORKSHEET)
            self.login_attempts = 0
        except Exception as e:
            self.login_attempts += 1
            if self.login_attempts > NUM_RETRIES:
                logging.info('Unable to login and get spreadsheet')
                logging.info(e)
                sys.exit(1)
            time.sleep(RETRY_TIME)
            self.login_open_sheet()
        return 

    """
        Takes a tuple of the following:
        <time secs> <human time> <temp (f)> <light level> <humid> <power>
    """
    def log_readings(self, readings):
        # Login if necessary.
        if self._worksheet is None:
            self.login_open_sheet()

        logging.debug("Logging to google sheet")
        # Append the data in the spreadsheet, including a timestamp
        try:
            #_worksheet.append_row((datetime.datetime.now(), temp, humidity))
            self._worksheet.append_row(readings)
            logging.debug("Successfully logged to google sheet")
        except Exception as e:
            # Error appending data, most likely because credentials are stale.
            # Null _worksheet so a login is performed at the top of the loop.
            logging.info('{0}: Append error, logging in again'.format(time.asctime()))
            logging.info('Exception: {}'.format(str(e)))
            self._worksheet = None
            if self.retry == False:
                self.retry = True
                self.log_readings(readings)
                self.retry = False
        return 
