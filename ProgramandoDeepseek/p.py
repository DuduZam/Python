from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# Configurar Selenium para manejar Cloudflare
driver = webdriver.Chrome()
driver.get("https://mediastream.platzi.com/video/h/512e13acaca1ebcd2f000279/620aced51ddf3808d2a61ff6_620aced51ddf3808d2a62002.mp4")

# Time.sleep() espera a que mediastream.platzi.com elimine los CAPCHA
time.sleep(10)

# Obtener cookies de la sesión
cookies = driver.get_cookies()
driver.quit()

# Usar cookies con requests para descargar el video
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Iniciar descarga del video
response = session.get("https://mediastream.platzi.com/video/h/512e13acaca1ebcd2f000279/620aced51ddf3808d2a61ff6_620aced51ddf3808d2a62002.mp4", headers={'Referer': 'https://mediastream.platzi.com'})

with open('video.mp4', 'wb') as f:
    f.write(response.content)
    #preguntar a AI