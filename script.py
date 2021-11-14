import csv
from collections import Counter
from datetime import date, timedelta

csv_file = open('records/sim_df_updated.csv', 'r')
csv_reader = csv.reader(csv_file)

#  local state variables
header = next(csv_reader, None)
header = [col_name.title().replace("_", " ") for col_name in header]
history = []


def get_next_line() -> dict:
    """
    Reads the next line from the csv file, save it to history and returns it as a dict.
    """
    next_line = next(csv_reader, None)

    if next_line:
        next_line = dict(zip(header, next_line))
        history.append(next_line)
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

        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
        while start_date <= end_date:
            _history.append(history_logs[start_date.isoformat()])
            start_date += timedelta(days=1)
        return _history

    if start_date and end_date:
        return get_records_in_range(start_date, end_date)
    elif start_date:
        return get_records_in_range(start_date, date.today().isoformat())
    elif end_date:
        return get_records_in_range(date.today().isoformat(), end_date)
    return history


def get_daily_history() -> dict:
    """
    Returns the history of the csv file grouped by day.
    """
    daily_history = {}
    for line in history:
        day = line['Start Timestamp'].split(" ")[0]
        if day in daily_history:
            daily_history[day].append(line)
        else:
            daily_history[day] = [line]
    return daily_history


def get_summarized_daily_history() -> dict:
    """
    Returns the history of the csv file summarized by day.
    """
    daily_history = get_daily_history()
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
