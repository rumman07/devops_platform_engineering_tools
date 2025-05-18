# Github Commit audit by Month Range

## Step-1 Create necessary directories 

After pulling this branch, create two folders, inside `audits` and `logs/error`, in the current directory `gh-commit-audit-docker` using the following command:

```bash
mkdir -p ./audits ./logs/error
```
## Step-2 Provide `ORG_NAME` and `TEAM_ID`

Give your `ORG_NAME` and `TEAM_ID` inside the **audit-gen.sh** script.

```bash
ORG_NAME=<your-org-name>
TEAM_ID=<your-team-id>
```
## Step-3 Time Range Configuration

Configure the audit period on the `audit-gen.sh` script using one of these methods:

### **Option 1: Duration-based**

```bash
is_period=1      // Enable duration mode
MONTH_START="YYYY-MM"  // Starting month (e.g., "2025-01")
MONTH_END="YYYY-MM" // optional
PERIOD=2         // Number of months to audit
```
### **Option 2: Range-based**

```bash
is_period=0      // Enable range mode
MONTH_START="YYYY-MM"  // First month to audit (e.g., "2025-01")
MONTH_END="YYYY-MM"    // Last month to audit (e.g., "2025-03")
PERIOD=2 // optional
```
## Step-4 Building Docker Image

```bash
docker build -t gh-audit .
```
## Step-5 Run Docker Container 

Use this command to run the container, which will execute the scripts, generate the outputs, and then automatically stop the container.

```bash
docker run -e GH_PAT=<github-personal-access-token> \
-v $(pwd)/audits:/app/audits \
-v $(pwd)/logs:/app/logs \
gh-audit
```

## Step-6 Debuging

After the `container` stops **successfully**, verify the `audits` folder for generated audit files. If the folder is empty or the unexpected things are noticed, review the `logs` folder and `logs/error/` folder for details.

**Note**: In the current directory you must have these folders `audits` and `logs/error/`.