import re
from flask import Flask, request, redirect, render_template, flash
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import os
import subprocess
import sys
import pathlib

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = "abc"


@app.route("/")
def index():
    return render_template("upload.html")


suffixes = (".mp4", ".mov", ".wmv", ".avi", ".webm", "mkv", ".flv")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    option = request.form.get("convert_num")

    target = os.path.join(APP_ROOT, "videos/")
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        if destination.endswith(suffixes):
            flash("Working on it...")
            file.save(destination)
            if option == "1":
                des_format = "mp4"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            elif option == "2":
                des_format = "mov"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            elif option == "3":
                des_format = "wmv"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            elif option == "4":
                des_format = "avi"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            elif option == "5":
                des_format = "webm"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            elif option == "6":
                des_format = "mkv"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            elif option == "7":
                des_format = "flv"
                check_same_format(destination, des_format)
                convert(destination, des_format)
            else:
                print("Invalid Input")
        else:
            flash("Invalid file format")
    return render_template("complete.html")


# @app.route("/checking")
def check_same_format(destination, received_format):
    if received_format in destination:
        flash("Its already in that format. Try different format.")
        sys.exit()
    else:
        return


def compress(video_file):
    temp = video_file
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_file,
            "-vcodec",
            "h264",
            "-acodec",
            "aac",
            video_file.replace(
                "." + video_file.split(".")[-1],
                "-compressed." + video_file.split(".")[-1],
            ),
        ]
    )
    if os.path.exists(temp):
        os.remove(temp)


def convert(file_src, dest_format):
    temp1 = file_src
    temp2 = temp1.split(".")
    temp2[-1] = dest_format
    dest_path = ".".join([str(elem) for elem in temp2])

    # cmd="ffmpeg -i in.mp4 -y out.avi"
    process = subprocess.Popen(
        ["ffmpeg", "-i", file_src, "-y", dest_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    for line in process.stdout:
        print(line)
    compress(dest_path)


if __name__ == "__main__":
    app.run(debug=True)
