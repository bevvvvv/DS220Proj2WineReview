from flask import Flask, render_template, request
import pandas as pd
import queryFunctions

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'
wineTypes = sorted(pd.read_csv('wines.csv')['x'].dropna().tolist())
countries = sorted(pd.read_csv('countries.csv')['x'].dropna().tolist())
wineries = sorted(pd.read_csv('wineries.csv')['x'].dropna().tolist())
regions = sorted(pd.read_csv('regions.csv')['x'].dropna().tolist())

@app.route('/', methods=['POST', 'GET'])
def poll():
    if request.method == 'POST':
        return render_template('results.html', q1=request.data)

    return render_template('index.html', wineTypes=wineTypes, countries=countries, wineries=wineries, regions=regions)