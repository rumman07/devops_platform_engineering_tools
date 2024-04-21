#!/bin/bash


python3 getProject_Repo_Name.py
## to use gei and ado2gh firstly you have to set
# environment variables

## manuall add er khetre terminal e kore nibo
export GH_PAT="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"
export ADO_PAT="c77kb35dygobrvqcxybqeyob7w24yetmlu2r6fj7omdkme63reja"

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
git_org="u19test"


## azure organization
azure_org="udemydevopscourse"

tail -n +2 "$projects" | while IFS=',' read -r project_name_space project_name repo_name repository_id; do
    repo_response=$(gh api -X GET "/repos/$git_org/$repo_name")
    not_found=$(echo "$repo_response" | jq -r '.message')
    if [ "$not_found" == "Not Found" ]; then
        echo "Not Found Error Means Here That The Repository Was Not Migrated Before"
        echo "Started Migrating"
        response=$(gh ado2gh migrate-repo --ado-org "$azure_org" --ado-team-project "$project_name_space" --ado-repo "$repo_name" --github-org "$git_org" --github-repo "$repo_name")
            # Check the exit status of the previous command
        if [ $?==0 ];then
            echo "Migration successful"
            echo "$response"
            status=$(curl -L -u "'':$ADO_PAT"\
             -X PATCH\
             -H "Content-Type: application/json" --write-out "%{http_code}\n" --silent --output /dev/null https://dev.azure.com/$azure_org/$project_name/_apis/git/repositories/$repository_id?api-\
             version=7.1-preview.1\
	     -d '{"isDisabled": true}')
	    if [ $status -eq 200 ];then
            	echo "Disabling $project_name_space was Successfull"
            else
            	echo "Disabling Azure Repo Failed"
            	# Log The Details to a csv file
            	echo ",$azure_org,$project_name_space,$repo_name,Operation Disable Failed" >> error_log.csv
            	continue
            fi   	
        else
            echo "Error: Migration failed"
            # Log the details to a CSV file
            echo ",$azure_org,$project_name_space,$repo_name,Migration failed" >> error_log.csv
            continue
        fi
    else 
        echo "Repo $repo_name from this project $project_name_space was migrated"
        continue
    fi
done 
