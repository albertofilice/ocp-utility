import os
import sys
import requests
from datetime import datetime, timedelta
from getpass import getpass
from prompt_toolkit import prompt

# Definisci l'indirizzo di AWX
tower_url = prompt('Indirizzo AWX: ')

# Richiedi le credenziali di accesso all'API di AWX
tower_username = prompt('Username: ')
tower_password = getpass('Password: ')

# Calcola la data limite (un giorno fa)
limit_date = datetime.now() - timedelta(days=1)
formatted_limit_date = limit_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# URL dell'API per ottenere i job completati
api_url = f"{tower_url}/api/v2/jobs/?format=json&page_size=200"

# Effettua la richiesta GET all'API di Ansible Tower per ottenere la prima pagina dei risultati
response = requests.get(api_url, auth=(tower_username, tower_password))

# Controlla lo status della risposta
if response.status_code == 200:
    # Ottieni il numero totale di pagine dei risultati
    total_pages = response.json()["count"] // 100 + 1

    # Scansiona tutte le pagine dei risultati
    for page in range(1, total_pages + 1):
        # Aggiungi il parametro 'page' all'URL dell'API per ottenere la pagina corrente
        page_url = f"{api_url}&page={page}"

        # Effettua la richiesta GET per la pagina corrente
        page_response = requests.get(page_url, auth=(tower_username, tower_password))

        # Controlla lo status della risposta
        if page_response.status_code == 200:
            # Ottieni i job completati dalla pagina corrente
            jobs = page_response.json()["results"]

            # Elimina i job uno per uno
            for job in jobs:
                job_id = job["id"]
                finished_date = job["finished"]

                if finished_date < formatted_limit_date:
                    delete_url = f"{tower_url}/api/v2/jobs/{job_id}/"
                    delete_response = requests.delete(delete_url, auth=(tower_username, tower_password))

                    if delete_response.status_code == 204:
                        print(f"Eliminato job con ID {job_id}")
                    else:
                        print(f"Errore durante l'eliminazione del job con ID {job_id}")
                else:
                    print(f"Ignorato job con ID {job_id}: non soddisfa il criterio di data limite")
        else:
            print(f"Errore durante l'ottenimento dei job completati dalla pagina {page}.")
else:
    print("Errore durante l'ottenimento dei job completati da Ansible Tower.")