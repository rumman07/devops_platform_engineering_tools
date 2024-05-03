import pandas as pd 

df = pd.read_csv('./azure_repo_list[updated].csv')
project_names = list(df['project_name'])
for i in range(len(project_names)):
  project_names[i] = project_names[i].replace(' ','%20')
data = {
    'project_name_space':df['project_name'].to_numpy(),
    'project_name' :project_names,
    "repo_name" : df['repository_name'].to_numpy(),
    "repository_id":df['repository_id'].to_numpy(),
 }
print("Getting Data From Latest Commit Info CSV")
n_df = pd.DataFrame(data)

n_df.to_csv('./latestCommitInfoProjectRepoNames.csv',index=False)
print("Data Extracting Successfull....\n")
print(n_df,end="\n\n\n\n")
