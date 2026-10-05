import os
import requests
from googlesearch import search
import time
import re

docs = [
    "ГОСТ 7.32-2017",
    "ГОСТ Р 15.301-2016",
    "ГОСТ Р 56602-2015",
    "ГОСТ Р 58239-2018",
    "ГОСТ Р 56571-2015",
    "ГОСТ Р 58467-2019",
    "ГОСТ Р 56553-2015",
    "ГОСТ 58750-2019",
    "ГОСТ Р 58242-2018",
    "ГОСТ Р 70299-2022",
    "ГОСТ Р 70300-2022",
    "ГОСТ Р 70303-2022",
    "ГОСТ Р 70301-2022",
    "ГОСТ Р 70302-2022",
    "ГОСТ Р 70305-2022",
    "ГОСТ Р 70304-2022",
    "ПУЭ 7 издание",
    "ГОСТ Р 50571-4-44-2011",
    "ГОСТ Р 50571.17-2000",
    "СП 76.13330.2016",
    "СП 256.1325800.2016",
    "Правила безопасности энергопринимающих установок 2017 968",
    "ТР ТС 004/2011",
    "ТР ТС 012/2011",
    "ТР ТС 020/2011",
    "Правила технической эксплуатации электроустановок потребителей 2003"
]

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name

def download():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    out_dir = '/Users/anton/Documents/NIRS/normative_docs'
    os.makedirs(out_dir, exist_ok=True)
    
    for doc in docs:
        query = f'"{doc}" filetype:pdf'
        print(f"Поиск: {doc}")
        try:
            # Увеличиваем таймаут и добавляем паузу между запросами к самому гуглу
            results = list(search(query, num_results=10, lang="ru", timeout=15, sleep_interval=2))
            downloaded = False
            for url in results:
                print(f"  Проверяем ссылку: {url}")
                try:
                    response = requests.get(url, headers=headers, timeout=15, verify=False)
                    if response.status_code == 200 and response.content.startswith(b'%PDF'):
                        filename = sanitize_filename(doc) + '.pdf'
                        filepath = os.path.join(out_dir, filename)
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        print(f"  [+] Успешно скачан: {filename}")
                        downloaded = True
                        break
                except Exception as e:
                    print(f"  [-] Ошибка скачивания с {url}: {e}")
            if not downloaded:
                print(f"  [!] Не удалось найти прямой PDF для {doc}")
        except Exception as e:
            print(f"  [-] Ошибка поиска для {doc}: {e}")
        time.sleep(3) # pause to avoid ban

if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    download()
