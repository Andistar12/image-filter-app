"""
Written by Andy Nguyen
A simple app to process an image based on filters
"""

import flask
from flask import request
from PIL import Image, ImageOps
import logging
import hashlib
from werkzeug.utils import secure_filename
import os
import traceback

# ----------------------------------
# Globals

app = flask.Flask(__name__)
app.secret_key = "nah"
app.logger.setLevel(logging.DEBUG)
app.port = 5000

ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg"]
ALLOWED_FILTERS = ["invert", "rgb", "beige"]

# ----------------------------------
# Frontend

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


# ----------------------------------
# Backend

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in \
            ["png", "jpeg", "jpg"]

@app.route("/process", methods=["POST"])
def process():
    app.logger.debug("Received request to process image")
    app.logger.debug(dict(request.form))

    if "filter" not in request.form:
        return flask.jsonify({
            "error": "No filter specified"
        })

    filt = request.form.get("filter").lower()

    if filt not in ALLOWED_FILTERS:
        return flask.jsonify({
            "error": "Bad filter"
        })

    if "image" not in request.files:
        return flask.jsonify({
            "error": "No file sent"
        })

    f = request.files["image"]
    
    if f.filename == "":
        return flask.jsonify({
            "error": "No file sent"
        })

    if "." not in f.filename or f.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return flask.jsonify({
            "error": "Invalid file"
        })

    # Save file
    filename = "static/image" + secure_filename(f.filename)
    f.save(filename)

    # Run filter
    if filt == "invert":
        try:
            pass
            #ImageOps.invert(Image.open(filename)).save(filename)
        except Exception as e:
            app.logger.debug(e)
            return flask.jsonify({
                "error": "Error occurred applying filter"
            })
    elif filt == "rgb":
        try:
            red = [0, 255, 0, 0]
            green = [0, 0, 255, 0]
            blue = [0, 0, 0, 255]
            color_list = [red, green, blue]
            im = Image.open(filename)
            pixels = im.load()
            width, height = im.size

            for i in range(width):
                for j in range(height):
                    index = 0
                    for x in range(len(color_list)):
                        smallest = 255

                        R_VAL = (pixels[i,j])[0] - (color_list[x][1])
                        G_VAL = (pixels[i,j])[1] - (color_list[x][2])
                        B_VAL = (pixels[i,j])[2] - (color_list[x][3])
                        final_val = abs(R_VAL) + abs(G_VAL) + abs(B_VAL)

                        dfz = final_val

                        if dfz < smallest:
                            smallest = dfz
                            index = x

                    pixels[i,j] = (color_list[index][1], color_list[index][2], color_list[index][3])
            im.save(filename)

        except Exception as e:
            app.logger.debug(traceback.format_exc())
            return flask.jsonify({
                "error": "Error occurred applying filter"
            })
    elif filt == "beige":
        try:
            emb_dark_grey = [0,65,65,65]
            emb_light_grey = [0,120,120,120]
            emb_dark_brown = [0,48,46,42]
            emb_dark_creme = [0,173,159,139]
            emb_mid_creme = [0,209,193,171]
            emb_mid_light_beige = [0,242,235,225]
            emb_off_white = [0,247,240,230]

            color_list = [emb_dark_grey,emb_light_grey, emb_creme, emb_dark_creme, emb_mid_creme, emb_off_white, emb_mid_light_beige]
            im = Image.open(filename)
            pixels = im.load()
            width, height = im.size

            for i in range(width):
                for j in range(height):
                    index = 0
                    for x in range(len(color_list)):
                        smallest = 255

                        R_VAL = (pixels[i,j])[0] - (color_list[x][1])
                        G_VAL = (pixels[i,j])[1] - (color_list[x][2])
                        B_VAL = (pixels[i,j])[2] - (color_list[x][3])
                        final_val = abs(R_VAL) + abs(G_VAL) + abs(B_VAL)

                        dfz = final_val

                        if dfz < smallest:
                            smallest = dfz
                            index = x

                    pixels[i,j] = (color_list[index][1], color_list[index][2], color_list[index][3])
            im.save(filename)

        except Exception as e:
            app.logger.debug(traceback.format_exc())
            return flask.jsonify({
                "error": "Error occurred applying filter"
            })

    return flask.jsonify({
        "resource": "/" + filename
    })

# ----------------------------------
# Init

if __name__ == "__main__":
    print("Opening for global access on port {}".format(app.port))
    app.run(port=app.port, host="0.0.0.0")
