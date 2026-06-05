from flask import Flask, render_template, request
import cv2
import numpy as np
import os
import time
from multiprocessing import Pool

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def process_chunk(chunk):
    return cv2.Canny(chunk, 100, 200)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            image = cv2.imread(filepath, 0)

            start = time.time()
            cv2.Canny(image, 100, 200)
            serial_time = time.time() - start

            chunks = np.array_split(image, 4)

            start = time.time()
            with Pool(4) as pool:
                processed = pool.map(process_chunk, chunks)

            parallel_result = np.vstack(processed)
            parallel_time = time.time() - start

            output_path = os.path.join(RESULT_FOLDER, "result.png")
            cv2.imwrite(output_path, parallel_result)

            result = {
                "image": output_path,
                "serial": round(serial_time, 4),
                "parallel": round(parallel_time, 4)
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
