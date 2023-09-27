from flask import Flask, request, render_template, send_from_directory
import qrcode
from PIL import Image
import hashlib

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encode", methods=["POST"])
def encode():
    url = request.form.get("url")
    
    # Create a unique and valid filename using the hash of the URL
    filename_hash = hashlib.sha1(url.encode()).hexdigest()
    qr_filename = f"qr_codes/{filename_hash}.png"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_img.save(qr_filename)

    return render_template("index.html", qr_filename=qr_filename)

@app.route("/decode/<filename>")
def decode(filename):
    img = Image.open(f"qr_codes/{filename}")
    decoded_data = qrcode.decoding.qr_decode(img)
    return render_template("index.html", decoded_data=decoded_data[0].data.decode())

@app.route("/qr_codes/<filename>")
def serve_qr_code(filename):
    return send_from_directory("qr_codes", filename)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
