from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

def get_weather(city, state, zip_code):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "appid": API_KEY,
        "units":"imperial"
    }
    if zip_code:
        params["zip"] = zip_code + ",US"
    elif city:
        q = city
    elif state:
        q += ",US"
        params["q"] = q
    else:
        return None, "No Location Provided"
    
    try:
        response = requests.get(base_url, params=params)
        data=response.json()

        if response.status_code !=200:
            return None, data.get("message", "Error fetching weather")
        
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        city_name = data['name']
        

        return {
             "city": city_name,
             "temp": temp,
             "description" :description.capitalize(),
         } ,None
    except Exception as e:
        return None, str(e)
    

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        html = '''
         <h1 style="color: blue;">Weather App</h1>

        <form method="POST" action="/weather">
        City:   <input type="text" name="city" required><br>
        State:  <input type="text" name="state"><br>
        Zip:    <input type="text" name="zip_code"><br><br>
        Search: <button type="submit">Search</button>
        </form>
        '''
    
        return render_template_string(html)
    else: # POST
        return weather()

@app.route("/weather", methods=["POST"])
def weather():
    city      = request.form.get("city", "").strip()
    state     = request.form.get("state", "").strip()
    zip_code  = request.form.get("zip_code", "").strip()

    #Location String
    if zip_code:
       location = zip_code
    elif state:
         location=f"{city},{state}, US"
    else:
        location=f"{city}, US"

    result, error = get_weather(location, state, zip_code)

    if error:
        msg = f"<p style='color:red;'>Error: {error}</p>"
    elif result:
        msg =( f"""
        <h2>weather in {result['city']}</h2>
        <p>Temperature: {result['temp']} °F</p>
        <p>Description: {result['description']}</p>
        """)
    else:
        msg = "<h2>No Data</h2>"

    back_link = '<p><a href="/">← Back</a></p>'
    return render_template_string(msg + back_link)

if __name__ == "__main__":
    app.run(debug=True)