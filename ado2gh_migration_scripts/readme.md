
# Migrating From Azure To GitHub

A custom script to migrate repository from ADO to Github. First we have a csv of the ADO repositories from the ADO organization projects sorted by last commit date. From that list we have migrated those repositories in two methods assigning team in github and without assigning team and if any error occurs we can find the repositories along with their project name. We have used ado2gh to single repo migration from azure to github. ADO2GH is a github cli extension.




## Installation Prerequisite

Install GitHub CLI (for linux)

```bash
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```
Install GitHub CLI extension (for linux)
```bash
gh extension install github/gh-ado2gh
```

## Environment Variables

To run this script you will need to add some environment variables (here shown for linux).

`Set Environment Variables by running below commands`

`export GH_PAT="your_github_personal_access_token(must be classic one)"`

`export ADO_PAT="your_azure_personal_access_token"`

After Setting environment variables you should authenticate with your github account by using below  command.

```bash
   gh auth login
```
# Running Script
First Unzip the folder called "MigrationWithAssigningTeam". Make sure you have created a file named "error_log.csv". Then open the terminal within this folder. Change the permission for the "migrationWithAssigningTeam.sh" script.
```bash 
chmod +x ./migrateWithAssinginTeam.sh
```
now run the script by below command.
```bash
    ./migrateWithAssigningTeam.sh
```


