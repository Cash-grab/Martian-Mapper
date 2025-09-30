from flask import jsonify
from flask import render_template, request, Blueprint
import requests
import random
from config import NASA_API_KEY

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('homepage.html')


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

@views.route('/tracker')
def Tracker():
    return render_template('ISSTracker.html')

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

@views.route('/marsMap')
def mars_map():
    return render_template('marsMap.html')

@views.route('/api/random_mars_image')
def random_mars_image():
    rovers = ["Curiosity", "Opportunity", "Spirit", "Perseverance"]


    rover = random.choice(rovers)
    print("Choosen rover", rover)
    choosenSite = {
        "Curiosity": {"lat": -4.5895, "lng": 137.4417},
        "Opportunity": {"lat": -1.9462, "lng": 354.4734},
        "Spirit": {"lat": -14.5684, "lng": 175.472636},
        "Perseverance": {"lat": 18.4447, "lng": 77.4508}
    }[rover]

    # Pick a random sol (Martian day)
    sol = random.randint(1, 3000)
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&api_key={NASA_API_KEY}"
    print("made query" , url)
    resp = requests.get(url)
    print('Requested URL')
    data = resp.json()
    if not data.get('photos'):
        print("No photos found retrying!")
        return random_mars_image()  # Try again if no photos
    
    photo = random.choice(data['photos'])
    print("IMAGE CHOOSEN: ", photo['img_src'])
    while "BR.JPG" in photo['img_src']:
        print(photo['img_src'], '\n Caught inavlid image, now retying')
        return random_mars_image()
    

    

    
    
    
    # Simulate coordinates near Rover's landing site
    coords = {
        "lat": choosenSite["lat"] + (random.random() - 0.5) * 2,  # +/- 1 degree
        "lng": choosenSite["lng"] + (random.random() - 0.5) * 2
    }
    return jsonify({
        "img": photo["img_src"],
        "coords": coords
    })