## Imports
import os 
import requests
import logging
import pandas as pd 
import time 

## extracting corrent directory from the file name
currentDirectory = os.path.dirname(os.path.realpath(__file__))

## checking the error.log file exists or not
if not os.path.exists(f'{currentDirectory}/error.log'):
    with open(f'{currentDirectory}/error.log','w'):
        pass


def listAllBranchByRepositories( GH_PAT, REPO_NAME):
    try :

        ## list for the branches in the repo
        repoBranches = []

        ## For Page_No
        i= int(1) 
        while True :

            ## Request Headers

            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {GH_PAT}",
                "X-GitHub-Api-Version": "2022-11-28"
            }

            ## Request Parameters
            params = {
                "per_page":100,
                "page":i
            }
            
            ## Request URL
            URL = f"https://api.github.com/repos/{REPO_NAME}/branches"

            print(f"[info] started fetching repository branch data for page_no {i}....")

            ## Response For GET request

            response = requests.get(url=URL, headers=headers, params=params)

            ## converting the response into json format
            results = response.json() 
            
            if not results :
                ## if no results found that means there is not page that contain repositories
                print(f"[info] No Further Branch Found in this repository {REPO_NAME} \n exiting from fetching branch info")
                break

            print(f"[success] fetching branch data successfull for page_no {i}")

            ## Listing branch from the response

            for branch in results:
                repoBranches.append(
                  {
                    "organization_name": REPO_NAME.split("/")[0],
                    "repostiory_name": REPO_NAME.split("/")[1],
                    "branch_name": branch['name'],
                    "is_protected": branch['protected'],
                    "last_commit_link": branch['commit']['url'],
                  }
                )
            i = i+1
            time.sleep(3)

        return repoBranches 

    except requests.exceptions.RequestException as e :
        error_msg = f'Error Occurred While Fetching Data: {e}'
        print(f"====={error_msg}=====")
        logging.error(error_msg)


if __name__ == "__main__" :

    GH_PAT = os.environ.get("GH_PAT")
    
    repoNamesDf = pd.read_csv("./repo-list.csv")

    repoNames = repoNamesDf['repository_name'].to_list()
    
    branchesList = []
    for REPO_NAME in repoNames:
        print(f"[info] started fetching branch list for repo {REPO_NAME.split("/")[-1]}")

        repoBranchList = listAllBranchByRepositories(GH_PAT,REPO_NAME)

        print(f"[success] successfully fetched branch list for repo {REPO_NAME.split("/")[-1]}")

        branchesList.extend(repoBranchList)

    branchesDf = pd.DataFrame(branchesList)
    branchesDf.to_csv("./branches-list.csv", index=False)