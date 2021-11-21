from scripts import reader


def inject_productivity_chart_start_and_end_dates(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('for_productivity_charts'):
            kwargs['start_date'] = kwargs['end_date'] = reader.get_current_date_in_history()
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper
