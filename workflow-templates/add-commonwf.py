
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
        # os.system("code "+repoPath)
        return True
def pushChangesDefault(repoPath):
    try:
        repo = Repo(repoPath)
        repo.git.add(A=True)
        repo.config_writer().set_value("user", "name", "wfupdate").release()
        repo.config_writer().set_value("user", "email", "wfupdate@lummo.com").release()
        repo.git.commit(m="add:common workflow file")
        repo.git.push("origin")
    except:
        print('Some error occured while pushing the code'+repoPath)

def pushChangesMaster(repoPath,repoName,mainBranch): 
    
    try:
        repo = Repo(repoPath)
        repo.git.checkout(mainBranch)
        pushStatus=copyWorkflows(repoPath,repoName)
        if pushStatus:
                os.system("code "+repoPath)
                repo.git.add(A=True)
                repo.config_writer().set_value("user", "name", "wfupdate").release()
                repo.config_writer().set_value("user", "email", "wfupdate@lummo.com").release()
                repo.git.commit(m="add: common workflow file")
                repo.git.push("origin")
    except:
        print('Some error occured while pushing the code in master '+repoName)

def findBranches(repoPath,repoName):
    try:
        repo = Repo(repoPath)
        defaultBranch = repo.active_branch.name
        print ("Default Branch for "+repoName+": "+defaultBranch)
        mainBranch=defaultBranch
        remote_refs = repo.remote().refs
        for refs in remote_refs:
            # print (refs.name)
            if refs.name == "origin/master" or refs.name == "origin/main":
                mainBranch=refs.name
                if mainBranch == "origin/master":
                    mainBranch="master"
                else:
                    mainBranch="main"
        print ("Main Branch for "+repoName+": "+mainBranch)
        return defaultBranch,mainBranch,True
    except:
        print("Unable to Read from "+repoName)
        return "master","main",False

if __name__ == "__main__":
    repos=listRepos()
    print(len(repos))
    # repoPath,repoName=cloneRepo("singlerepo")
    # defaultBranch,mainBranch,branchStatus=findBranches(repoPath,repoName)
    # if branchStatus:
    #     if defaultBranch==mainBranch:
    #         pushChangesMaster(repoPath,repoName,mainBranch)
    #     else:
    #         pushStatus=copyWorkflows(repoPath,repoName)
    #         print(pushStatus)
    #         if pushStatus:
    #             pushChangesDefault(repoPath)
    #         pushChangesMaster(repoPath,repoName,mainBranch)
    # else:
    #     print("unable to get branch details")
    count=0
    for repo in repos:
        count=count+1
        print (count)
        if (count!=113):
            repoName=str(repo)
            print(repoName)
            repoPath,repoName=cloneRepo(repoName)
            defaultBranch,mainBranch,branchStatus=findBranches(repoPath,repoName)
            if branchStatus:
                if defaultBranch==mainBranch:
                    pushChangesMaster(repoPath,repoName,mainBranch)
                else:
                    pushStatus=copyWorkflows(repoPath,repoName)
                    if pushStatus:
                        pushChangesDefault(repoPath)
                    pushChangesMaster(repoPath,repoName,mainBranch)
            else:
                print("unable to get branch details")
