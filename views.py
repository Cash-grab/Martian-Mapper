from flask import render_template, request, Blueprint
import requests
from config import NASA_API_KEY

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('homepage.html')

@views.route('/tracker')
def Tracker():
    return render_template('ISSTracker.html')

@views.route('/queryForm')
def queryForm():
    return render_template('queryForm.html')

@views.route('/query', methods=['POST'])
def query_api():
    try:
        rover = request.form['rover']
        query_type = request.form['query_type']
        params = {'api_key': NASA_API_KEY}
        if query_type == 'sol':
            sol = request.form['sol']
            params['sol'] = sol
            api_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'
        else:
            earth_date = request.form['earth_date']
            params['earth_date'] = earth_date
            api_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        imageQuantity = int(request.form.get('quantity', 5))
        if 'photos' in data and len(data['photos']) > 0:
            photos = data['photos'][:imageQuantity]
            return render_template('results.html', photos=photos)
        else:
            return "No photos found for the specified criteria.", 404

    except requests.exceptions.RequestException as e:
        return f"Error: A network or API error occurred: {e}", 500

@views.route('/homepage')
def homepage():
    return render_template('homepage.html')

@views.route('/secretAppList')
def secretAppList():
    return render_template('secretAppList.html')

@views.route('/marsWeather')
def mars_weather():
    try:
        api_url = "https://api.nasa.gov/insight_weather/?api_key={}&feedtype=json&ver=1.0".format(NASA_API_KEY)
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        sols = data.get('sol_keys', [])
        if not sols:
            return render_template('marsWeather.html', weather=None, error="No weather data available.")
        latest_sol = sols[-1]
        weather = data[latest_sol]
        weather['sol'] = latest_sol
        return render_template('marsWeather.html', weather=weather, error=None)
    except Exception as e:
        return render_template('marsWeather.html', weather=None, error=str(e))

@views.route('/marsNews')
def mars_news():
    return render_template('marsNews.html')