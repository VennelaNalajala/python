import configparser
import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from load import load



config = configparser.ConfigParser()
config.read('config.ini')

username = config['sharepoint']['username']
password = config['sharepoint']['password']
site_url = config['sharepoint']['site_url']
list_name = config['sharepoint']['list_name']


ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
target_list = ctx.web.lists.get_by_title(list_name)


items = target_list.items.select(
    ['Title', 'Status', 'Project_x0020_Manager', 'Start_x0020_Date', 'End_x0020_Date', 'Budget', 'Department']
).get().execute_query()


data = []
for item in items:
    data.append({
        'project_name': item.properties.get('Title'),
        'status': item.properties.get('Status'),
        'project_manager': item.properties.get('Project_x0020_Manager'),
        'start_date': item.properties.get('Start_x0020_Date'),
        'end_date': item.properties.get('End_x0020_Date'),
        'budget': item.properties.get('Budget'),
        'department': item.properties.get('Department'),
    })

df = pd.DataFrame(data)
print("Fetched SharePoint Data:")
print(df)
load(df)


