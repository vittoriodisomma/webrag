import os
import vdb
import time
import re
import requests as req
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

#MODEL = "gemma2:9b"
#MODEL = "mistral:latest"
MODEL = "mistral:latest"
USAGE = f"""Ciao, sono il tuo Webrag. Le opzioni possibili sono:
Digita https:// per indicizzare un sito
Digita una domanda. """

def pages_extraction(site, url):
    prompt = f"List of urls of the main 10 pages associated to {site} (only fully qualified and not broken or fake)."
    msg = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        response = req.post(url, json=msg, timeout=10)
        res = response.json()
        result = res.get("response", "error")
    except Exception as e:
        result = str(e)
    pattern = r'https?://[^\s)>\]\"]+'
    pages = []
    urls = re.findall(pattern, result) 
    for url in urls:
        try:
            response = req.get(url, timeout=10)
            if response.status_code == 200:
                pages.append(url)
        except Exception as e:
            print(f"Error {str(e)}")      
    return pages

def text_extraction(page):
    response = req.get(page, timeout=10)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "footer", "noscript"]):
        tag.decompose()
    content = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', content).strip()
    return text

def data_storage(url, db, page):
    content = text_extraction(page)
    prompt = f"Very short summary of {content}"
    msg = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        res = req.post(url, json=msg, timeout=10).json()
        content = res.get("response", "error")
    except Exception as e:
        content = str(e)
    result = db.insert(page, content)
    return result

def webrag(args):
    db = vdb.VDB(args)
    db.setup()
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))  
    auth = args.get("AUTH", os.getenv("AUTH"))
    base = f"https://{auth}@{host}/"
    url = f"{base}/api/generate"
    out = ''
    inp = str(args.get("input", ""))
    if inp == '':
        out = USAGE
    elif inp.startswith('https'):
        start = time.time()
        pages = pages_extraction(inp, url)
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda page: data_storage(url, db, page), pages))
        end = time.time()
        print('durata:', end-start)
        n_success = results.count('Caricamento effettuato su Milvus')
        if n_success == len(pages):
            out = 'Il sito è stato indicizzato correttamente.'
        else:
            out = 'Alcune pagine non sono state caricate.'   
    else:
        searches = db.search(inp)
        texts = [search['content'] for search in searches]
        urls = [search['url'] for search in searches]
        out = '\n'.join(texts)
        url = '\n'.join(urls)
        out += f'\n Per maggiori informazioni potete consultare le seguenti pagine {url}'
    return { "output": out}
