# Github Organization Repository Monthly Audit By Commits of Repository Members or Contributors

First of all download the files in this folder to you desired folder in your pc or server. Also setup the `mailx` for sending mail to distribution lists.

## Step-1 Download all the necessary required packages

```bash
pip3 install -r requirements.txt
```

## Step-2 Get your github personal access token

Get your github personal access token and make sure you have placed the token into the script file `audit-gen-with-mailing.sh` at the specified place.

## Step-3 Add the emails to sent audit information

Place the `emails` separated by space into the `MAILUSERS` variable in the script `audit-gen-with-mailing.sh`

## Step-4 Add the usernames

Place the `usernames` separated by space into the `USERNAMES` variable in the script `audit-gen-with-mailing.sh`

## Step-5 Give the desired month

Give the month you want to extract the audit. But it has to be in this format `YYYY-MM`. Example `2025-01`.


## Step-6 Populate `repos.txt` file

populate with the github `repository` **links** in the corresponding file `repos.txt`.

## Step-7 Give Execute permission to `audit-gen-with-mailing.sh` script

```bash
chmod +x ./audit-gen-with-mailing.sh
```
## Step-8 Execute the script

```bash
./audit-gen-with-mailing.sh
```

After a successful execution you will notice a `monthly-audit.csv` file in the current directory which will be sent over email to the distributions.

**Note:** For demonstration I have used the `freeCodeCamp` organization to test my script. And for emailing I have configured `mailx` with **smtp.gmail.com**.