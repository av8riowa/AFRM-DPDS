from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)
data_file = 'vehicles.csv'

def load_data():
    return pd.read_csv(data_file)

def save_data(df):
    df.to_csv(data_file, index=False)

@app.route('/')
def index():
    df = load_data()
    vehicles = df.to_dict('records')
    return render_template('index.html', vehicles=vehicles)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    serial_number = data['serial_number']
    auth_number = data['auth_number']
    latitude = data['latitude']
    longitude = data['longitude']
    speed = data['speed']
    timestamp = datetime.now().isoformat()

    df = load_data()
    mask = (df['serial_number'] == serial_number) & (df['auth_number'] == auth_number)
    if mask.any():
        df.loc[mask, ['latitude', 'longitude', 'speed', 'timestamp']] = [latitude, longitude, speed, timestamp]
        save_data(df)
    return 'OK'

@app.route('/edit/<serial_number>/<auth_number>', methods=['GET', 'POST'])
def edit(serial_number, auth_number):
    df = load_data()
    vehicle = df[(df['serial_number'] == serial_number) & (df['auth_number'] == auth_number)].to_dict('records')[0]

    if request.method == 'POST':
        vehicle['callsign'] = request.form['callsign']
        vehicle['serial_number'] = request.form['serial_number']
        vehicle['auth_number'] = request.form['auth_number']
        df.update(pd.DataFrame([vehicle]))
        save_data(df)
        return redirect(url_for('index'))

    return render_template('edit.html', vehicle=vehicle)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
