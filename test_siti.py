import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Script per testare il web scraping su un sito specifico
url = ""

try:
    response = requests.get(url, headers=headers)
    
    # Se il sito non ci ha bloccato, response.status_code sarà 200 OK 
    # altrimenti ottieni un errore tipo 403 Forbidden (ha capito che si tratta di un bot) 
    # o 503 Service Unavailable (se il server è sovraccarico)
    print(f"Status Code: {response.status_code}") 

    # Parsing del contenuto HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Tag, {'classe/id': 'nome_classe/id'}
    price_tag = soup.find('div', {'class': 'price',})
    
    if price_tag:
        print(f"Prezzo: {price_tag.text.strip()}")
    else:
        print("Prezzo non trovato.")

except requests.RequestException as e:
    print(f"Errore durante la richiesta: {e}")
