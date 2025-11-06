import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import time 

# Configurazione email
EMAIL_SENDER = "" #inserisci la tua email qui
EMAIL_PASSWORD = "" #inserisci la tua password per l'app qui
EMAIL_RECEIVER = "" #inserisci la email del destinatario qui

# Setup dell'header per imitare un browser reale
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# La lista dei siti che ho validato
SITI_DA_CONTROLLARE = [
    {
        'nome': 'NOIRFONCE',#nome sito
        'url': 'https://noirfonce.eu/it-it/products/new-balance-1906-m1906dh?_pos=3&_fid=88fcfaa81&_ss=c',#url sito
        'selettore_prezzo': ('span', {'class': 'money'})# (TAG, {ATTRIBUTO: 'VALORE'})
    },
    {
        'nome': 'STIMM',
        'url': 'https://stimm.com/products/new-balance-sneakers-m1906-silver-metallic?variant=46983325450585&utm_source=google&utm_medium=cpc&utm_campaign=PerformanceMax+cross-network&gad_source=1&gad_campaignid=15418731971&gbraid=0AAAAADh8ReuXPhahvs4nRurERZ7g7LgWp&gclid=Cj0KCQjw35bIBhDqARIsAGjd-cYytp9rf3Wtd6poKKWWr7EE34L67Fvg9qsFpobT2HuzLqyDrOj45j0aAoalEALw_wcB',
        'selettore_prezzo': ('div', {'class': 'text-xl flex gap-2 items-center',})

    },
    {
        'nome': 'CLOTHIFY-IT',
        'url': 'https://clothify-it.com/products/new-balance-1906d-protection-pack-silver-metallic?variant=48034639446360',
        'selettore_prezzo': ('span', {'class': 'yv-product-price h2',})
    },
    {
        'nome': 'SANT KICKS',
        'url': 'https://santkicks.com/en/products/new-balance-1906-m1906dh?variant=44407441621131&country=US&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOoqNwAzgzaZHB-NJaawk5AzbpKx7FbqirimfbqJp5sTlun-hqjc6vc0',
        'selettore_prezzo': ('span', {'class': 'price',})
    },
    {
        'nome': 'LACED.',
        'url': 'https://www.laced.com/products/new-balance-1906d-protection-pack-silver-metallic?eu_size=44.5&preferred_currency=EUR&preferred_location=IT&size_system=EU&uk_size=10&us_size=10.5&srsltid=AfmBOopStADbljnFmD3BuU2XfFzmkkGUtMXoOKuj6pfksCGzuZlAgK3Hif0',
        'selettore_prezzo': ('h2', {'class': 'e1kigzca5 css-7nzvi2',})
    },
    {
        'nome': 'MISTER RESELLER',
        'url': 'https://mistereseller.com/products/new-balance-1906d-white-protection-pack?variant=46979148480848&country=IT&currency=EUR&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&srsltid=AfmBOoqvXFtRU4ltTyXHlP-2x3H0mdZ8PdxgyRvmNpFlVaJPv2h-i58mCwI',
        'selettore_prezzo': ('span', {'class': 'sale-price',})
    },
    {
        'nome': 'TRYME SHOP',
        'url': 'https://www.trymeshop.com/products/new-balance-sneakers-retro-running-1906r-argento?variant=47244773228889&cmp_id=18385934636&adg_id=&kwd=&device=c&gad_source=1&gad_campaignid=18383100367&gbraid=0AAAAADjsqK28RHPFZ9A7FX3t3kBu-kl1Y&gclid=Cj0KCQjw35bIBhDqARIsAGjd-cYmMHs0ZjN7Fmf9BJgXpbeEmbhDjx8eEqjIfaT7bwcTHnsHkqVhb8EaAiIJEALw_wcB',
        'selettore_prezzo': ('span', {'class': 'money',})
    },
    {
        'nome': 'SNEAKER ASK',
        'url': 'https://sneakerask.com/it/products/1906d-protection-pack-silver-metallic?variant=48562654150991&gad_source=1&gad_campaignid=23149729340&gbraid=0AAAAA90L4c10jmmaOz6FQD6SCNUuolNWS&gclid=Cj0KCQjw35bIBhDqARIsAGjd-cZe2YQp79tGOahA6P9Jjw9HIt5YeNYHbTS3D1xTTiG4VAV-SW0HG_IaAqQaEALw_wcB',
        'selettore_prezzo': ('sale-price', {'class': 'text-lg',})
    },
    {
        'nome': 'LYST',
        'url': 'https://www.lyst.com/it-it/calzature/new-balance-sneakers-1906d-protection-pack-5/?product=LCADXRL&link_id=1007605838&_country=IT&size=9.5&show_express_checkout=true&atc_medium=cpc&atc_content=IT-PLA-New%2BBalance%2BSneakers-Clothing%2B%2526%2BAccessories%2B%253E%2BShoes%2B%253E%2BTrainers-CSS%2BVacherin-no&atc_country=IT&atc_source=google&atc_grouping=Google-PLA-EXPRESS&atc_campaign=IT-PLA-EXPRESS&atc_type=pla&atc_click_boost=0_click&sem_id=A8572548540&gad_source=1&gad_campaignid=22129125254&gbraid=0AAAAABqIjfx7GNwcDc09NHfAANnZu3B0Q&gclid=Cj0KCQjw35bIBhDqARIsAGjd-cZ8QyY1BdGOzkJVtGaf0OzygabfUMivZ1aHljYFYVI9iRpgEmUgEY4aAhxKEALw_wcB&paid_session_id=92db0c44-a007-40d3-9dba-d8bc3c67b53c',
        'selettore_prezzo': ('div', {'class': '_1b08vvhrq vjlibs2',})
    },
    {
        'nome': 'MY PLACE ROMA',
        'url': 'https://www.myplaceroma.com/products/new-balance-1906d-protection-pack-silver-metallic?variant=48176830808392&country=IT&currency=EUR&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&g_c_l_i_d=Cj0KCQjw35bIBhDqARIsAGjd-cZPVzIBm1HZKRmn2Lf9U8-Uts5U9V4aphKRF_hODUDVR1QJOjGbip4aAqLfEALw_wcB&g_b_r_a_i_d=0AAAAAqtDKblvK36I3lU_K2gvT0LWVjx_B&w_b_r_a_i_d=CkwKCAjwvJHIBhBGEjwAKJvepDc1TumBS1m0Jar8YETjNDn9M662GcmSsb02bOcKs0XYxNtbc-95eS0LgdMDeGe7BI1KTWPa3Z4aAgVG&gad_source=1&gad_campaignid=21783161745&gbraid=0AAAAAqtDKblvK36I3lU_K2gvT0LWVjx_B&gclid=Cj0KCQjw35bIBhDqARIsAGjd-cZPVzIBm1HZKRmn2Lf9U8-Uts5U9V4aphKRF_hODUDVR1QJOjGbip4aAqLfEALw_wcB',
        'selettore_prezzo': ('p', {'class': 'f8pr-price s1pr',})
    }
]

