from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configurar el navegador
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin abrir ventana
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abrir la página
url = "https://www.ultracasas.com"
driver.get(url)

# Esperar a que cargue el contenido
time.sleep(5)

# Extraer los elementos de las propiedades
properties = driver.find_elements(By.CLASS_NAME, "listing-card")

# Crear listas para almacenar los datos
direcciones = []
precios = []
habitaciones = []
tamanios = []

# Recorrer cada propiedad
for prop in properties:
    try:
        direccion = prop.find_element(By.CLASS_NAME, "listing-location").text
        precio = prop.find_element(By.CLASS_NAME, "listing-price").text
        detalles = prop.find_elements(By.CLASS_NAME, "listing-detail-item")

        # Extraer habitaciones y tamaño si están disponibles
        hab = detalles[0].text if len(detalles) > 0 else "N/A"
        tam = detalles[1].text if len(detalles) > 1 else "N/A"

        direcciones.append(direccion)
        precios.append(precio)
        habitaciones.append(hab)
        tamanios.append(tam)
    except Exception as e:
        print("Error en una propiedad:", e)

# Cerrar el navegador
driver.quit()

# Crear el DataFrame
df = pd.DataFrame({
    "Dirección": direcciones,
    "Precio": precios,
    "Habitaciones": habitaciones,
    "Tamaño": tamanios
})

# Mostrar los primeros resultados
print(df.head())