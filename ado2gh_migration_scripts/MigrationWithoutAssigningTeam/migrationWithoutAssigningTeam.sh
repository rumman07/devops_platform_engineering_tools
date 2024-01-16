#!/bin/bash


python3 getProject_Repo_Name.py
## to use gei and ado2gh firstly you have to set
# environment variables

## manuall add er khetre terminal e kore nibo
export GH_PAT=""
export ADO_PAT=""

## connect with your github account
gh auth login 

## read the csv generated by upper script 
## create team in github organization 
## privacy "secret"

# Your CSV file name
projects="latestCommitInfoProjectRepoNames.csv"

# Check if the file exists
if [ ! -f "$projects" ]; then
    echo "File $projects not found."
    exit 1
fi

## github organization name
git_org="ur9-0"


## azure organization
azure_org="udemydevopscourse"

tail -n +2 "$projects" | while IFS=',' read -r project_name repo_name; do
    repo_response=$(gh api -X GET "/repos/$git_org/$repo_name")
    not_found=$(echo "$repo_response" | jq -r '.message')
    if [ "$not_found" == "Not Found" ]; then
        echo "Not Found Error Means Here That The Repository Was Not Migrated Before"
        echo "Started Migrating"
        response=$(gh ado2gh migrate-repo --ado-org "$azure_org" --ado-team-project "$project_name" --ado-repo "$repo_name" --github-org "$git_org" --github-repo "$repo_name")
            # Check the exit status of the previous command
        if [ $? -eq 0 ]; then
            echo "Migration successful"
            echo "$response"
        else
            echo "Error: Migration failed"
            # Log the details to a CSV file
            echo "$azure_org,$project_name,$repo_name,Migration failed" >> error_log.csv
            continue
        fi
    else 
        echo "Repo $repo_name from this project $project_name was migrated"
        continue
    fi
done 
