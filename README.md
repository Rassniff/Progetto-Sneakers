# Price Tracker: Monitoraggio Prezzi di Sneaker tramite Web Scraping e Notifica Email

Uno script Python per il monitoraggio dei prezzi di sneaker, sviluppato come progetto per l'esame di Reti di Calcolatori.

Questo script analizza (fa *scraping*) un elenco di siti di e-commerce per un articolo specifico, estrae i prezzi e invia un report riepilogativo in formato HTML via email.

-----

## Obiettivi del Progetto

L'obiettivo era quello di implementare un client di rete in grado di:

  * Interagire con server web multipli tramite il protocollo **HTTP** per scaricare contenuti.
  * Effettuare il **parsing** di payload applicativi complessi (l'HTML dei siti) per estrarre informazioni specifiche.
  * Gestire le diverse strutture dati e le contromisure anti-bot di base.
  * Implementare un client **SMTP** per inviare una notifica formattata via email.

-----

## Tecnologie Utilizzate

  * **Python 3.11+**
  * **`requests`**: Per l'invio di richieste HTTP GET e la gestione degli header (es. `User-Agent`).
  * **`beautifulsoup4`**: Per il parsing del DOM HTML e la ricerca dei selettori di prezzo.
  * **`smtplib`** e **`email.message`**: (Librerie standard di Python) Per la creazione e l'invio di email in formato `text/html` tramite un server SMTP (es. Gmail).

-----

## Come Eseguirlo

### 1\. Prerequisiti

  * Python 3.10 o superiore.
  * Un account email (es. Gmail) con una **"Password per le app"** generata.

### 2\. Installazione

1.  Clona questo repository:

    ```bash
    git clone https://github.com/TUO-NOME-UTENTE/TUO-REPO.git
    cd TUO-REPO
    ```

2.  Crea e attiva un ambiente virtuale (consigliato):

    ```bash
    # Su Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Su Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  Installa le librerie necessarie:

    ```bash
    pip install requests beautifulsoup4
    ```

### 3\. Configurazione

Apri il file `main.py` e modifica le seguenti costanti nella parte superiore del file:

```python
# --- Configurazione (Tutto in cima) ---
EMAIL_SENDER = "latuaemail@gmail.com"
EMAIL_PASSWORD = "la_tua_password_app_di_16_lettere" # <-- INSERISCI QUI LA PASSWORD PER LE APP
EMAIL_RECEIVER = "email.destinatario@esempio.com"

# Finge di essere un browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 ...'
}

# Modifica questa lista con i siti da analizzare
SITI_DA_CONTROLLARE = [
    {
        'nome': 'Nome Sito 1',
        'url': '...',
        'selettore_prezzo': ('span', {'class_': 'prezzo'})
    },
    # ...
]
```

### 4\. Esecuzione

Una volta configurato, esegui semplicemente lo script:

```bash
python main.py
```

Lo script stamperà i progressi sul terminale e invierà l'email al termine.

-----
