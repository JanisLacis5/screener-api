import pytz
from datetime import datetime


def get_eastern_time():
    est_timezone = pytz.timezone("America/New_York")
    est_time = datetime.now(est_timezone)
    est_time = est_time.strftime("%H%M")
    return est_time
