import git
import os

def autoGit():
  # Check out via HTTPS
  repo = git.Repo.clone_from('https://github.com/TirthParikh27/AddSec' , 'AddSec')
  #repo = git.Repo('AddSec') 
  origin = repo.remote("origin")  
  print(repo)
  # Edit files
  f = open(os.path.abspath(os.getcwd())+"\AddSec\demofile.txt", "w")
  f.write("Script works ! We can edit and push workflow files")
  f.close()

  # Commit
  repo.index.add([os.path.abspath(os.getcwd())+'\AddSec\demofile.txt'])  # in this case filename would be "/User/some_user/some_dir/demofile.txt"
  repo.index.commit("Workflow edited - test 3")

  # Push
  repo.git.push("--set-upstream", origin, repo.head.ref)

autoGit()