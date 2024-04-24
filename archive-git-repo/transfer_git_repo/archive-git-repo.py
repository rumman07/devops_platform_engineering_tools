import requests
import time
import os
import json
import logging
## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

## creating error.log file
with open(f'{c_dir}/error.log', 'w'):
    pass

## configure logging file
logging.basicConfig(filename=f'{c_dir}/error.log',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')

def archive_repository(token, owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "archived":True
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Repository '{owner}/{repo}' archived successfully.")
    else:
        print(response.json())
        print(f"Failed to archive repository '{owner}/{repo}'. Status code: {response.status_code}")
        logging.error(f"Failed to archive repository '{owner}/{repo}'. Status code: {response.status_code}")

def archive_repositories_from_file(token, file_path):
    org_name = 'testRez2'
    with open(file_path, "r") as file:
        repositories = file.readlines()

    for repo_name in repositories:
        response = archive_repository(token=token, owner=org_name, repo=repo_name.strip())
        time.sleep(5)
if __name__ == '__main__' :
    token = os.getenv('GH_PAT')
    file_path = f"{c_dir}/repo_names.txt"
    archive_repositories_from_file(token, file_path)
