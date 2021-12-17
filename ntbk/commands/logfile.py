# system imports
from datetime import date, timedelta


def filepath_for_date(dt, file):
    return f"log/{dt.strftime('%Y/%m-%B/%Y-%m-%d').lower()}/{file}.md"


def get_date(date_arg):
    if date_arg == 'today':
        return date.today()
    elif date_arg == 'yesterday':
        return date.today() - timedelta(days=1)
    elif date_arg == 'tomorrow':
        return date.today() + timedelta(days=1)

    return date_arg #should be a date instance
    

def get_files_for_day(day_path):
    files = []
    for child in day_path.glob('*.*'):
        files.append(child)
    return files


def list_files_for_day(day_path):
    for f in get_files_for_day(day_path):
        print(f.relative_to(day_path))