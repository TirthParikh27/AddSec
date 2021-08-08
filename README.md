# AddSec
Add "SEC" to DevOps
Note : Configure aws credentials , slack token , sonarcloud token and any other required tokens to your demo repository 
# Setup
## Flask server
1) run "pip install -r requirements.txt"
2) cd flaskapp
3) Finally run  "python app.py" to start the server

## React UI
1) cd ui
2) npm install
3) npm start

# Page 1 : Load your pipeline
![image](https://user-images.githubusercontent.com/47681913/128626418-2f616cf7-e7ea-4362-80fb-44346c96aa26.png)
This is the first page where you follow the 3 steps to import your existing github actions pipeline
1) Enter github repo and workflow name
2) Label the Commit , Build and Deploy stages of your pipeline (you have a list of all extracted steps)
3) Configure security automation tools  , enter the required details

# Page 2 : Integrate Tools
![image](https://user-images.githubusercontent.com/47681913/128626573-210388cb-f490-482c-a6ec-fa2df883be8d.png)
This is the second page where you can visualise your uploaded pipeline and integrate security tools by dragging and dropping tools
from the sidebar and attaching them at the correct location in the pipeline.
Press Integrate when you are done adding tools and this will push your new workflow to the hithub repo provided earlier and ask for credentials in your flask server terminal.
