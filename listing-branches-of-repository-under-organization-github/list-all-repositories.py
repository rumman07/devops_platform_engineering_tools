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


def listAllRepositories( GH_PAT, ORG_NAME):
    try :

        ## list for the repositories
        repoNames = []

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
            URL = f"https://api.github.com/orgs/{ORG_NAME}/repos"

            print(f"[info] started fetching repository data for page_no {i}....")

            ## Response For GET request

            response = requests.get(url=URL, headers=headers, params=params)

            results = response.json() 
            
            

            if not results:
                ## if no results found that means there is not page that contain repositories
                print(f"[info] No Further Repository Found in this Organization {ORG_NAME} \n exiting from fetching repository info")
                break

            print(f"[success] fetching repository data successfull for page_no {i}")
            ## Listing repositories from the response

            for repository in results:
                repoNames.append(
                     repository['full_name']
                )
            i = i+1
            time.sleep(3)

        print("[info] started exporting repository_names in repo-list.csv file....")

        ## creating a dataframe to store the repository_names in csv format
        repoNamesDf = pd.DataFrame(repoNames, columns=["repository_name"])
        repoNamesDf.to_csv('repo-list.csv', index=False)

        print("[success] exporting repository_names successfull")

    except requests.exceptions.RequestException as e :
        error_msg = f'Error Occurred While Fetching Data: {e}'
        print(f"====={error_msg}=====")
        logging.error(error_msg)


if __name__ == "__main__" :

    GH_PAT = os.environ.get("GH_PAT")

    ORG_NAME = os.environ.get("ORG_NAME")

    listAllRepositories(GH_PAT,ORG_NAME)