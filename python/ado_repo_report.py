"""
Script - Azure DevOps organization repositories list and sort them based on 
last commit date.
Writting a python script to get the last change information of 
repositories on different projects under an organization  
"""

## dependencies
# requests for requesting the REST API
# pandas for using DataFrame Datastructure to perform filtering and sorting
# pandas also for creating the csv files

# To handle the request and response from the REST API
import requests 
# Structuring the data and filtering on it
import pandas as pd
# For taking in environmental variable 
import os

## personal access token
PATS = "njbp5vl3a6xg3vm2voubjzctqv3zz7r4s5zszqrzljuqf2mhmfba"
## organization name
organization = "udemydevopscourse"
## REST API url to get all of the project in that specific organization
url = f"https://dev.azure.com/{organization}/_apis/projects?api-version=7.1-preview.4"
## header config
headers = {"Content-Type": "application/json"}
## for basic auth
auth = ('', PATS)
## all of the project names will be stored here in this list
project_names = []
## all of the repositories names will be stored here in this list
repository_names = []
## Repository ids will be stored here in this list
repository_ids = []
## column names in our csv file to make it more readable and understandable
column_names = ['project_name',
                'repository_name',
                'repository_id',
                'last_commit_id',
                'committer_name',
                'last_commit_date',
                'comment',
                'last_commit_link']
## creating a blank data frame to store data in an organized way
df = pd.DataFrame()

## requesting to the REST API and get the response
response = requests.get(url, headers=headers, auth=auth)

## checking if the response is valid
if response.status_code == 200:

    ## converting the response string into JSON format
    res = response.json()
    ## storing the project names in our list project_names
    for i in range(len(res['value'])):
        project_names.append(res['value'][i]['name'])
    
    ## this is for the repositories under a project of an organization
    for project_name in project_names:

        # REST API for get the repositories under a project of an organization
        url = f"https://dev.azure.com/{organization}/{project_name}/_apis/git/repositories?api-version=7.2-preview.1"
        ## Getting the response by calling the REST API
        response = requests.get(url, headers=headers, auth=auth)

        # Checking if the response we got is valid
        if response.status_code == 200:

            # converting the response into JSON
            res = response.json()

            ## Storing the repositories name and (project_name,ids) for further uses
            for i in range(len(res['value'])):
                repository_names.append(res['value'][i]['name'])
                repository_ids.append((project_name, res['value'][i]['id']))
    ## finding the latest update on each of the repositories
    for idx,repo in enumerate(repository_ids):
        # project name
        project = repo[0]
        # repository id under that project
        repository_id = repo[1]
        # branch name (determines the latest update based on which branch)
        name = 'master'
        # REST API for get the latest changes to master branch
        url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository_id}/stats/branches?name={name}&api-version=7.2-preview.2"
        # Calling the API to get the response
        response = requests.get(url, headers=headers, auth=auth)
        # Checking if the response is valid
        if response.status_code == 200:
            # converting the response string data into JSON format
            res = response.json()

            # last changes commit ID
            commit_id = res['commit']['commitId']

            # Who made the latest changes
            committer_name = res['commit']['committer']['name']

            # At which date-time the changes were applied
            commit_date = pd.to_datetime(res['commit']['committer']['date'])

            # Comment for the last change
            comment = res['commit']['comment']

            # Latest change link
            commit_url = res['commit']['url']

            # creating a 1D array to place the data related to last change
            # project_name, repository_name, repository_id, then of it described before in this block
            data = [repo[0],
                    repository_names[idx],
                    repo[1],
                    commit_id,
                    committer_name,
                    commit_date,
                    comment,
                    commit_url]
            # Creating a new dataframe from the 1D array and column names are given by the predefined column in the beginning
            new_df = pd.DataFrame([data],columns=column_names)
            # Adding new dataframe to the main data frame which is declared in the beginning
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
        else:
            # if the response is not valid then we have another option to check if the 
            #default branch name is "main"
            name = 'main'
            # REST API to get the last change in the main branch
            response = requests.get(url, headers=headers, auth=auth)
            # check if the response is valid
            if response.status_code == 200:
                # same thing what we did for the name = "master"
                res = response.json()
                commit_id = res['commit']['commitId']
                committer_name = res['commit']['committer']['name']
                commit_date = pd.to_datetime(res['commit']['committer']['date'])
                comment = res['commit']['comment']
                commit_url = res['commit']['url']
                data = [repo[0],
                        repository_names[idx][repo[1]],
                        repo[1],
                        commit_id,
                        committer_name,
                        commit_date,
                        comment,
                        commit_url]
                new_df = pd.DataFrame([data], columns=column_names)
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
            else:
                # If there is an error
                print(f"Error: {response.status_code} - {response.text}")
    ## Sorting the data according to latest commit date
    df = df.sort_values(by="last_commit_date", ascending=False)
    ## storing the data into csv format which will be in your same directory where the 
    ## python file is present 
    df.to_csv('./ado_repo_list_by_commit_date.csv', index=False)
    print("Succesfully updated the csv file")
else:
    # If the is an error
    print(f"Error: {response.status_code} - {response.text}")           


        
