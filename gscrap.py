from selenium import webdriver
import json
import os
import urllib.request
import sys, argparse

print("\033[96m  ▄████   ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  \n ██▒ ▀█▒▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒\n▒██░▄▄▄░░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒\n░▓█  ██▓  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒\n░▒▓███▀▒▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░\n ░▒   ▒ ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░\n  ░   ░ ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░     \n░ ░   ░ ░  ░  ░  ░          ░░   ░   ░   ▒   ░░       \n      ░       ░  ░ ░         ░           ░  ░         \n                 ░                                    \033[92m")

parser = argparse.ArgumentParser()
parser.add_argument("--search", help="Especificar el termino de busqueda")
parser.add_argument("--scrolling", help="Especificar la constante de scrolling para web driver", type=int)
args = parser.parse_args()

searchterm = args.search if args.search else ''
scrolling = args.scrolling if args.scrolling else 100


if searchterm != '':
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    url = "https://www.google.co.in/search?q=" + searchterm + "&source=lnms&tbm=isch"
    browser = webdriver.Chrome('/home/bastian/bin/chromedriver', chrome_options=options)
    browser.get(url)
    # header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    counter = 0
    succounter = 0
    print("Google Images Scrapper v1.1 - by Bastian Muhlhauser\n[#] Creando carpeta ", searchterm)
    if not os.path.exists(searchterm):
        os.mkdir(searchterm)

    print("[#] Cargando imagenes")
    for _ in range(500):
        browser.execute_script("window.scrollBy(0,10000)")

    browser.find_element_by_id('smb').click()

    for _ in range(scrolling):
        browser.execute_script("window.scrollBy(0,10000)")
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        counter = counter + 1
        print("Imagenes Totales:", counter)
        print("Imagenes guardadas:", succounter)
        print("URL:", json.loads(x.get_attribute('innerHTML'))["ou"])

        img = json.loads(x.get_attribute('innerHTML'))["ou"]
        imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
        try:
            req = urllib.request.Request(img)
            raw_img = urllib.request.urlopen(req).read()
            File = open(os.path.join(searchterm, searchterm + "_" + str(counter) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succounter = succounter + 1
        except:
            print("No se pudo descargar la imagen")

    browser.close()