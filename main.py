import os
import argparse
import time

from exceptiongroup import catch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service
import json
from typing_extensions import final

home_dir = os.environ['HOME']
from ClassDTO import ClassDTO
def creacionRutas(navegador: ClassDTO):

    print(f'Tu navegador : {navegador.navegador}')

    if navegador.navegador == "chrome":
        chrome_profile_path = f"{home_dir}/.config/google-chrome/Default"
        options = ChromeOptions()  # Usamos las opciones de Chrome
        options.add_argument(f"user-data-dir={chrome_profile_path}")
        options.add_argument("--headless")  # Si deseas usar sin interfaz gráfica
        driver = webdriver.Chrome(options=options)

    elif navegador.navegador == "firefox":
        if navegador.perfil is None:
            print("Perfil de Firefox no especificado.")
            return
        firefox_profile_path = f"{home_dir}/.mozilla/firefox/{navegador.perfil}"
        print(firefox_profile_path)
        options = FirefoxOptions()
        options.add_argument(f"-profile {firefox_profile_path}")
        options.add_argument("--headless")  # Evitar iniciar interfaz gráfica
        driver = webdriver.Firefox(options=options)
    elif navegador.navegador == "brave":
         # brave_binary_path = f"/opt/brave.com/brave/brave-browser"
         brave_binary_path = f"/usr/bin/brave-browser-stable"
         brave_profile_path= f"{home_dir}/.config/BraveSoftware/Brave-Browser"
         options = ChromeOptions()
         # options.add_argument("--headless")  # Si deseas usar sin interfaz gráfica
         options.binary_location=brave_binary_path
         options.add_argument(f'user-data-dir={brave_profile_path}')
         # options.add_argument()
         # service = Service(brave_binary_path)
         # driver = webdriver.Chrome(options=options,service=service)
         driver = webdriver.Chrome(options=options)
         # time.sleep(20)

    else:
        print("Navegador no soportado")
        return

    try:

        driver.get(navegador.url_origen)
        time.sleep(5)
        # time.sleep(20)

        auth_token = driver.execute_script('return localStorage.getItem("auth")')
        auth_data=json.loads(auth_token)

        auth_token=auth_data["token"]
        print(f"Auth token: {auth_token}")
        driver.get(navegador.url_destino)
        # driver.execute_script(f'localStorage.setItem("auth","s")')

        driver.execute_script(f'localStorage.setItem("auth",JSON.stringify({{token: "{auth_token}"}}))')
        driver.execute_script(f'localStorage.setItem("permissions","owner")')
        time.sleep(20)
        # driver.execute_script(f'localStorage.setItem("auth",JSON.stringify({{auth_token: "{auth_token}"}}))')
    except Exception as e:
        print(f'Problemas con la ejecucion verifica parametros')
        print(e)
    finally:
        driver.quit()
        print(f'Finalizado')



def posiblesPerfiles(navegador):
    print("Debes introducir tu perfil")

    if navegador == "firefox":
        os.system(f'ls {os.environ["HOME"]}/.mozilla/firefox/')
        return f'{os.environ["HOME"]}/.mozilla/firefox/'

    elif navegador == "chrome":
        os.system(f'ls {os.environ["HOME"]}/.config/google-chrome/')
        return f'{os.environ["HOME"]}/.config/google-chrome/'

    elif navegador == "brave":
        os.system(f'ls {os.environ["HOME"]}/.config//BraveSoftware/Brave-Browser')
        return f'{os.environ["HOME"]}/.config//BraveSoftware/Brave-Browser/'


def main(args):
    print(f'URL ORIGEN : {args.URL_ORIGEN}')
    print(f'URL DESTINO : {args.URL_DESTINO}')
    print(f'NAVEGADOR : {args.NAVEGADOR}')
    print(f'Perfil : {args.PERFIL}')

    # Crear el objeto DTO con la información proporcionada
    Navegacion = ClassDTO(
        url_origen=args.URL_ORIGEN,
        url_destino=args.URL_DESTINO,
        navegador=args.NAVEGADOR,
        perfil=args.PERFIL
    )


    creacionRutas(navegador=Navegacion)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Procesamiento de una URL")
    parser.add_argument("--URL-ORIGEN", type=str, required=True, help="La URL de origen a procesar")
    parser.add_argument("--URL-DESTINO", type=str, required=True, help="La URL de destino a procesar")
    parser.add_argument("--NAVEGADOR", type=str, required=True, help="Introduce tu navegador (chrome-firefox-brave)")
    parser.add_argument("--PERFIL", type=str, required=False, help="Introduce tu perfil")

    args = parser.parse_args()

    if args.PERFIL is None:
        posiblesPerfiles(args.NAVEGADOR)
    else:
        main(args)
