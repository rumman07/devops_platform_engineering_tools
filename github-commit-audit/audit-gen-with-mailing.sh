#!/bin/sh

# distribution list for sending mail
MAILUSERS='ahmedabir.rez@gmail.com u1904117@student.cuet.ac.bd'

# github usernames for auditing
USERNAMES='camperbot raisedadead sahat valenzsa'

# month has to be in this format 
MONTH='2025-01'

python3 monthly-audit.py "$USERNAMES" "$MONTH"

if [ $? -eq 0 ]; then
    echo "Success"
    echo "Monthly Audit Report" | mailx -s "Monthly Audit Report" -a $PWD/monthly_audit.csv $MAILUSERS
fi