from datetime import date, timedelta


def filepath_for_date(dt):
    return dt.strftime('log/%Y/%m-%B/%Y-%m-%d.md').lower()

def todays_file():
    return filepath_for_date(date.today())

def yesterdays_file():
    yesterday = date.today() - timedelta(days=1)
    return filepath_for_date(yesterday)

def tomorrows_file():
    tomorrow = date.today() + timedelta(days=1)
    return filepath_for_date(tomorrow)

def specific_date_file(dateString):
    return filepath_for_date(date.fromisoformat(dateString))

def is_logfile_command(command):
    if command in ['today', 'yesterday', 'tomorrow']:
        return True
    
    try:
        specific_date_file(command)
        return True
    except:
        return False
    
def get_logfile(name):
    if name == 'today':
        return todays_file()
    elif name == 'yesterday':
        return yesterdays_file()
    elif name == 'tomorrow':
        return tomorrows_file()

    return specific_date_file(name)