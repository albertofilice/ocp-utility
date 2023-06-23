import requests
from prompt_toolkit import prompt
import json
from getpass import getpass

# Definisci l'indirizzo di AWX
awx_host = prompt('Indirizzo AWX: ')

# Richiedi le credenziali di accesso all'API di AWX
awx_username = prompt('Username: ')
awx_password = getpass('Password: ')

# Effettua l'autenticazione e ottieni il token di accesso
auth_url = f"{awx_host}/api/v2/tokens/"
auth_response = requests.post(auth_url, auth=(awx_username, awx_password))
auth_response.raise_for_status()
auth_token = auth_response.json()['token']

# Ottieni la lista dei tipi di credenziali
credential_types_url = f"{awx_host}/api/v2/credential_types/"
headers = {
    'Authorization': f"Bearer {auth_token}",
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
credential_types_response = requests.get(credential_types_url, headers=headers)
credential_types_response.raise_for_status()
credential_types = credential_types_response.json()

# Stampa la lista dei tipi di credenziali
for credential_type in credential_types['results']:
    print(f"ID: {credential_type['id']}, Nome: {credential_type['name']}")
