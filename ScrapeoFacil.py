import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base
url = "https://quotes.toscrape.com/page/{}/"

# Listas para almacenar los datos
citas = []
autores = []
etiqueta = []

# Recorrer las primeras 10 páginas
for paginas in range(1, 11):
    response = requests.get(url.format(paginas))
    html = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar todos los bloques de citas
    bloque_frases = html.find_all('div', class_='quote')
    
    for frase in bloque_frases:
        texto = frase.find('span', class_='text').get_text()
        autor = frase.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in frase.find_all('a', class_='tag')]
        
        citas.append(texto)
        autores.append(autor)
        etiqueta.append(", ".join(tags))

# Crear el DataFrame
df = pd.DataFrame({
    "Cita": citas,
    "Autor": autores,
    "Etiquetas": etiqueta
})

# Mostrar los primeros 5 resultados
print(df.head(10))

# Guardar en un archivo CSV
df.to_csv("citas_scrapeadas.csv", index=False, encoding='utf-8')