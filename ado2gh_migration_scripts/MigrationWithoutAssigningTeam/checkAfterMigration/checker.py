import pandas as pd 
import os 

c_dir = os.path.dirname(os.path.realpath(__file__))
## dependencies on the GetOrganizationRepositoriesFromGithub
path = f'{c_dir}/orgRepositories.csv'
migrated_df = pd.read_csv(path)
migrated_df['full_name'] = migrated_df['full_name'].str.split('/').str[1]
## dependencies on the migrationOfAzureReposToGithub
path = f'{'/'.join(os.path.dirname(__file__).split('/')[0:-1])}/latestCommitInfoProjectRepoNames.csv'
hasto_migrate = pd.read_csv(path)
hasto_migrate['repo_name'] = hasto_migrate['repo_name'].str.replace(' ','-')
c_dir = os.path.dirname(os.path.realpath(__file__))

error_df = pd.DataFrame()

# Merge the dataframes on repo_name, indicator=True to identify the source of each row
merged = pd.merge(migrated_df, hasto_migrate, left_on='full_name', right_on='repo_name', how='outer', indicator=True)
# Filter the rows where the indicator column is 'right_only' (only present in hasto_migrate)
result = merged[merged['_merge'] == 'right_only']
result.drop(columns=['id', 'full_name', 'isPrivate', 'git_url','clone_url','_merge'],inplace=True)
result.to_csv(f'{c_dir}/migrationFailedToTheseRepositories.csv',index=False)
