import requests
import pandas as pd 
import os
import logging
import matplotlib.pyplot as plt
## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

## ensuring if the error.log file exists or not
if not os.path.exists(f'{c_dir}/error.log'):
    with open(f'{c_dir}/error.log', 'w'):
        pass
## configure logging file
logging.basicConfig(filename=f'{c_dir}/error.log',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
def get_user_repositories(gh_pat,org_name):
    try :
        ## page no
        i = int(1)
        repositories_info = []
        while True :
            # request header
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {gh_pat}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            ## parameters to pass to the rest api
            params={
                "per_page":100,
                "page":i,
            }
            url = f"https://api.github.com/orgs/{org_name}/repos"
            response = requests.get(url, headers=headers,params=params)
            
            # getting the response into json format
            results = response.json()
            # if there is no repos in that page then break
            if not results :
                break
            for repository in results :
                repositories_info.append(
                    
                    repository['full_name']
                );
            i = i + 1
        return repositories_info
    except requests.exceptions.RequestException as e :
        error_msg = f'Error occurred while fetching data : {e}'
        print(error_msg)
        logging.error(error_msg)

def get_lang_in_repositories(gh_pat,repo_names):
    try :
        # request header
        columns = ['repo_name','language_used']
        df = pd.DataFrame()
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {gh_pat}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        for repo_name in repo_names :
            url = f"https://api.github.com/repos/{repo_name}/languages"
            response = requests.get(url, headers=headers)
            # getting the response into json format
            results = response.json()
            keys = list(results.keys())
            for lang in keys :
                data = [[repo_name, lang]]
                n_df = pd.DataFrame(data, columns=columns)
                df = pd.concat([df,n_df],axis=0,ignore_index=True)
        return df
    except requests.exceptions.RequestException as e :
        error_msg = f'Error occurred while fetching data : {e}'
        print(error_msg)
        logging.error(error_msg)


if __name__ == "__main__" :

    # GitHub Personal Access Token
    gh_pat = os.environ.get("GH_PAT")
    # Github User Name
    org_name = "freeCodeCamp"
    repo_names = get_user_repositories(gh_pat,org_name)
    df = get_lang_in_repositories(gh_pat,repo_names)
    df.to_csv(f'{c_dir}/laguageStatusGitHub.csv',index=False)
