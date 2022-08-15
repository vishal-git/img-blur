from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from cv2 import (
    resize,
    imdecode,
    IMREAD_COLOR,
    cvtColor,
    COLOR_BGR2RGB,
    GaussianBlur,
    COLOR_BGR2GRAY,
    CV_64F,
    Laplacian,
)
from numpy import frombuffer, array, uint8, float32
from PIL.Image import fromarray


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# overall page design
HEAD_HTML = """
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
    </head>
    <body style="background-color: #222;">
    <center>
    """


@app.post("/", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
async def main():
    # fmt: off
    content = (
        HEAD_HTML
        + """<h1 style="color: #0AC663;
                        font-family: monospace;
                        font-weight: extra-bold;
                        font-stretch: extra-expanded;
                        text-align: center">IMAGE BLURRINESS DETECTION
             </h1>"""
        + """<br><br><h3 style="color: white;
                         font-family: monospace">
                         Upload a picture to check whether it's blurry or not:
                     </h3>
             <br>"""
    )

    content = (
        content
        + """
        <br/>
        <br/>
        <form action="/result/" enctype="multipart/form-data" method="post">
        <input style="background-color: #900C3F;
                      padding: .5em;
                      -moz-border-radium: 5px;
                      -webkit-border-radius: 5px;
                      border-radius: 6px;
                      color: #EDEAE6;
                      font-size: 18px;
                      text-decoration: none;
                      border: none;" name="files" type="file">
        <input style="background-color: #900C3F;
                      padding: .5em;
                      -moz-border-radium: 5px;
                      -webkit-border-radius: 5px;
                      border-radius: 6px;
                      color: #EDEAE6;
                      font-size: 20px;
                      text-decoration: none;
                      border: none;" type="submit">
        </form>
        </body>
        """
    )
    # fmt: on

    return content


@app.post("/result/", response_class=HTMLResponse)
async def show_results(files: UploadFile = File(...)):
    """Runs blurriness in an image and display the image
    on the results page with a note (blurry or not)."""

    """
    images = []
    for file in files:
        f = await file.read()
        images.append(f)
    """
    image = await files.read()
    image_name = files.filename

    image = frombuffer(image, uint8)
    image = imdecode(image, IMREAD_COLOR)
    image_resized = resize(image, (224, 224))

    image_blurred = GaussianBlur(image_resized, (3, 3), 0)
    image_grayed = cvtColor(image_blurred, COLOR_BGR2GRAY)
    laplacian = Laplacian(image_grayed, CV_64F)
    blurriness_score = laplacian.var()

    if blurriness_score < 30:
        msg = f"The image is quite blurry! (score:{blurriness_score:.0f})"
    elif blurriness_score < 80:
        msg = f"The image is blurry. (score:{blurriness_score:.0f})"
    elif blurriness_score < 140:
        msg = f"The image is a little blurry. (score:{blurriness_score:.0f})"
    else:
        msg = f"The image does not seem to be blurry (score:{blurriness_score:.0f})"

    # resize and save the image (for display)
    image_rgb = cvtColor(image_resized, COLOR_BGR2RGB)
    pillow_image = fromarray(image_rgb)
    pillow_image.save("static/" + image_name)
    image_path = "static/" + image_name

    # fmt: off
    tbl = "<table align='center'>"
    tbl += "<tr></tr>"
    tbl += "<tr></tr>"
    tbl += "<td><img height='300' src='/" + image_path + "'></td>"
    tbl += "<td style='color: white; font-size: 18px; font-family: monospace; font-weight: bold; font-stretch: extra-expanded; text-align: right'>" + msg + "</td>"

    content = (
        HEAD_HTML
        + """<h1 style="color: #0AC663;
             font-family: monospace;
             font-weight: extra-bold;
             font-stretch: extra-expanded;
             text-align: center">IMAGE BLURRINESS: PREDICTION</h1>"""
        + str(tbl)
        + """<br><form method="post" action="/">
                 <button style="background-color: #900C3F;
                                padding: .5em;
                                -moz-border-radium: 5px;
                                -webkit-border-radius: 5px;
                                border-radius: 6px;
                                color: #EDEAE6;
                                font-size: 20px;
                                text-decoration: none;
                                border: none;" type="submit">Home</button></form>"""
    )

    return content
