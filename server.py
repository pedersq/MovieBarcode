from flask import Flask, Response, render_template, request
from flask_cors import CORS
import string
import random
import sqlite3
import barcode_db
import barcode_gen

app = Flask(__name__)
CORS(app)

@app.route("/browse")
def recall_image():
    return render_template('browse.html')

@app.route("/get_image", methods=['POST'])
def send_img():

    video_id = request.args.get('vid_id')
    total_samples = float(request.args.get('total_samples'))
    video_title = request.args.get('title')
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.jpeg'
    print(total_samples)

    barcode_exists = barcode_db.contains_video(video_id, total_samples)
    if barcode_exists:
        print(barcode_exists)
        return Response(barcode_exists[0][4])

    response = None
    if barcode_gen.download_video(video_id):
        width, height = barcode_gen.gen_image(total_samples, filename)
        print("width:", width)
        print("height:", height)
        barcode_db.add_new_barcode(video_id,
                                   video_title,
                                   width,
                                   height,
                                   filename)

        response = Response(filename)
    else:
        response = Response('failed')
    return response

@app.route("/")
def hello_world():
    return render_template('index.html')


