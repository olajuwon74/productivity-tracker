import csv
from collections import Counter
from datetime import date, timedelta

csv_file = open('records/sim_df_updated.csv', 'r')
csv_reader = csv.reader(csv_file)

#  local state variables
header = next(csv_reader, None)
header = [col_name.title().replace("_", " ") for col_name in header]
history = []

def append_to_history(line):
    """
    Appends a line to the history.
    currently using local state variable, can be changed to a cache
    """
    history.append(line)

def read_history():
    """
    Reads the history of the csv file and returns it as a list of dicts.
    currently using local state variable, can be changed to a cache
    """
    return history

def get_next_line() -> dict:
    """
    Reads the next line from the csv file, save it to history and returns it as a dict.
    """
    next_line = next(csv_reader, None)

    if next_line:
        next_line = dict(zip(header, next_line))
        append_to_history(next_line)
        return next_line
    return {}


def get_header() -> list:
    """
    Returns the header of the csv file.
    """
    return header


def get_history(start_date=None, end_date=None) -> list:
    """
    Returns the history of the csv file.
    """
    def get_records_in_range(start_date, end_date):
        # get the history between the start and end date
        history_logs = get_daily_history()
        _history = []
        if history_logs:
            days_in_log = list(history_logs.keys())

            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            max_date = date.fromisoformat(days_in_log[-1])
            longest_possible_end = min([max_date, end_date])

            while start_date <= longest_possible_end:
                for record in history_logs[start_date.isoformat()]:
                    _history.append(record) # append the record to the history
                start_date += timedelta(days=1)
        return _history

    if start_date and end_date:
        return get_records_in_range(start_date, end_date)
    elif start_date:
        return get_records_in_range(start_date, date.today().isoformat())
    elif end_date:
        return get_records_in_range(date.today().isoformat(), end_date)
    return read_history()


def get_daily_history(start_date=None, end_date=None) -> dict:
    """
    Returns the history of the csv file grouped by day.
    """
    daily_history = {}
    for line in history:
        day = line['Start Timestamp'].split(" ")[0]
        if start_date and day < start_date:
            continue
        elif end_date and day > end_date:
            break
        
        if day in daily_history:
            daily_history[day].append(line)
        else:
            daily_history[day] = [line]
        
    return daily_history


def get_summarized_daily_history(start_date=None, end_date=None) -> dict:
    """
    Returns the history of the csv file summarized by day.
    """
    daily_history = get_daily_history(start_date, end_date)
    summarized_history = {}

    for day, records in daily_history.items():
        sequences = [record.get("Sequence") for record in records]
        most_common_sequences = [count_pair[0]
                                 for count_pair in Counter(sequences).most_common(2)]

        # since scoring is realtime, we need to take the last record of the day
        status = records[-1].get("Cat")

        summarized_history[day] = {
            "status": status,
            "sequence": "\n".join(most_common_sequences)
        }
    return summarized_history
