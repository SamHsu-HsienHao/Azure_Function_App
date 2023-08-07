import requests

login_url = "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/oauth2/v2.0/token"
login_headers = {"Content-Type": "application/x-www-form-urlencoded"}
login_params = {"client_id":"f8d3ae81-a383-4744-ab8d-42452dc10cda",
          "grant_type":"client_credentials",
          "scope":"https://vault.azure.net/.default",
          "client_secret":"Y3E8Q~o9UI4cNbtrKSUKkIrV8quxOpIqEGujia8Y"}

aad_response = requests.post(login_url, headers=login_headers, data=login_params)

aad_token=aad_response.json()['access_token']
kv_url = "https://samhsukv.vault.azure.net/secrets/adb-accessToken/?api-version=7.4"
kv_headers = {"Authorization": f"Bearer {aad_token}",
           "Content-Type": "application/json"}

kv_response = requests.get(kv_url, headers=kv_headers)

adb_pat=kv_response.json()['value']
workspace_url="https://adb-1520547678772531.11.azuredatabricks.net"
adb_url = f"{workspace_url}/api/2.0/token/create"
adb_headers = {"Authorization": f"Bearer {adb_pat}"}
adb_params = {"lifetime_seconds": "2592000","comment": "create_by_API"}

adb_response = requests.post(adb_url, headers=adb_headers, json=adb_params)

new_adb_access_token = adb_response.json()["token_value"]
update_kv_params = {"value": new_adb_access_token}

update_kv_response = requests.put(kv_url, headers=kv_headers, json=update_kv_params)
update_kv_response.json()