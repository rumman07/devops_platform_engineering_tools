import pandas as pd 

df = pd.read_csv('latestCommitInfo.csv')
data = {
    'project_name' : df['project_name'].to_numpy(),
    "repo_name" : df['repository_name'].to_numpy(),
    "repository_id":df['repository_id'].to_numpy(),
 }
print("Getting Data From Latest Commit Info CSV")
n_df = pd.DataFrame(data)

n_df.to_csv('./latestCommitInfoProjectRepoNames.csv',index=False)
print("Data Extracting Successfull....\n")
print(n_df,end="\n\n\n\n")
