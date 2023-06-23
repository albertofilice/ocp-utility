import requests
import json
from getpass import getpass
from prompt_toolkit import prompt

# Definisci l'indirizzo di AWX
awx_host = prompt('Indirizzo AWX: ')

# Richiedi le credenziali di accesso all'API di AWX
awx_username = prompt('Username: ')
awx_password = getpass('Password: ')

# Effettua l'autenticazione e ottieni il token di accesso
auth_url = f"{awx_host}/api/v2/tokens/"
auth_data = {
    'username': awx_username,
    'password': awx_password
}
auth_response = requests.post(auth_url, auth=(awx_username, awx_password))
auth_response.raise_for_status()
auth_token = auth_response.json()['token']

# Definisci i dettagli del progetto
project_name = prompt('Nome del progetto: ')
project_description = prompt('Descrizione del progetto: ')
project_organization = prompt('Organizzazione del progetto: ')

# Richiedi i parametri di configurazione GIT
git_url = prompt('URL del repository GIT: ')
git_username = prompt('Username GIT: ')
git_password = getpass('Password GIT: ')

# Crea le credenziali di accesso Source Control
credentials_url = f"{awx_host}/api/v2/credentials/"
headers = {
    'Authorization': f"Bearer {auth_token}",
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
credentials_data = {
    'name': f"Credenziali Source Control - {project_name}",
    'description': f"Credenziali di accesso al repository GIT per il progetto {project_name}",
    'organization': project_organization,
    'credential_type': 2,  # Tipo di credenziali Source Control
    'inputs': {
        'username': git_username,
        'password': git_password
    }
}

print(json.dumps(credentials_data, indent=4))

create_credentials_response = requests.post(credentials_url, headers=headers, auth=(awx_username, awx_password), json=credentials_data)
create_credentials_response.raise_for_status()
credentials_id = create_credentials_response.json()['id']

# Crea il progetto
projects_url = f"{awx_host}/api/v2/projects/"
project_data = {
    'name': project_name,
    'description': project_description,
    'organization': project_organization,
    'scm_type': 'git',
    'scm_url': git_url,
    'scm_credential': credentials_id
}
create_project_response = requests.post(projects_url, headers=headers, auth=(awx_username, awx_password), json=project_data)
create_project_response.raise_for_status()

# Stampa la risposta del server
print(f"Progetto '{project_name}' creato con successo!")
print(json.dumps(create_project_response.json(), indent=4))
