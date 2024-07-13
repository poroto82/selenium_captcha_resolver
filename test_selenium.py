from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin GUI)

chrome_driver_path = './driver/chromedriver'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Abrir Google
    driver.get("https://www.google.com")

    # Buscar el campo de búsqueda y escribir la consulta
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python")
    search_box.send_keys(Keys.RETURN)

    # Esperar a que se carguen los resultados
    time.sleep(2)  # Es mejor usar WebDriverWait en lugar de sleep para esperar eventos específicos

    # Extraer los títulos de los resultados de búsqueda
    results = driver.find_elements(By.CSS_SELECTOR, 'h3')
    for index, result in enumerate(results):
        print(f"Result {index + 1}: {result.text}")

finally:
    # Cerrar el navegador
    driver.quit()