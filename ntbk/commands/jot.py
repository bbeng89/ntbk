# system imports
from datetime import datetime

# 3rd party imports
from colorama import Fore, Style

# app imports
import config

def jot_note(note, file_path, add_timestamp):
    with file_path.open(mode='a') as f:
        f.write('\n')
        if add_timestamp:
            f.write(f"[{datetime.now().strftime('%I:%M %p')}]\n")
        f.write(note + '\n')

    print(f"{Fore.GREEN}Jotted note to today's {file_path.name} file{Style.RESET_ALL}")