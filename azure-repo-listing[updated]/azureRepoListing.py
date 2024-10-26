import requests 
import pandas as pd
import os
import logging
import time

## for logger
## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

## creating error.log file
with open(f'{c_dir}/error.log', 'w'):
    pass

## configure logging file
logging.basicConfig(filename=f'{c_dir}/error.log',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')


# auth creation and header 
def getAuth(ado_pat) :
    ## header config
    headers = {"Content-Type": "application/json"}

    ## for Basic Auth
    auth = ('', ado_pat)

    return (headers,auth)

## listing all of the projects under an organization
def getProjects(organization,headers,auth) :
    try:
        url = f"https://dev.azure.com/{organization}/_apis/projects?api-version=7.1-preview.4"
        # Make the request to Azure DevOps REST API
        response = requests.get(url,headers=headers,auth=auth )
        # Check if the request was successful
        if response.status_code == 200:
            print('Projects Information Successfully Extracted!!!')
            results = response.json()
            projects_info = results['value']
            project_names = []
            ## storing the project names in our list project_names
            for i in range(len(results['value'])) :
                project_names.append(results['value'][i]['name'])
            return project_names
        else:
            # if for any request error happens it will be in log
            print(f"Request failed with status code: {response.status_code}")
            logging.error(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"An error occurred: {str(e)}")
        return None

## listing all repositories with neccessary information 
def getRepositories(project_names,organization,headers,auth) :
    try :
        repositories=[]
        for i in range(len(project_names)) :
            project_name = project_names[i]
            url = f"https://dev.azure.com/{organization}/{project_name}/_apis/git/repositories?api-version=7.2-preview.1" 
            response = requests.get(url,headers=headers,auth=auth)
            if response.status_code == 200 :
                results = response.json()
                for j in range(len(results['value'])):
                    repositories.append({
                        'project_name':project_names[i],
                        'repo_name':results['value'][j]['name'],
                        'repo_id':results['value'][j]['id']
                    })
                # give sleep timer because of handling frequent request
                time.sleep(5)
                print(f'Repositories Extracted Successfully From Project {project_names[i]}!!')
            else :
                print(f"Request failed with status code: {response.status_code} for Project {project_names[i]}")
                logging.error(f"Request failed with status code: {response.status_code} for Project {project_names[i]}")
        return repositories
    except Exception as e :
        print(f'An Error Occurred: {str(e)}')
        logging.error(f'An Error Occurred: {str(e)}')
        return None
    
## give info about active pull request or disability of the repo or inaccessibility of that repo
def hasActivePullRequest(repo_name,repo_id,organization,project_name,headers,auth):
    try :
        url = f"https://dev.azure.com/{organization}/{project_name}/_apis/git/repositories/{repo_id}/pullRequests?searchCriteria.status=active&skip=0"
        response = requests.get(url,headers=headers,auth=auth)
        if response.status_code == 200 :
            time.sleep(5)
            if response.json()['count']>0 :
                print(f'This repo {repo_name} from this project {project_name} has Active Pull Request!!')
            else :
                print(f'This repo {repo_name} from this project {project_name} doesn\'t have Active Pull Request!!')
            return response.json()['count']>0
        else :
            if "NotFound" in response.json()['typeKey'] :
                return "repo_inaccessible"
            else :
                return response.status_code
    except Exception as e :
        print(f'An Error Occurred: {str(e)}')
        logging.error(f'An Error Occurred: {str(e)}')
        return None

def getRepoSize(org_name, project_name, repo_id, repo_name,headers, auth):
        url = f"https://dev.azure.com/{org_name}/{project_name}/_apis/git/repositories/{repo_id}/items?api-version=7.1&recursionLevel=Full&includeContentMetadata=true"
        response = requests.get(url,headers=headers,auth=auth)
        size = int(0)
        if response.status_code == 200 :
            results = response.json()
            for i in range(len(results['value'])):
                object_id = results['value'][i]['objectId']
                object_type = results['value'][i]['gitObjectType']
                if object_type == "blob" :
                    url_item = f'https://dev.azure.com/{org_name}/{project_name}/_apis/git/repositories/{repo_id}/blobs/{object_id}?$format=json&api-version=7.1'
                    res_item = requests.get(url_item,headers=headers,auth=auth)
                    if res_item.status_code == 200 :
                        results_item = res_item.json()
                        size = size + int(results_item['size'])
                    else :
                        print(f"Request failed with status code: {response.status_code} for Project {project_name} Repository_Name {repo_name} File Info not found")
                        logging.error(f"Request failed with status code: {response.status_code} for Project {project_name} Repository_Name {repo_name} File Info not found")
                    time.sleep(3)
                
        else :
            print(f"Request failed with status code: {response.status_code} for Project {project_name} Repository_Name {repo_name}")
            logging.error(f"Request failed with status code: {response.status_code} for Project {project_name} Repository_Name {repo_name}")
        time.sleep(5)
        print(f"[info] This repository {repo_name} has total {size} bytes of data")
        return size
## for getting the latest commit info from a repository based on main or master branch
def getRepoDetailedInfo(repositories_info, organization, headers, auth) :
    column_names = ['project_name','repository_name','repository_size_in_mb','branch_name',
                    'repository_id','last_commit_id','haveActivePullRequests',
                    'committer_name','last_commit_date','comment','last_commit_link']
    df = pd.DataFrame()
    try :
        for repo_info in repositories_info :
            project_name = repo_info['project_name']
            repo_id = repo_info['repo_id']
            repo_name = repo_info['repo_name']
            response = hasActivePullRequest(repo_name,repo_id,organization,project_name,headers,auth)
            repository_size = round(getRepoSize(organization, project_name, repo_id, repo_name, headers, auth)*0.00000095367432, 4)
            if response == True or response == False :
                # for main branch
                isActive = response
                name = "main"
                url = f"https://dev.azure.com/{organization}/{project_name}/_apis/git/repositories/{repo_id}/stats/branches?name={name}&api-version=7.1-preview.1"
                response = requests.get(url,headers=headers,auth=auth)
                if response.status_code == 200 :
                    result = response.json()
                    project_name = repo_info['project_name']
                    repo_name = repo_info['repo_name']
                    # extracting the commit info
                    commit_info = result.get('commit', {})
                    # extracting the branch name
                    branch_name = result.get('name',{})
                    commitId = commit_info.get('commitId', '')
                    committerName = commit_info.get('committer', {}).get('name', '')
                    commitDate = pd.to_datetime(commit_info.get('committer', {}).get('date', ''))
                    comment = commit_info.get('comment', '')
                    commitURL = commit_info.get('url', '')
                    data = [project_name,repo_name,repository_size,branch_name,repo_id,
                            commitId,isActive,committerName,commitDate,
                            comment,commitURL]
                    n_df = pd.DataFrame([data],columns=column_names)
                    df = pd.concat([df,n_df],axis=0,ignore_index=True)
                    time.sleep(5)
                    print(f'Latest Commit Information Extracted Successfully From repo {repo_name} in project {project_name}')
                    continue
                else :
                    # for master branch
                    name = "master"
                    url = f"https://dev.azure.com/{organization}/{project_name}/_apis/git/repositories/{repo_id}/stats/branches?name={name}&api-version=7.1-preview.1"
                    response = requests.get(url,headers=headers,auth=auth)
                    if response.status_code == 200 :
                        result = response.json()
                        project_name = repo_info['project_name']
                        repo_name = repo_info['repo_name']
                        # extracting the commit info
                        commit_info = result.get('commit', {})
                        # extracting the branch name
                        branch_name = result.get('name',{})
                        commitId = commit_info.get('commitId', '')
                        committerName = commit_info.get('committer', {}).get('name', '')
                        commitDate = pd.to_datetime(commit_info.get('committer', {}).get('date', ''))
                        comment = commit_info.get('comment', '')
                        commitURL = commit_info.get('url', '')
                        data = [project_name,repo_name,repository_size,branch_name,repo_id,
                                commitId,isActive,committerName,commitDate,
                                comment,commitURL]
                        n_df = pd.DataFrame([data],columns=column_names)
                        df = pd.concat([df,n_df],axis=0,ignore_index=True)
                        time.sleep(5)
                        print(f'Latest Commit Information Extracted Successfully From repo {repo_name} in project {project_name}')
                        continue
                    else :
                        print(f'The request came with a response with status code {response.status_code} for repository {repo_info["repo_name"]} on this project {repo_info["project_name"]}')
                        logging.error(f'The request came with a response with status code {response.status_code} for repository {repo_info["repo_name"]} on this project {repo_info["project_name"]}')
                        continue
            ## if the repo is disabled or inaccessible because of authenticity
            elif response == 'repo_inaccessible' :
                print(f'Repository Is Disabled or You Do Not Have Permission For This Repository : project_name: {repo_info["project_name"]} repo_name: {repo_info["repo_name"]},repo_id: {repo_id}')
                logging.error(f'Repository Is Disabled or You Do Not Have Permission For This Repository : project_name: {repo_info["project_name"]} repo_name: {repo_info["repo_name"]},repo_id: {repo_id}')
                continue
            ## or there is another problem with the response
            else :
                print(f'The request came with a response with status code {response} for repository {repo_info["repo_name"]} on this project {repo_info["project_name"]}')
                logging.error(f'The request came with a response with status code {response} for repository {repo_info["repo_name"]} on this project {repo_info["project_name"]}')
                continue
        return df
    except Exception as e :
        print(f'An Error Occurred: {str(e)}')
        logging.error(f'An Error Occurred: {str(e)}')
        return None


if __name__ == '__main__' :
    # Azure DevOps organization name
    organization = 'udemydevopscourse'
    # Azure Personal Access token from environment variable
    ado_pat = os.environ.get('ADO_PAT')
    headers,auth = getAuth(ado_pat)
    # get project names
    projects_names = getProjects(organization,headers,auth)
    time.sleep(5)
    if projects_names is not None :
        # get repositories information based on project names
        repositories_info = getRepositories(projects_names,organization,headers,auth)
        if repositories_info is not None :
           # getting repositories detailed information and sorting based on time ascending
           repo_detailed_info = getRepoDetailedInfo(repositories_info,organization,headers,auth)
           repo_detailed_info = repo_detailed_info.sort_values(by="last_commit_date",ascending=False)
           # saving it in a csv format file to be understandable
           repo_detailed_info.to_csv(f'{c_dir}/azure_repo_list[updated].csv',index=False)
           print("Successfully Dumped The Informations of each Repositories into the azure_repo_list[updated].csv")
        else :
            print(f'Not Found Any Repositories for Any of The Projects On this organization {organization}')
            logging.error(f'Not Found Any Repositories for Any of The Projects On this organization {organization}')
            exit()
    else :
        print(f'Not Found Any Projects On this organization {organization}')
        logging.error(f'Not Found Any Projects On this organization {organization}')
        exit()
    