# Funzione che pulisce e converte il prezzo
def pulisci_prezzo(prezzo_str):
    """
    Converte una stringa di prezzo (es. "€ 1.299,00")
    in un numero float (es. 1299.0).
    Gestisce sia il formato IT (virgola) che US (punto).
    """
    if not prezzo_str:
        return None

    # tolgo gli spazi e simboli di valuta comuni
    prezzo_pulito = prezzo_str.strip()
    prezzo_pulito = prezzo_pulito.replace('Prezzo scontato', '')
    prezzo_pulito = prezzo_pulito.replace('£', '')
    prezzo_pulito = prezzo_pulito.replace('€', '')
    prezzo_pulito = prezzo_pulito.replace('$', '')
    prezzo_pulito = prezzo_pulito.replace(' ', '')

    # gestisco i diversi formati numerici
    
    # rimuovo eventuali caratteri non numerici
    if '.' in prezzo_pulito and ',' in prezzo_pulito:
        prezzo_pulito = prezzo_pulito.replace('.', '') # tolgo il punto delle migliaia
        prezzo_pulito = prezzo_pulito.replace(',', '.') # sostituisco la virgola dei decimali
    elif ',' in prezzo_pulito:
        prezzo_pulito = prezzo_pulito.replace(',', '.') 
          
    # converto in float
    try:
        return float(prezzo_pulito)
    except ValueError:
        print(f"Errore: non posso convertire '{prezzo_str}' in un numero.")
        return None

