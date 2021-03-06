from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from scripts import logics
import json

TEMPLATE_DIR = 'templates'
STATIC_DIR = 'static'
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/logs')
def view():
    """
    Loads the view page
    """
    # parse request arguments
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    header = logics.get_header()
    next_line = {}

    if start_date or end_date:
        lines_history = logics.get_history(start_date, end_date)
    elif not (start_date and end_date):
        next_line = logics.get_next_line()
        # exclude the last line from the list, since it is the next_line variable
        lines_history = logics.get_history()[:-1]

    return render_template('view.html',
                           header=header,
                           next_line=next_line,
                           history=lines_history)


@app.route('/history')
def history():
    """
    Loads the history page
    """
    # parse request arguments
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    daily_history = logics.get_summarized_daily_history(
        start_date=start_date, end_date=end_date, number_of_records=2)
    return render_template('history.html', daily_history=daily_history)


@app.route('/productivity')
def productivity():
    """
    Loads the productivity page
    """

    # for productivity doughnut chart
    daily_history = logics.get_summarized_daily_history(
        for_productivity_charts=True, number_of_records=5)
    top_sequences_with_counts = [(entry['sequence'], entry['counts'])
                                 for history in daily_history.values() for entry in history['sequences']]
    total_counts = sum([count for _, count in top_sequences_with_counts])
    top_sequences_with_percentage = [{'id': sequence, 'value': (
        counts/total_counts)*100} for sequence, counts in top_sequences_with_counts] or [{'id': 'No data', 'value': 100}]
    
    last_two_days = logics.get_last_two_days_history()
    yesterday_class_weight = last_two_days["yesterday"].get("norm_prod") or 0
    today_class_weight = last_two_days["today"].get("norm_prod") or 0
    daily_change = today_class_weight - yesterday_class_weight
    if daily_change > 0:
        daily_change_class = 'G'
    elif daily_change < 0:
        daily_change_class = 'P'
    else:
        daily_change_class = 'N'
    
    yesterday_class_weight = yesterday_class_weight or '-'
    today_class_weight = today_class_weight or '-'


    message = {
        "P": "Productivity went down!!!",
        "G": "Productivity went up!!!",
        "N": "Maintaining Productivity"
    }
    return render_template('productivity.html',
                top_sequences_with_percentage=json.dumps(top_sequences_with_percentage),
                yesterday_class_weight=yesterday_class_weight,
                today_class_weight=today_class_weight,
                daily_change_class=daily_change_class,
                daily_change_message=message[daily_change_class],
                )


@app.route('/current_record')
def get_latest_productivity():
    """
    Gets the latest productivity status/cat
    """
    latest_productivity = logics.get_current_line()
    return jsonify(latest_productivity)


@app.route('/day_productivity')
def get_day_productivity_chart_data():
    """
    Gets the productivity chart data for the current day
    """
    day_productivity = logics.get_history(for_productivity_charts=True)
    return jsonify(day_productivity)


@app.route("/")
def home():
    """
    Loads the home page
    """
    return redirect(url_for('productivity'))
