from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

TEMPLATE_DIR = 'assets'
STATIC_DIR = 'assets'
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/view')
def view():
    """
    Loads the view page
    """
    return render_template('html/view.html')

@app.route('/history')
def history():
    """
    Loads the history page
    """
    return render_template('html/history.html')

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