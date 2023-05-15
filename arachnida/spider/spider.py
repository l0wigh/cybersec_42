#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys
import os
import requests
import shutil


# Getting every links on the page
def getlinks(addr):
    html_page = requests.get(addr[0])
    soup = BeautifulSoup(html_page.text, 'html.parser')
    for link in soup.find_all('a'):
        try:
            if link.get('href').startswith("http://") or link.get('href').startswith("https://"):
                addr.append(link.get('href'))
            else:
                addr.append(addr[0] + link.get('href'))
        except Exception:
            print("<a> tag doesn't have a link")
    return addr


def getimages(addr, folder):
    for link in addr:
        for img_link in BeautifulSoup(requests.get(link).text, 'html.parser').find_all('img'):
            if (img_link.get('src').startswith("http")):
                if img_link.get('src').endswith('.png') or img_link.get('src').endswith('.bmp') or img_link.get('src').endswith('.jpg') or img_link.get('src').endswith('.jpeg') or img_link.get('src').endswith('.gif'):
                    r = requests.get(img_link.get('src'), stream=True)
                    print("\33[2K\rSaving : " + img_link.get('src'), end="")
                    with open(folder + img_link.get('src').rsplit('/', 1)[1], 'wb') as out_file:
                        shutil.copyfileobj(r.raw, out_file)
                else:
                    print("\33[2K\rNot a picture")


def main(argv):
    recursive = 0
    path = "./data/"
    if len(argv) < 2:
        print("Manque des arguments bonhomme")
    else:
        argv.pop(0)
        while len(argv) != 1:
            if argv[0] == "-r":
                argv.pop(0)
                if argv[0] == "-l":
                    argv.pop(0)
                    recursive = int(argv[0])
                    continue
                else:
                    recursive = 5
                    continue
            if argv[0] == "-p":
                argv.pop(0)
                path = "./" + argv[0] + "/"
                continue
            else:
                argv.pop(0)
        os.system("rm -rf " + path + " 2> /dev/null")
        os.system("mkdir " + path + " 2> /dev/null")
        if recursive == 0:
            addr = argv
            getimages(addr, path)
        else:
            addr = []
            addr.append(argv[0])
            while recursive != 0:
                addr = getlinks(addr)
                recursive = recursive - 1
            getimages(addr, path)


main(sys.argv)
