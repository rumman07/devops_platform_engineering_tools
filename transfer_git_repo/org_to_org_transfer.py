import argparse
import requests
import time
import os
import logging
## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

## creating error.log file
with open(f'{c_dir}/error.log', 'w'):
    pass

## configure logging file
logging.basicConfig(filename=f'{c_dir}/error.log',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')

def transfer_repo(repo_name,old_owner,new_owner,token):
    url = f"https://api.github.com/repos/{old_owner}/{repo_name}/transfer"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "new_owner": f"{new_owner}",
        "new_name": f"{repo_name}"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 202 :
        print(f"{repo_name} this repo successfully transferred to organization {new_owner}")
    else :
        print(f"Transferring this {repo_name} repository is failed with status-code {response.status_code}")
        logging.error(f"Transferring this {repo_name} repository is failed with status-code {response.status_code}")
    return 

if __name__ == "__main__":
    ## for agr parse
    # parser = argparse.ArgumentParser(description="Transfer a GitHub repository")
    # parser.add_argument("repo_name", type=str, help="Name of the repository (REPO)")
    # args = parser.parse_args()
    GH_PAT = os.getenv("GH_PAT")
    org1_from = "testRez2"
    org2_to = "testRez1"
    # from file read the lines for the repo names
    with open('./repo_names.txt', 'r') as file:
        for line in file:
            repo_name = line.strip()
            response = transfer_repo(repo_name,org1_from,org2_to,GH_PAT)
            time.sleep(5)
