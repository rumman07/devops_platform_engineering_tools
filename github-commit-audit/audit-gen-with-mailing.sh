#!/bin/sh

# distribution list for sending mail
MAILUSERS='ahmedabir.rez@gmail.com u1904117@student.cuet.ac.bd'

ORG_NAME="your-org-name"
TEAM_ID="your-team-id"
## Getting the Data We Need To Process Further
python3 get-data.py "$ORG_NAME" "$TEAM_ID"

## Now two files will be generated repos.txt and team_users.txt

# month has to be in this format 
MONTH='2025-01'

## Auditing Based on Team name and User Under the team and also in the filtered list of 
## repositories by Custom_Properties Audit Field

while IFS='=' read -r TEAM_NAME USERNAMES; do
    # Remove leading/trailing whitespace from USERNAME
    USERNAMES=$(echo "$USERNAMES" | xargs)
    # Call the Python script for auditing with USERNAMES, MONTH, TEAM_NAME as arguments
    python3 monthly-audit.py "$USERNAMES" "$MONTH" "$TEAM_NAME"

    if [ $? -eq 0 ]; then
    echo "Successfully"
    echo "Monthly Audit Report Team $TEAM_NAME" | mailx -s "Team - $TEAM_NAME Monthly Audit Report" -a $PWD/$TEAM_NAME-$MONTH-audit.csv $MAILUSERS
    fi
done < team_users.txt


