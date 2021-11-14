from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import script

TEMPLATE_DIR = 'templates'
STATIC_DIR = 'static'
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/view')
def view():
    """
    Loads the view page
    """
    # parse request arguments
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    header = script.get_header()
    next_line = {}

    if start_date or end_date:
        lines_history = script.get_history(start_date, end_date)
    elif not (start_date and end_date):
        next_line = script.get_next_line()
        # exclude the last line from the list, since it is the next_line variable
        lines_history = script.get_history()[:-1]


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


    daily_history = script.get_summarized_daily_history(start_date, end_date)
    return render_template('history.html', daily_history=daily_history)


@app.route('/productivity')
def productivity():
    """
    Loads the productivity page
    """
    return render_template('productivity.html')


@app.route("/")
def home():
    """
    Loads the home page
    """
    return redirect(url_for('view'))
