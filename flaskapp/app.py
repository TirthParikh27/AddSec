import os
from flask import Flask, flash, request, redirect, url_for, session
from flask import jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import yaml
import json
import time
from autoGit import cloneGit, pushGit

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
tools_list = ['CodeGuru', 'ZAP', 'Snyk']
tools_type = ['SAST', 'DAST', 'Compliance']
# secure pipeline dict
secure_flow = {}
# repo folder
repo_folder = 'ClonedRepo'


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

# @app.route('/upload', methods=['POST'])
# def fileUpload():
#     global filename
#     target=os.path.join(UPLOAD_FOLDER,'test_docs')
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     logger.info("welcome to upload`")
#     file = request.files['file']
#     filename = secure_filename(file.filename)
#     print(filename)
#     destination="/".join([target, filename])
#     file.save(destination)
#     session['uploadFilePath']=destination
#     response={"res" : "Successfully uploaded"}
#     return response

# get step names from workflow yaml
@app.route('/getNames')
def names():
    global file_dict
    global updated_steps
    global filename
    if len(updated_steps)==0:
        with open('{}/.github/workflows/{}'.format(repo_folder,filename)) as f:
            file_dict = yaml.safe_load(f)
        steps = file_dict['jobs']['deploy']['steps']
        for s in steps:
            s['visible'] = checkVisible(s)
            updated_steps.append(s)
    print("Returned step names")
    return jsonify(updated_steps)

# return the names of all steps and pos of tools
@app.route('/getNamesPos')
def namePos():
    global updated_steps
    return {'steps':updated_steps, 'pos':pos}

# return list of tools and type
@app.route('/getToolNames')
def toolNames():
    global tools_list
    global tools_type
    res = []
    for i in range(len(tools_list)):
        res.append(tools_list[i]+'('+tools_type[i]+')')
    print("Returned tool names")
    return jsonify(res)

# post the index of stages
@app.route('/setStagePos', methods=['POST'])
def setPos():
    global pos
    data = request.get_json()
    pos = data.get('pos','')
    response={"res" : "Successfully stored positions"}
    print("Successfully stored positions")
    return response

# make the changes to the pipeline
# {'id':{'data':{'label'}}}
@app.route('/setToolNames', methods=['POST'])
def makeSecure():
    global secure_flow
    global file_dict
    global repo_folder
    global filename
    tmp_pos_dict = {}
    tool_pos_dict = {}
    step_list = []
    data = request.get_json()
    # print(data)
    for row in data:
        try:
            if 'dndnode' in row['id']:
                try:
                    tmp_pos_dict[row['id']]=row['data']['label']
                except:
                    print('label??')
        except:
            print("NO SOURCE")
    for t in tmp_pos_dict:
        for r in data:
            try:
                if t == r['source']:
                    tool_pos_dict[r['target']] = tmp_pos_dict[t]
                elif t == r['target']:
                    tool_pos_dict[r['source']] = tmp_pos_dict[t]
            except:
                continue
    for i in data:
        try:
            if isinstance(int(i['id']), int):
                step_list.append(i['data']['label'])
            else:
                continue
            if i['id'] in tool_pos_dict:
                step_list.append(tool_pos_dict[i['id']])
        except:
            continue
    steps = file_dict['jobs']['deploy']['steps']
    l = []
    names = []
    for i in steps:
        if i['name'] in step_list:
            l.append(i)
            names.append(i['name'])
        elif 'slug' in i['name'] or 'checkout' in i['name']:
            l.append(i)
            names.append(i['name'])
    for j, s in enumerate(step_list):
        if s not in names:
            inlist = step_list[j-1]
            if 'codeguru' in s.lower():
                with open('tools/codeguru_1.json', 'r') as f:
                    json_data = json.load(f)
                    l.insert(names.index(inlist)+1,json_data)
                with open('tools/codeguru_2.json', 'r') as f:
                    json_data = json.load(f)
                    l.insert(names.index(inlist)+1,json_data)
            elif 'zap' in s.lower():
                with open('tools/zap.json', 'r') as f:
                    json_data = json.load(f)
                    l.insert(names.index(inlist)+1,json_data)
            elif 'docker' in s.lower():
                with open('tools/snyk.json', 'r') as f:
                    json_data = json.load(f)
                    l.insert(names.index(inlist)+1,json_data)

    secure_flow = file_dict
    secure_flow['jobs']['deploy']['steps'] = l
    f = open('{}/.github/workflows/{}'.format(repo_folder, filename), 'w')
    yaml.dump(secure_flow, f, allow_unicode=True)
    # push the changes to git repo
    pushGit("/"+repo_folder+"/.github/workflows/"+filename, "your pipeline has been secured", repo_folder)
    response={"res" : "Successfully integrated tools"}
    print("Successfully integrated tools and pushed")
    return response , 200

@app.route('/setRepo' , methods=['POST'])
def setRepo():
    global filename
    global repo_folder
    data = request.get_json()
    filename = data['filename']
    print(data)
    cloneGit(data['url'], repo_folder)
    response={"res" : "Successfully Found workflow file"}
    print("Successfully Found workflow file")
    return response , 200


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
