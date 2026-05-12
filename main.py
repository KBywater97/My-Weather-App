from flask import Flask, request, render_template_string
import get_weather_api as api

app = Flask(__name__)

# HTML form template
FORM_HTML = """
<h2>Weather App</h2>
<form method="POST">
    City: <input type="text" name="city"><br>
    State: <input type="text" name="state"><br>
    Zip: <input type="text" name="zip"><br>
    <button type="submit">Search</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get form inputs
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip")

        # Call the API function from api.py
        weather_data, error = api.get_weather(city, state, zip_code)

        if error:
            result = f"<p style='color:red;'>Error: {error}</p>"
        else:
            result = f"""
                <h3>Weather in {weather_data['city']}</h3>
                <p>Temperature: {weather_data['temp']}°F</p>
                <p>Condition: {weather_data['description']}</p>
            """

        return render_template_string(FORM_HTML + result)


    return render_template_string(FORM_HTML)

if __name__ == "__main__":
    app.run(debug=True)
