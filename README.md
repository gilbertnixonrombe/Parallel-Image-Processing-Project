# Parallel Image Processing

<p align="center">
  <img src="./images/banner.png" width="600">
</p>

<h4 align="center">IFB 206 Komputasi Paralel — Institut Teknologi Nasional Bandung</h4>

---

**Parallel Image Processing** is a web-based application that demonstrates the performance difference between **serial** and **parallel** image processing using Python's `multiprocessing` module. The app applies Canny edge detection to uploaded images, splitting the workload across 4 parallel processes and comparing execution time against the serial approach.

## Demo

Upload any grayscale or color image through the web interface, and the system will:
1. Process the image **serially** using OpenCV's `Canny` edge detector
2. Split the image into 4 horizontal chunks and process them **in parallel** using `multiprocessing.Pool`
3. Display the result image alongside both execution times

## System Architecture

```
User (Browser)
     │
     ▼
Flask Web Server (app.py)
     │
     ├── Serial Processing
     │       └── cv2.Canny(full_image)
     │
     └── Parallel Processing (Pool of 4 workers)
             ├── Worker 1 → cv2.Canny(chunk_1)
             ├── Worker 2 → cv2.Canny(chunk_2)
             ├── Worker 3 → cv2.Canny(chunk_3)
             └── Worker 4 → cv2.Canny(chunk_4)
                     └── np.vstack → merged result
```

## How It Works

### Image Splitting
The input image (loaded as grayscale) is divided into **4 equal horizontal chunks** using `numpy.array_split`. Each chunk is sent to a separate worker process.

```python
chunks = np.array_split(image, 4)
```

### Parallel Canny Edge Detection
Each worker applies Canny edge detection independently:

```python
def process_chunk(chunk):
    return cv2.Canny(chunk, 100, 200)

with Pool(4) as pool:
    processed = pool.map(process_chunk, chunks)
```

### Merging Results
The processed chunks are stacked back into a full image:

```python
parallel_result = np.vstack(processed)
```

### Performance Measurement
Both serial and parallel execution times are measured using `time.time()` and returned to the frontend for comparison.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Flask |
| Image Processing | OpenCV (`cv2`) |
| Parallelism | Python `multiprocessing.Pool` |
| Array Operations | NumPy |
| Frontend | HTML + Jinja2 |

## Project Structure

```
ParallelImageProcessing/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Web UI template
├── static/
│   ├── uploads/            # Uploaded images (auto-created)
│   └── results/            # Processed output images (auto-created)
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8 or newer
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/Student-Embedded-Control-and-AI-Fest/CuffnCode
cd ParallelImageProcessing
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

### Usage

1. Click **Choose File** and select an image (JPEG, PNG, etc.)
2. Click **Process**
3. View the Canny edge detection result and compare **Serial** vs **Parallel** execution times

## Dependencies

```
flask
opencv-python
numpy
pillow
```

Install all with:

```bash
pip install -r requirements.txt
```

## Parallelism Concept

This project illustrates **task parallelism** applied to image processing. By dividing the image into independent chunks, each chunk can be processed simultaneously on a separate CPU core, reducing total execution time for large images.

The speedup follows **Amdahl's Law**:

$$S = \frac{1}{(1 - P) + \frac{P}{N}}$$

Where:
- $S$ = theoretical speedup
- $P$ = proportion of parallelizable work
- $N$ = number of parallel processors (4 in this project)

In practice, overhead from process spawning and memory copying can reduce actual speedup on small images.

## Notes

- Processing time difference becomes more visible with **larger images**
- The app runs with `debug=True` — disable this for production
- On Windows, ensure the `if __name__ == "__main__":` guard is in place (already done in `app.py`) to avoid multiprocessing issues

## Credits

- OpenCV Canny Edge Detection: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
- Python multiprocessing documentation: https://docs.python.org/3/library/multiprocessing.html
- Flask documentation: https://flask.palletsprojects.com/

---

*IFB 206 Komputasi Paralel — Semester Genap 2025/2026 — Institut Teknologi Nasional Bandung*
