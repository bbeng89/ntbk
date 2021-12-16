# system imports
from datetime import date, timedelta


def filepath_for_date(dt, file):
    return f"log/{dt.strftime('%Y/%m-%B/%Y-%m-%d').lower()}/{file}.md"


def today(file):
    return filepath_for_date(date.today(), file)


def yesterday(file):
    yesterday = date.today() - timedelta(days=1)
    return filepath_for_date(yesterday, file)


def tomorrow(file):
    tomorrow = date.today() + timedelta(days=1)
    return filepath_for_date(tomorrow, file)


def specific_date(date, file):
    return filepath_for_date(date, file)
    

def get_logfile(date, file):
    if date == 'today':
        return today(file)
    elif date == 'yesterday':
        return yesterday(file)
    elif date == 'tomorrow':
        return tomorrow(file)

    return specific_date(date, file)


def get_files_for_day(day_path):
    files = []
    for child in day_path.glob('*.*'):
        files.append(child)
    return files


def list_files_for_day(day_path):
    for f in get_files_for_day(day_path):
        print(f.relative_to(day_path))