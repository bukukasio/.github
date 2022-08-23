
import os
import github3
from git import Git
from git import Repo
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
    wfPath=repoPath+"/.github/workflows/common-workflows.yml"
    WfDirectory=repoPath+"/.github/workflows"

    isExist = os.path.exists(wfPath)
    if isExist:
        print("Workflow exists skipping for repo "+repoName)
    else:
        print("Workflow doesn't exists creating workflow for repo "+repoName)
        wfDirectoryPath = Path(WfDirectory)
        wfDirectoryPath.mkdir(parents=True, exist_ok=True)
        os.system("cp "+"./common-workflow.yml "+WfDirectory)
        os.system("code "+repoPath)
    
if __name__ == "__main__":

    repos=listRepos()
    repoPath,repoName=cloneRepo(str(repos[0]))
    copyWorkflows(repoPath,str(repos[0]))