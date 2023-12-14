import functions

from flask import Flask, render_template, request

# Create an instance of Flask
app = Flask(__name__)


# Create a view function for /
@app.route("/")
def index():
    return render_template("index.html")

# Create a view function for /results
@app.route("/submit-page", methods=["GET", "POST"])
def submit_page():
    if request.method == "POST":
        checked = "coord" in request.form
        place = request.form["water"]
        if checked == True:
            tuplify = tuple(place.split(","))
            if functions.rightformat(tuplify) == True:
                isit = functions.isitwater(tuplify)
                water = functions.get_state(isit)
            else:
                return render_template("badtuple.html", place = place)
        else:
            if functions.wrongformat(place) == True:
                geocoded = functions.geocode(request.form["water"])
                if geocoded != None:
                    isit = functions.isitwater(geocoded)
                    water = functions.get_state(isit)
                    
                else:
                    return render_template("cantbefound.html", place = place)
            else:
                return render_template("cantbefound.html", place = place)

        if water == True:
            state = "water"
        else:
            state = "earth"
        
        sounds = functions.searchsound(state)
        return render_template("results.html", water = water, sounds = sounds[0], place = place, images = sounds[1])
    else:
        return ("HTTP 400 Error: Wrong HTTP method")
    
