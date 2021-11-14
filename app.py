from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import script

TEMPLATE_DIR = 'assets'
STATIC_DIR = 'assets'
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/view')
def view(start_date=None, end_date=None):
    """
    Loads the view page
    """
    header = script.get_header()
    next_line = {}

    if not (start_date and end_date):
        next_line = script.get_next_line()
        # exclude the last line from the list, since it is the next_line variable
        lines_history = script.get_history()[:-1]
    else:
        lines_history = script.get_history(start_date, end_date)

    return render_template('html/view.html',
                           header=header,
                           next_line=next_line,
                           history=lines_history)


@app.route('/history')
def history():
    """
    Loads the history page
    """
    daily_history = script.get_summarized_daily_history()
    print(daily_history)
    return render_template('html/history.html', daily_history=daily_history)


@app.route('/productivity')
def productivity():
    """
    Loads the productivity page
    """
    return render_template('html/productivity.html')


@app.route("/")
def home():
    """
    Loads the home page
    """
    return redirect(url_for('view'))
