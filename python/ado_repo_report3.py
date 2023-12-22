# to handle the request and response from the REST API
import requests
# structuring the data and filtering on it
import pandas as pd
## personal access token
PATS = ""
## organization name
organization = ""

## REST API url to get all of the project in that specific organization
url = f"https://dev.azure.com/{organization}/_apis/projects?api-version=7.1-preview.4"
## header config
headers = {"Content-Type": "application/json"}
## for Basic Auth
auth = ('', PATS)

## all of the project names will be here in this list
project_names = []

## all of the repositories names will be here in this list
repository_names = []

## all of the repositories ids will be here in this list
repository_ids = []

## column names in our csv file to make it more readable and understandable
column_names = ['project_name','repository_name','branch_name','repository_id','last_commit_id','committer_name','last_commit_date','comment','last_commit_link']

## creating a blank data frame to store data in an organized way
df = pd.DataFrame()

## to store the repository id which have issues with extracting the latest changes from "main" or "master"  branch
err_df = pd.DataFrame()
## requesting to the REST API and get the response
response = requests.get(url, headers=headers, auth=auth)

## checking if the response is OK or NOT
if response.status_code == 200 :

  ## converting the response string into JSON format
  res = response.json()
  ## storing the project names in our list project_names
  for i in range(len(res['value'])) :
    project_names.append(res['value'][i]['name'])

  ## this is for the repositories under a project of an organization
  for project_name in project_names :

      # REST API   for get the repositories under a project of an organization
      url = f"https://dev.azure.com/{organization}/{project_name}/_apis/git/repositories?api-version=7.2-preview.1"

      ## getting the response by calling the REST API
      response = requests.get(url,headers=headers,auth=auth)

      # checking if the response we get is it OK or NOT
      if response.status_code == 200 :

         # converting the response into JSON
         res = response.json()

         ## storing the repositories name and (project_name,ids) for further uses
         for i in range(len(res['value'])):
             repository_names.append(res['value'][i]['name'])
             repository_ids.append((project_name,res['value'][i]['id']))

  ## finding the latest update on each of the repositories
  for idx,repo in enumerate(repository_ids) :
    # project name
    project = repo[0]
    # repository id under that project
    repositoryId = repo[1]
    # branch name (determines the latest update based on which branch)
    name = "master"
    # REST API for get the latest changes to master branch
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/stats/branches?name={name}&api-version=7.2-preview.2"
    # calling the API to get the response
    response = requests.get(url,headers=headers,auth=auth)
    # checking if the response is OK or NOT
    if response.status_code == 200 :
      # converting the response string data into JSON format
      res = response.json()

      # last changes commit ID
      commitId = res['commit']['commitId']

      # who have make the changes to the last change
      committerName = res['commit']['committer']['name']

      # at which date-time the changes are applied
      commitDate = pd.to_datetime(res['commit']['committer']['date'])

      # comment for the last change
      comment = res['commit']['comment']

      # last change link
      commitURL = res['commit']['url']

      # creating a 1D array to place the data related to last change
      # project_name, repository_name, repository_id, then of it described before in this block
      data = [repo[0],repository_names[idx],name,repo[1],commitId,committerName,commitDate,comment,commitURL]
      # creating a new dataframe from the 1D array and column names are given by the predefined column in the beginning
      new_df = pd.DataFrame([data],columns=column_names)
      # adding new dataframe to the main data frame which is declared in the beginning
      df = pd.concat([df, new_df], axis=0, ignore_index=True)
    else :
      # if the response is not ok then we have another option to check if the default branch name is "main"
      name = "main"
      # REST API to get the last change in the main branch
      url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/stats/branches?name={name}&api-version=7.2-preview.2"
      # calling the REST API
      response = requests.get(url,headers=headers,auth=auth)
      # check if the response is OK or NOT
      if response.status_code == 200:
        # same thing what we do for the name="master"
        res = response.json()
        commitId = res['commit']['commitId']
        authorName = res['commit']['committer']['name']
        commitDate = pd.to_datetime(res['commit']['committer']['date'])
        comment = res['commit']['comment']
        commitURL = res['commit']['url']
        data = [repo[0],repository_names[idx],name,repo[1],commitId, authorName,commitDate,comment,commitURL]
        new_df = pd.DataFrame([data],columns=column_names)
        df = pd.concat([df, new_df], axis=0, ignore_index=True)
      else :
        columns = ['project_name','repositoryId']
        data = [project,repositoryId]
        new_df = pd.DataFrame([data],columns=columns)
        # store it to err_dataframe
        err_df = pd.concat([err_df, new_df], axis=0, ignore_index=True)
        # if any error occurs
        print(f"Error: {response.status_code} - {response.text}")
  ## sorting the data according to latest change
  df = df.sort_values(by="last_commit_date",ascending=False)
  ## storing the data into csv format which will be in your same directory where the python file is present
  df.to_csv('./latestCommitInfo.csv',index=False)
  err_df.to_csv('./errorToFindRepoBranches.csv',index=False)
  print("Successfully Updated The CSV's")
else :
  # if any error occurs
  print(f"Error: {response.status_code} - {response.text}")