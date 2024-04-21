import pandas as pd
import os 
import requests 
import logging 
import matplotlib.pyplot as plt
## get the current directory
c_dir = os.path.dirname(os.path.realpath(__file__))

## ensuring if the error.log file exists or not
if not os.path.exists(f'{c_dir}/error.log'):
    with open(f'{c_dir}/error.log', 'w'):
        pass

## configure logging file
logging.basicConfig(filename=f'{c_dir}/error.log',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')

def getAuth(ado_pat) :
    ## header config
    headers = {"Content-Type": "application/json"}
    ## for Basic Auth
    auth = ('', ado_pat)
    return (headers,auth)

def getProjects(organization_name,headers,auth) :
    ## REST API url to get all of the project in that specific organization
    url = f"https://dev.azure.com/{organization_name}/_apis/projects?api-version=7.1-preview.4"
    try :
        response = requests.get(url, headers=headers, auth=auth)
        results = response.json()
        if response.status_code!=200 and "NotFound" in results['typeName'] :
            error_msg = f'Error occurred while fetching projects : {organization_name}'
            print(error_msg)
            logging.error(error_msg)
            return []
        
        project_names = []
        ## storing the project names in our list project_names
        for i in range(len(results['value'])) :
            project_names.append(results['value'][i]['name'])
        return project_names
    except requests.exceptions.RequestException as e :
        error_msg = f'Error occurred while fetching projects : {e}'
        print(error_msg)
        logging.error(error_msg)
def getLanguagesOnEachProject(organization_name,projects,headers,auth) :
    try :
        df = pd.DataFrame()
        for project_name in projects :
            url =f'https://dev.azure.com/{organization_name}/{project_name}/_apis/projectanalysis/languagemetrics' 
            response = requests.get(url, headers=headers, auth=auth)
            results = response.json()
            for repo_hist in results['repositoryLanguageAnalytics'] :
                languages=[]
                repo_name = repo_hist['name']
                for lang in repo_hist['languageBreakdown'] :
                    lang_name = lang['name']
                    if lang_name == 'Unknown' :
                        continue
                    languages.append(lang_name)
                languages =','.join(languages)
                n_df  = pd.DataFrame(data=[[project_name,repo_name,languages]],columns=['project_name','repo_name','languages'])
                df = pd.concat([df,n_df],axis=0,ignore_index=True)
        return df
    except requests.exceptions.RequestException as e :
        error_msg = f'Error occurred while fetching language details : {e}'
        print(error_msg)
        logging.error(error_msg)
if __name__ == "__main__":
    ado_pat = os.environ.get("ADO_PAT")
    organization_name = "udemydevopscourse" 
    # get the authentication and headers 
    headers,auth = getAuth(ado_pat=ado_pat)
    # getting the project names
    project_names = getProjects(organization_name,headers,auth)
    df = getLanguagesOnEachProject(organization_name,project_names,headers,auth)
    df.to_csv(f'{c_dir}/languageStatusAzure.csv',index=False)