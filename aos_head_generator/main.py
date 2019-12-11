from io import BytesIO
from PIL import Image, ImageDraw
from flask import Flask, request, abort, send_file

def create_head(color):
    head = Image.open("template.png")
    draw = ImageDraw.Draw(head)
    draw.rectangle(((0, 0), (100, 50)), fill=color)

    bio = BytesIO()
    head.save(bio, "PNG")
    bio.seek(0)
    return bio

app = Flask(__name__)

@app.route("/v1/heads/<string>.png")
def send_image(string):
    if len(string) not in (6, 3):
        abort(400)

    l = len(str)//3
    color_str = string[0:l], string[l:l*2], string[l*2:l*3]
    color_str = map(lambda x: if len(x) < 2: x+x, color_str)
    
    color = tuple(int(i, 16) for i in color_str)

    image_binary = create_head(color)
    resp = send_file(image_binary, mimetype="image/png")
    resp.cache_control.max_age = 60 * 60 * 24
    resp.cache_control.public = True
    return resp
