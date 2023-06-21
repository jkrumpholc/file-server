import json
import os
from datetime import datetime
from flask import Flask, request, redirect, render_template, send_from_directory
from flask_cors import CORS, cross_origin


app = Flask(__name__, template_folder='html')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/upload_page')
@cross_origin()
def upload():
    return render_template("upload.html")


@app.route('/message')
@cross_origin()
def uploaded():
    return render_template("message.html", file=request.args.get('file_name'), action=request.args.get('action'))


@app.route('/upload_file', methods=["POST"])
@cross_origin()
def upload_file():
    if request.files.get("file") is None:
        return {"result": "False"}
    f = request.files["file"]
    if f.filename == '':
        return render_template("error.html", message="File not included")
    if not os.path.exists(os.getcwd() + "/upload"):
        os.mkdir(os.getcwd() + "/upload")
    f.save(os.getcwd() + "/upload/" + f.filename)
    return redirect(f'/message?file_name={f.filename}&action=uploaded')


@app.route('/get_file')
@cross_origin()
def get_file():
    file = request.args.get("file")
    if os.path.exists(f"{os.getcwd()}/{file}"):
        return send_from_directory(os.getcwd(), file)
    return


@app.route('/download')
@cross_origin()
def download():
    return render_template("download.html")


@app.route('/list_files')
@cross_origin()
def list_files():
    try:
        ret = {"files": []}
        upload_path = os.getcwd() + '/upload'
        for i, n in enumerate(os.listdir(upload_path)):
            m = f"{upload_path}/{n}"
            if os.path.isfile(m):
                name, type = n.rsplit(".", 1)
                ret["files"].append(
                    {"name": name, "type": type, "size": f"{os.path.getsize(m)} B",
                     "date": datetime.fromtimestamp(os.path.getmtime(m)).strftime('%d.%m.%Y %H:%M:%S')})
        return json.dumps(ret)
    except Exception as e:
        print(e)


@app.route('/stats')
@cross_origin()
def stats():
    return render_template("stats.html")


@app.route('/get_stats')
@cross_origin()
def get_stats():
    path = f"{os.getcwd()}/upload"
    sizes = []
    for i in os.scandir(path):
        sizes.append(os.path.getsize(i))
    sizes.sort()
    sum_size = sum(sizes)
    num_file = len(os.listdir(path))
    ret = {"number": num_file, "total_size": sum_size, "mean_size": round(sum_size / num_file, 1),
           "median_size": sizes[(len(sizes) // 2)]}
    return json.dumps(ret)


@app.route('/delete')
@cross_origin()
def delete():
    return render_template("delete.html")


@app.route('/delete_file')
@cross_origin()
def delete_file():
    file = request.args.get("file")
    os.remove(os.getcwd() + file)
    return redirect(f'/message?file_name={file.rsplit("/")[-1]}&action=deleted')


@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="This page doesn't exist")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8001)
