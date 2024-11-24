import requests

def get_tree_data_on_request(id):
    url = f'https://tumalas.kz/wp-admin/admin-ajax.php?action=tuma_cached_childnew_get&nodeid=14&id={id}'
    response = requests.get(url)
    return response.json()