#!/bin/sh



# distribution list for sending mail
MAILUSERS='ahmedabir.rez@gmail.com u1904117@student.cuet.ac.bd'

# current directory
c_dir="$PWD"

## Getting the Data We Need To Process Further
python3 get-data.py

## Now two files will be generated repos.txt and team_users.txt

# month has to be in this format 
MONTH='2025-01'

## Auditing Based on Team name and User Under the team and also in the filtered list of 
## repositories by Custom_Properties Audit Field

## an array to store all csv
declare -a csv_files


while IFS='=' read -r TEAM_NAME USERNAMES; do
    # Remove leading/trailing whitespace from USERNAME
    USERNAMES=$(echo "$USERNAMES" | xargs)
    # Call the Python script for auditing with TEAM_NAME and USERNAME as arguments
    python3 monthly-audit.py "$USERNAMES" "$MONTH" "$TEAM_NAME"

    # Check if the Python script was successful and file exists
    if [ $? -eq 0 ]; then
        csv_file="${c_dir}/${TEAM_NAME}-${MONTH}-audit.csv"
        if [ -f "$csv_file" ]; then
            csv_files+=("$csv_file")
        fi
    fi
done < team_users.txt


# After processing all teams, send one email with all CSVs
if [ ${#csv_files[@]} -gt 0 ]; then
    # Build the mailx command with multiple -a options
    attachments=""
    for csv in "${csv_files[@]}"; do
        attachments="$attachments -a $csv"
    done
    
    # Send email with all attachments
    echo "Monthly Audit Report For Each Team" | mailx -s "Monthly Audit Report For Each Team" $attachments "$MAILUSERS"
    if [ $? -eq 0 ]; then
        echo "Success: Email sent with all audit reports"
    else
        echo "Error: Failed to send email"
    fi
else
    echo "Error: No CSV files generated"
fi