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
# input json
file_dict = {}
# store position of commit, build, deploy stages
pos = {}
# steps
steps = []
# steps with visibility
updated_steps = []
# tools
tools_list = ['CodeGuru', 'ZAP']
tools_type = ['SAST', 'DAST']

# hide unnecessary steps in the ui
def checkVisible(step):
    black_list = ['checkout', 'slug']
    for word in black_list:
        try:
            if step['name'] != None:
                if word in step['name']:
                    return False
            if step['uses'] != None:
                if word in step['name']:
                    return False
            if step['run'] != None:
                if word in step['run']:
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
    global file_dict
    global updated_steps
    if len(updated_steps)==0:
        with open('test_docs/{}'.format(filename)) as f:
            file_dict = yaml.safe_load(f)
        steps = file_dict['jobs']['deploy']['steps']
        for s in steps:
            s['visible'] = checkVisible(s)
            updated_steps.append(s)
    return jsonify(updated_steps)

# return the names of all steps and pos of tools
@app.route('/getNamesPos')
def namePos():
    global updated_steps
    return {'steps':updated_steps, 'pos':pos}

# return tools
@app.route('/')
# post the index of stages
@app.route('/setStagePos', methods=['POST'])
def setPos():
    global pos
    data = request.get_json()
    pos = data.get('pos','')
    print(pos)
    response={"res" : "Successfully stored positions"}
    return response

# make the changes to the pipeline
@app.route('/setToolNames', methods=['POST'])
def makeSecure():
    secure_flow = {}
    data = request.get_json()
    print(data)
    response={"res" : "Successfully integrated tools"}
    return response , 200




if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
