import requests
import pandas as pd 
import os
import logging

## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

path =f'{'/'.join(os.path.dirname(__file__).split('/')[0:-2])}/ado2gh_migration_scripts/MigrationWithoutAssigningTeam/checkAfterMigration/orgRepositories.csv'

repo_under_organization = pd.read_csv(path)
repo_names = repo_under_organization['full_name'].to_numpy()
## ensuring if the error.log file exists or not
if not os.path.exists(f'{c_dir}/error.log'):
    with open(f'{c_dir}/error.log', 'w'):
        pass


## configure logging file
logging.basicConfig(filename=f'{c_dir}/error.log',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
def get_lang_in_repositories(gh_pat):
    try :
        # request header
        columns = ['repo_name','languages_used']
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
            keys_str = ', '.join(keys)
            data = [[repo_name, keys_str]]
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
    org_name = "utesta"
    df = get_lang_in_repositories(gh_pat)
    df.to_csv(f'{c_dir}/laguageStatusGitHub.csv',index=False)
