
from flask import Flask, render_template, request
from sqlitedict import SqliteDict
import os
import json

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='')
logger = app.logger

files_table = SqliteDict('main.db', tablename="files", autocommit=True)


@app.route("/")
def image_view():
    img_filename = request.args.get('img')
    img_path = None
    if img_filename:
        img_path = os.path.join('static', img_filename)
        if img_filename not in files_table:
            files_table[img_filename] = {
                'filename': img_filename,
                'line_pos': None
            }
    else:
        return render_template(
            "list.html",
        )
    return render_template(
        "index.html",
        title='App',
        img_path=img_path,
        file_dict=files_table[img_filename]
    )


@app.route("/api/set_line", methods=['POST'])
def set_line():
    img_filename = request.args.get('img')
    if not img_filename:
        return 'missing img'
    
    line_pos = request.json.get('line_pos')
    file_dict = files_table[img_filename]
    file_dict['line_pos'] = line_pos
    files_table[img_filename] = file_dict
    logger.info(files_table[img_filename])
    return 'ok'


@app.route("/api/get_files", methods=['GET'])
def get_files():
    return dict(files_table)

@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    if request.files:
        image = request.files["file"]
        name = request.form.get('name')
        image.save(os.path.join('static', image.filename))
        files_table[image.filename] = {
            'name': name,
            'filename': image.filename,
            'line_pos': None,
            'cell_height': 15,
        }                
    else:
        return 'no image!'
    return 'ok'