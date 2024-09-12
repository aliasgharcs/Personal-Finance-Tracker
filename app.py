from turtledemo.penrose import start

from flask import Flask, render_template, request, redirect, url_for
from main import add, update, delete, CSV
from data_entry import get_date, get_amount, get_category, get_description
from plot import plot_transaction
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Home page with options
@app.route('/')
def index():
    return render_template('index.html')

# Add new transaction (Data Entry)
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form.get('date')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description', '')
        CSV.add_entry(date, amount, category, description)
        return redirect(url_for('index'))
    return render_template('add.html')

# Update a transaction
@app.route('/update', methods=['GET', 'POST'])
def update_transaction():
    if request.method == 'POST':
        serial_number = int(request.form.get('serial_number'))
        date = request.form.get('date')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description', '')
        CSV.update_entry(serial_number, date, amount, category, description)
        return redirect(url_for('index'))
    return render_template('update.html')

# Delete a transaction
@app.route('/delete', methods=['GET', 'POST'])
def delete_transaction():
    if request.method == 'POST':
        serial_number = int(request.form.get('serial_number'))
        CSV.delete_entry(serial_number)
        return redirect(url_for('index'))
    return render_template('delete.html')

# View transactions within a date range
@app.route('/view_transaction', methods=['GET', 'POST'])
def view_transactions():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        df = CSV.get_transaction(start_date, end_date)
        return render_template('view.html', table=df.to_html())
    return render_template('view.html')

# Plot transaction data (daily/monthly/yearly)
@app.route('/plot', methods=['GET', 'POST'])
def plot_transactions():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        timeframe = request.form.get('timeframe')  # Get the selected timeframe

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date = start_date.strftime('%d-%m-%Y')

        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = end_date.strftime('%d-%m-%Y')


        df = CSV.get_transaction(start_date, end_date)

        if not df.empty:
            plot_filename = plot_transaction(df, timeframe)
            return render_template('plot.html', plot=url_for('static', filename=plot_filename))

    return render_template('plot.html')



if __name__ == "__main__":
    app.run(debug=True)
