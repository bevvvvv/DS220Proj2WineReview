from flask import Flask, render_template, request
import pandas as pd
import queryFunctions as query

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'
wineTypes = sorted(pd.read_csv('wines.csv')['x'].dropna().tolist())
countries = sorted(pd.read_csv('countries.csv')['x'].dropna().tolist())
wineries = sorted(pd.read_csv('wineries.csv')['x'].dropna().tolist())
regions = sorted(pd.read_csv('regions.csv')['x'].dropna().tolist())

@app.route('/', methods=['POST', 'GET'])
def poll():
    if request.method == 'POST':
        queryMethod = request.form["queries"]

        selectType = request.form.get("wineType")
        selectCountry = request.form.get("country")
        selectRegion = request.form.get("region")
        selectWinery = request.form.get("winery")
        priceRange = request.form.get("priceRange")
        scoreRange = request.form.get("scoreRange")
        lower = request.form.get("low")
        upper = request.form.get("high")

        params = request.form.getlist("params")
        
        wines = None
        if queryMethod == "filter":
                wines = query.pickwine(selectType, selectCountry, selectRegion, selectWinery, priceRange, scoreRange, params)
        elif queryMethod == "dist":
                wines = query.wineryDistance(selectType, lower, upper)
        else:
                wines = query.reviewerDistance(selectType, lower, upper)

        return render_template('results.html', q1=selectType, q2=selectCountry, q3=selectRegion, q4=selectWinery,
                               q5=priceRange, q6=scoreRange, wines=wines, params=params)

    return render_template('index.html', wineTypes=wineTypes, countries=countries, wineries=wineries, regions=regions)