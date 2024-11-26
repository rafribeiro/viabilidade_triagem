from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)

# Load images
IMAGE_FOLDER = "static/images"
images = sorted(os.listdir(IMAGE_FOLDER))

# File to store responses
RESPONSES_FILE = "responses.csv"

# Ensure the CSV file exists
if not os.path.exists(RESPONSES_FILE):
    with open(RESPONSES_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Image", "Response"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        return redirect(url_for("survey", name=name, email=email, index=0))
    return render_template("index.html")

@app.route("/survey/<name>/<email>/<int:index>", methods=["GET", "POST"])
def survey(name, email, index):
    if index >= len(images):
        return render_template("thank_you.html")

    image = images[index]
    if request.method == "POST":
        response = request.form["response"]

        # Save response to CSV
        with open(RESPONSES_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, image, response])

        return redirect(url_for("survey", name=name, email=email, index=index+1))

    return render_template("survey.html", image=image, index=index, total=len(images))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
