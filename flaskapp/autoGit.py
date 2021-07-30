import git
import os

def cloneGit(url , dirName):
  # Check out via HTTPS
  #repo = git.Repo.clone_from('https://github.com/TirthParikh27/AddSec' , 'AddSec')
  repo = git.Repo.clone_from(url , dirName)
  #repo = git.Repo('AddSec') 
  origin = repo.remote("origin")  

def pushGit(filePath , msg , dirName):
  repo = git.Repo(dirName) 
  # Commit
  #repo.index.add([os.path.abspath(os.getcwd())+'\AddSec\demofile.txt'])  # in this case filename would be "/User/some_user/some_dir/demofile.txt"
  repo.index.add([os.path.abspath(os.getcwd())+filePath]) 
  #repo.index.commit("Workflow edited - test 3")
  repo.index.commit(msg)

  # Push
  repo.git.push("--set-upstream", origin, repo.head.ref)

