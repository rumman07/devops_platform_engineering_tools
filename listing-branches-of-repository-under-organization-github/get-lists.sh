

export GH_PAT="github-access-token-goes-here"
export ORG_NAME="organization-name-goes-here"

# first execute this script
python3 -u ./list-all-repositories.py

# then execute this
python3 -u ./list-all-branches.py