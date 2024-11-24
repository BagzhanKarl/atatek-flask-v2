import requests

def get_tree_data_on_request(id):
    url = f'https://tumalas.kz/wp-admin/admin-ajax.php?action=tuma_cached_childnew_get&nodeid=14&id={id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(url, headers=headers)
    return response.json()