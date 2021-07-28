import os
from flask import Flask, flash, request, redirect, url_for, session
from flask import jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import yaml
import time

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')



UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','yml'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

# file name of uploaded workflow
filename = ''
# store position of commit, build, deploy stages
pos = {}
# steps
steps = []

# hide unnecessary steps in the ui
def checkVisible(inp):
    black_list = ['checkout', 'slug']
    for word in black_list:
        try:
            if inp['name'] != None:
                if word in inp['name']:
                    return False
            if inp['uses'] != None:
                if word in inp['name']:
                    return False
            if inp['run'] != None:
                if word in inp['run']:
                    return False
        except:
            continue
    return True

@app.route('/upload', methods=['POST'])
def fileUpload():
    global filename
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response={"res" : "Successfully uploaded"}
    return response

# get step names from workflow yaml
@app.route('/getNames')
def names():
  with open('test_docs/{}'.format(filename)) as f:
    inp = yaml.load(f)
    steps = inp['jobs']['deploy']['steps']
    # print(steps)
    updated_steps = []
    for s in steps:
        s['visible'] = checkVisible(s)
        updated_steps.append(s)
    return jsonify(updated_steps)

# return the names of all steps and pos of tools
@app.route('/getNamesPos')
def namePos():
  return {'steps':steps, 'pos':pos}

# post the index of stages
@app.route('/setPos', methods=['POST'])
def setPos():
  data = request.get_json()
  positions = data.get('pos','')
  pos = positions
  print(pos)
  response={"res" : "Successfully stored positions"}
  return response

# make the changes to the pipeline
@app.route('/secure')
def makeSecure():
  pass



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
