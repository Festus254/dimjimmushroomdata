from flask import Flask, render_template, request, flash, redirect, url_for
from app.forms import TemperatureForm
import csv
from datetime import datetime
import plotly
import plotly.graph_objs as go
import gunicorn

import pandas as pd
import numpy as np
import json

from os.path import join, dirname, realpath
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/data.csv')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e16f9f31b5b3508a7603d9aab0448c2a'

@app.route("/hello", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def hello():
    form = TemperatureForm()
    if form.validate_on_submit():
        time = datetime.now().strftime("%Y-%m-%d, %H:%M")
        temp = form.temp.data
        section = form.section.data
        with open(UPLOADS_PATH, 'a', newline='') as csv_file:
            data = csv.writer(csv_file, delimiter = ',',
                                  quotechar = '"',
                                  quoting = csv.QUOTE_MINIMAL)    
            data.writerow([time, temp, section])
                #closing the file
                #data.close()
            flash('Your temperature has been recorded', 'success')
            return redirect(url_for('results'))
        
    return render_template("home.html", form = form)

@app.route("/results", methods=["GET"])
def results():
    def create_plot():
        df = pd.read_csv(UPLOADS_PATH, delimiter=",")
        df.columns = df.columns.str.strip()
        
        df = pd.pivot_table(df, values='Temperature', index=['Time'], columns='Section', aggfunc=np.sum)
        
        fig = go.Figure()
        for col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col].values,
                                name = col,
                                mode = 'markers+lines',
                                line=dict(shape='linear'),
                                connectgaps=True
                                )
                    )
 
        graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    line = create_plot()
    if request.method == 'GET':
        with open(UPLOADS_PATH) as csv_file:
            data = csv.reader(csv_file, delimiter = ',')
            first_line = True
            records = []
            for row in data:
                if not first_line:
                     records.append({
                "Time": row[0],
                "Temperature": row[1],
                "Section": row[2]
                    })
                else:
                    first_line = False
    return render_template("results.html", title='Results', records = records, plot = line, len = len(records))
   
