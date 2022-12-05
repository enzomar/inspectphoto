from flask import Flask, jsonify
from flask import request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import render_template
import inspectphoto


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# https://pythonbasics.org/flask-upload-file/
@app.route('/inspect', methods = ['GET', 'POST'])
def inspect():
   if request.method == 'POST':
      f = request.files['file']
      #print(dir(f))
      #print(f.stream)
      #sf = secure_filename(f.filename)
      #f.save(sf)
      info = inspectphoto.run(f)
      print(info)
      return jsonify(info)


if __name__ == '__main__':
    app.run()
