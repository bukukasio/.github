
import os
import github3
from git import Git
from git import Repo
import git
import time
from pathlib import Path


organization=os.environ.get('ORGANIZATION')
gitToken=os.environ.get('GIT_TOKEN')

def cloneRepo(repoName):
    ts = str(time.time())
    clonePath='/tmp/'+ts+'/'+repoName
    repoURL="https://"+gitToken+":x-oauth-basic@github.com/"+repoName
    with Git().custom_environment():
         Repo.clone_from(repoURL,clonePath)
    return clonePath,repoName


def listRepos(): 
    gh = github3.login("uname",gitToken)
    org = gh.organization(organization)
    repos = list(org.repositories(type="all"))
    return repos

def copyWorkflows(repoPath,repoName):
    wfPath=repoPath+"/.github/workflows/common-workflow.yml"
    WfDirectory=repoPath+"/.github/workflows"

    isExist = os.path.exists(wfPath)
    if isExist:
        print("Workflow exists skipping for repo "+repoName)
        return False
    else:
        print("Workflow doesn't exists creating workflow for repo "+repoName)
        wfDirectoryPath = Path(WfDirectory)
        wfDirectoryPath.mkdir(parents=True, exist_ok=True)
        os.system("cp "+"./common-workflow.yml "+WfDirectory)
        os.system("code "+repoPath)
        return True

def pushChangesDefault(repoPath):
    try:
        repo = Repo(repoPath)
        repo.git.add(A=True)
        repo.config_writer().set_value("user", "name", "wfupdate").release()
        repo.config_writer().set_value("user", "email", "wfupdate@keyvalue.systems").release()
        repo.git.commit(m="Add common workflow file")
        repo.git.push("origin")
    except:
        print('Some error occured while pushing the code'+repoPath)

def pushChangesMaster(repoPath,repoName): 
    try:
        repo = Repo(repoPath)
        repo.git.checkout("master")
        copyWorkflows(repoPath,repoName)
        if pushStatus:
            repo.git.add(A=True)
            repo.config_writer().set_value("user", "name", "wfupdate").release()
            repo.config_writer().set_value("user", "email", "wfupdate@keyvalue.systems").release()
            repo.git.commit(m="Add common workflow file")
            repo.git.push("origin")
    except:
        print('Some error occured while pushing the code in master '+repoName)

if __name__ == "__main__":

    repos=listRepos()

    # for repo in repos:
    #     repoName=str(repo)
    #     repoPath,repoName=cloneRepo(repoName)
    #     pushStatus=copyWorkflows(repoPath,repoName)
    #     if pushStatus:
        #     pushChangesDefault(repoPath)
        #     pushChangesMaster(repoPath,repoName)

