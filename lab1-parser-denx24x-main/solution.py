import requests
import sys

PAGE_LIMIT = 121
session = requests.Session()


def cut_detail(text, detail, tag):
    return text.split(detail)[-1].split("<"  + tag + ">")[1].split("</" + tag + ">")[0]


result = []
for i in range(PAGE_LIMIT):
    data = session.get("https://smarfony.ru/page/" + str(i + 1))
    for i in data.text.split("class=\"card\"")[:-1]:
        url = i.split("\"")[-2]
        details = session.get(url).text
        try:
            curent_data = [
            cut_detail(details, "Операционная система", "span"), # enum
            cut_detail(details, "Фирма", "td"), # enum
            int(cut_detail(details, "Объём оперативной памяти (RAM)", "td").split()[0]), 
            int(cut_detail(details, "Kоличество ядер процессора", "td").split()[0]),
            float(cut_detail(details, "Диагональ", "td").split("&")[0]), 
            float(cut_detail(details, "Ширина", "td").split()[0]),
            float(cut_detail(details, "Высота", "td").split()[0]) 
            ]
            result.append(curent_data)
        except Exception:
            continue
    
sys.stdout = open("output.csv", "w")
print("OS;Producer;RAM;CPU cores;Diagonal;Width;Height")
for i in result:
    print(";".join(map(str, i)).replace(".", ","))