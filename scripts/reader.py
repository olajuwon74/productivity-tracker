import csv

csv_file = open('records/scaled_sim_log.csv', 'r')
csv_reader = csv.DictReader(csv_file)

#  local state variables
header = ["start_timestamp", "sequence", "cat", "norm_prod",
          "weight_ema_4", "class_weight", "seconds", "total_seconds"]

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


def get_next_record() -> dict:
    """
    Returns the next record in the csv file.
    """
    next_record = next(csv_reader, None)
    if not next_record:
        return {}

    formatted_record = {}
    for col in get_header():
        if col in ['class_weight', 'weight_ema_4', 'norm_prod']:
            formatted_record[col] = round(float(next_record.get(col, 0)), 1)
        else:
            formatted_record[col] = next_record.get(col)
    return formatted_record

def get_current_record() -> dict:
    """
    Returns the current record in the csv file.
    """
    current_record = read_history()[-1] if read_history() else {}
    return current_record

def get_header() -> list:
    """
    Returns the header of the csv file.
    """
    return header


def get_current_date_in_history():
    """
    Returns the date of the last record in the history.
    """
    # try to get the last record date, as set as the start date and the end date. if not found, return empty dict
    try:
        return read_history()[-1]['start_timestamp'].split(" ")[0]
    except IndexError:
        return None