""""
# chrome_profile_path="/home/fgonzalez@corp.sportclub.com.ar/.config/google-chrome/Default"
# URL_Inspeccion="https://buenclub-base.dev.sportclub.com.ar/socios"

# options = Options()
# options.add_argument(f"user-data-dir={chrome_profile_path}")
# driver = webdriver.Chrome(options=options)

# driver.get(URL_Inspeccion)
# driver.implicitly_wait(1000)  # Adjusted wait time to 10 seconds
# time.sleep(200)
# Add your code to interact with the webpage using your Chrome profile

# driver.quit()  # Close the browser window when finished
#
firefox_profile_path = "/home/fgonzalez@corp.sportclub.com.ar/.mozilla/firefox/6nmikg7p.default-release"
URL_Auth_Origin="https://buenclub-frontend.stg.sportclub.com.ar/socios"
URL_Auth_Destini="https://buenclub-frontend.dev.sportclub.com.ar/socios"
# Crear una instancia de Firefox con el perfil especificado
options = Options()
options.add_argument(f"-profile {firefox_profile_path}")
options.add_argument("--headless")  ## Evito iniciar interfaz grafica
# fp=webdriver.FirefoxProfile(firefox_profile_path)
# driver = webdriver.Firefox(fp)
# driver=webdriver.FirefoxProfile(firefox_profile_path)
driver = webdriver.Firefox(options=options)
time.sleep(1)
#{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjY2ZTA4ZmZlYzQ2MzY4NGYzOWE1MzhlOSIsImVtYWlsIjoiZmVkZXJpY29nb256YWxlekBzcG9ydGNsdWIudGVhbSIsInJvbGUiOiJvd25lciIsInNwaWNlIjoibW45WTcwdmhLYVNIIiwibWVyY2hhbnQiOltdLCJzZWRlIjpbXSwiYnJhbmRfaWQiOiI2MzI4YWZiMzU5ZDA1MmU2ODE3YzIyMDAiLCJuZWdvY2lvX2NlbnRyYWwiOnRydWUsImRhdGUiOiIxMC8wOS8yMDI0JyIsImV4cGlyZSI6IjIwMjQtMDktMTEgMTg6MzI6NDguNDM0OTk0IiwidmVyc2lvbiI6IjAuMS41In0.ao-ZbkAQapuucfUaN9589QAOzXY3xmYLyDR8qgRDGmE"}
# Obtencion de token de pagina auth
driver.get(URL_Auth_Origin)
auth_token=driver.execute_script('return localStorage.getItem("auth")')

auth_token=auth_token[1:-1]

driver.get(URL_Auth_Destini)
driver.execute_script(f'localStorage.setItem("auth",JSON.stringify({{auth_token: "{auth_token}"}}))')
# driver.execute_script("window.location='https://www.google.com.ar'")

# time.sleep(2)
# token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjY2ZTA4ZmZlYzQ2MzY4NGYzOWE1MzhlOSIsImVtYWlsIjoiZmVkZXJpY29nb256YWxlekBzcG9ydGNsdWIudGVhbSIsInJvbGUiOiJvd25lciIsInNwaWNlIjoibW45WTcwdmhLYVNIIiwibWVyY2hhbnQiOltdLCJzZWRlIjpbXSwiYnJhbmRfaWQiOiI2MzI4YWZiMzU5ZDA1MmU2ODE3YzIyMDAiLCJuZWdvY2lvX2NlbnRyYWwiOnRydWUsImRhdGUiOiIxMC8wOS8yMDI0JyIsImV4cGlyZSI6IjIwMjQtMDktMTEgMTg6MzI6NDguNDM0OTk0IiwidmVyc2lvbiI6IjAuMS41In0.ao-ZbkAQapuucfUaN9589QAOzXY3xmYLyDR8qgRDGmE"
# token="F"
# auth_token=driver.execute_script(f'localStorage.setItem("auth",JSON.stringify("{token}"))')
print(auth_token[1:-1])
# Realizar acciones en la página
# ...
# Cerrar el navegador
driver.quit()
"""