# Funzione che estrae il prezzo da un sito
def estrai_prezzo(url, tag, selettore):
    """
    Visita una singola URL e cerca di estrarre il prezzo
    usando il selettore fornito.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        
        # rispetto una pausa tra le richieste
        time.sleep(1) 
        
        if response.status_code != 200:
            return f"Errore {response.status_code}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price_tag = soup.find(tag, selettore)
        
        # estraggo il testo del prezzo
        if price_tag:
            testo_prezzo_sporco = ""
            price_node = price_tag.find(string=True, recursive=False)
            
            if price_node:
                testo_prezzo_sporco = price_node.strip()
            if not testo_prezzo_sporco:
                testo_prezzo_sporco = price_tag.text.strip()

            simbolo_valuta = "€"

            if "$" in testo_prezzo_sporco:
                simbolo_valuta = "$"
            elif "£" in testo_prezzo_sporco:
                simbolo_valuta = "£"

            prezzo_numerico = pulisci_prezzo(testo_prezzo_sporco)

            if prezzo_numerico is not None:
                return f"{simbolo_valuta} {prezzo_numerico:.2f}"
            else:
                return f"Non convertibile: {testo_prezzo_sporco}"
            
        else:
            return "Non disponibile"
        
    except requests.RequestException as e:
        return f"Errore di connessione: {e}"

# Funzione che invia l'email riepilogativa
def invia_riassunto_email(corpo_html):
    """
    Prende una stringa e la invia via email.
    """
    print("Invio email riepilogativa...")
    
    msg = EmailMessage()
    msg['Subject'] = 'Report Prezzi'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    # aggiungo il corpo HTML
    msg.add_alternative(corpo_html, subtype='html')

    # invio l'email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

# "main" del programma
if __name__ == "__main__":
    print("Avvio Price Tracker...")
    
    riassunto_html_lines = []
    riassunto_html_lines.append("<h1>Report prezzi scarpa: New Balance 1906D Protection Pack Silver Metallic </h1>")
    riassunto_html_lines.append("<p>Ecco i prezzi trovati in data odierna:</p>")
    riassunto_html_lines.append("<ul>")

    for sito in SITI_DA_CONTROLLARE:
        print(f"Controllo {sito['nome']}...")
        
        # estraggo i parametri per la funzione
        tag = sito['selettore_prezzo'][0]
        selettore = sito['selettore_prezzo'][1]
        
        prezzo = estrai_prezzo(sito['url'], tag, selettore)
        
        # aggingo una linea al riassunto HTML
        linea_html = f"<li><strong>{sito['nome']}:</strong> {prezzo} (<a href='{sito['url']}'>Vai al sito</a>)</li>"
        
        riassunto_html_lines.append(linea_html)
        print(f"{sito['nome']}: {prezzo}") # stampo a console

    riassunto_html_lines.append("</ul>") # chiudo la lista HTML
    print("--- Controllo terminato --- \n")

    # unisco le linee in un unico corpo HTML
    corpo_finale_html = "\n".join(riassunto_html_lines)
    
    # invio l'email
    invia_riassunto_email(corpo_finale_html)