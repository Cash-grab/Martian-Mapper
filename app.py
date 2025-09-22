import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
# Replace with your actual NASA API key.
NASA_API_KEY = os.environ.get('NASA_API_KEY', 'FWfMV1Y4DLpABZHUGbW9MhMMej3yA12XucJ4YR1a')

@app.route('/')
def home():
    """
    Renders the homepage with a welcome message and link to the query tool.
    """
    return render_template('homepage.html')

@app.route('/queryForm')
def queryForm():
    """
    Renders the main page with the user interface for the query tool.
    """
    return render_template('queryForm.html')

@app.route('/query', methods=['POST'])
def query_api():
    """
    Handles the API query based on user input from the form.
    """
    try:
        rover = request.form['rover']
        query_type = request.form['query_type']
        
        params = {'api_key': NASA_API_KEY}
        
        if query_type == 'sol':
            sol = request.form['sol']
            params['sol'] = sol
            api_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'
        else: # earth_date
            earth_date = request.form['earth_date']
            params['earth_date'] = earth_date
            api_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'

        response = requests.get(api_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        
        if 'photos' in data and len(data['photos']) > 0:
            # You can process the data here to display it nicely.
            # For a start, let's just return the first few photos.
            photos = data['photos'][:5] 
            return render_template('results.html', photos=photos)
        else:
            return "No photos found for the specified criteria.", 404

    except requests.exceptions.RequestException as e:
        return f"Error: A network or API error occurred: {e}", 500
    
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)