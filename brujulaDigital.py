 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

vec = ["politica/","economia/"]
aux = "https://www.brujuladigital.net/"
url = aux
num = "p="
df = pd.DataFrame(columns=["titular", "fecha", "contenido"])
#df_principal = pd.DataFrame(columns=["titular", "fecha", "contenido"])
for n in vec:
    seccion = n 
    for i in range(1500):
        b= i+1
        auxi = str(b)
        url = aux + n + num + auxi
        print(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            #print(response)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding = 'utf-32BE')
                nota_links = soup.find_all(class_="bxImgL")
                print(nota_links)
                for link in nota_links:
                    url = link['href']
                    #print(url)
                    response1 = requests.get(url)
                    soup1 = BeautifulSoup(response1.content, 'html.parser', from_encoding = 'utf-32BE')
                    #print(f"URL encontrada: {url}")
                    #extraer html de cada nodo
                    try:
                        titulo = [titulo.text.strip() for titulo in soup1.select('h1')]
                        fecha = [fecha.text.strip() for fecha in soup1.select('.fecha-cnt')]
                        contenido = [contenido.text.strip() for contenido in soup1.select('.contIn')]
                        df_aux = pd.DataFrame({"titular": titulo, "fecha": fecha, "contenido": contenido, "url": url, "seccion": seccion})
                        #print(df_aux)
                        df = pd.concat([df, df_aux]).drop_duplicates().reset_index(drop=True)
                        print(df)
                        #se repite 2 veces y eliminar header 
                        if len(df) >= 10:
                            ruta_guardar = "C:\\Users\\gusta\\OneDrive\\Documentos"
                            data = "brujula_digital.csv"
                            ruta_completa = os.path.join(ruta_guardar, data)
                            df.to_csv(ruta_completa,encoding='utf-32BE', mode='a', index=False,header=not os.path.exists(ruta_completa))
                            print("Se guardo parcialment el csv")
                            df = pd.DataFrame(columns=["titular", "fecha", "contenido", "url", "seccion"])
                    except ValueError as e:
                        print(f"Se produjo un error : {e}")
                        continue
            else:
                print(response)
        except requests.exceptions.RequestException as e:
            print(f"Se produjo un error : {e}")
            continue
    if not df.empty:
        ruta_guardar = "C:\\Users\\gusta\\OneDrive\\Documentos"
        data = "brujula_digital.csv"
        ruta_completa = os.path.join(ruta_guardar, data)
        df.to_csv(ruta_completa, encoding='utf-32BE', mode='a', index=False, header=not os.path.exists(ruta_completa))
        print("Se guardaron los datos restantes")
print("Termino")
