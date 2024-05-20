import requests
import json
import os
import sys

api_base_url = os.environ.get('API_BASE_URL', '')
workflow_url = 'executions/'
auth_token = os.environ.get('AUTH_TOKEN', '')

if (len(api_base_url) == 0 or len(auth_token) == 0):
    sys.stderr.write(
'''FOR SECURITY REASSONS YOU MUST SET THE NEXT VARIABLES IN YOUR ENV:
    API_BASE_URL=<url>
    AUTH_TOKEN=cookie_to_authenticate
''')
    sys.exit(0)
'''
Returns a dictionary list. Iterates through all the action 
list and collects all the actions that failed.
The key is an index and the
value is a dictionary with the next format:
{
    id: string
    stderr: string
    exit_code: int
}  
'''
def get_error_list(auth_token):
    error_list = list()
    cookies={'auth-token': auth_token}
    url = f'{api_base_url}{workflow_url}'
    res = requests.get(url, cookies=cookies)
    if (res.status_code == 200):
        dict_data = json.loads(res.text)
        for item in dict_data:
            try:
                if (item['result']['exit_code'] != 0):
                    tmp_dict = {
                            'id': item['id'],
                            'stderr': item['result']['stderr'],
                            'exit_code': item['result']['exit_code']
                    }
                    error_list.append(tmp_dict)
            except:
                continue
    else:
        print(f'cookie: {cookies}')
        print(f'Failed to retrieve data from {url} wit error code: {res.status_code}')
    return error_list

if __name__ == '__main__':
    errors = get_error_list(auth_token)
    for error in errors:
        print(f'ID: {error.get("id", "Invalid ID")}')
        print('-'* 32)
        print(f'exit_code: {error.get("exit_code", "None")}')
        print('-'* 32)

