from datetime import datetime, timedelta
from pathlib import Path

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import modulos.confidencial as cf


SUFIJO_ID_USUARIO = "l"
SUFIJO_ID_PASSWORD = "r"
SUFIJO_ID_BOTON_INGRESO = "t"
SUFIJO_ID_EXPEDIENTE = "i"
SUFIJO_ID_BOTON_BUSQUEDA_EXPEDIENTE = "s0"
SUFIJO_ID_DESPLEGABLE = "hb-btn" # 18-btn
SUFIJO_ID_VISUALIZAR = "jb" # 38
SUFIJO_ID_BOTON_DESCARGA = "7c"  

class Bot:

    def __init__(self):
        pass                       

    def set_config(self, USUARIO, PASSWORD, CARPETA_DE_DESCARGA, CHROMEDRIVER_PATH):
        self.USUARIO = USUARIO
        self.PASSWORD = PASSWORD
        self.CARPETA_DE_DESCARGA = CARPETA_DE_DESCARGA
        self.CHROMEDRIVER_PATH = CHROMEDRIVER_PATH

    def set_expediente(self, EXPEDIENTE):
        self.EXPEDIENTE = EXPEDIENTE

    def iniciar_driver(self):

        # Validar si los parámetros necesarios fueron configurados
        if not hasattr(self, 'CARPETA_DE_DESCARGA'):
            raise ValueError("CARPETA_DE_DESCARGA no está configurado.")
        
        # Configuramos el directorio de descarga
        prefs = {
            "download.default_directory": self.CARPETA_DE_DESCARGA,
            "download.prompt_for_download": False,  # No mostrar el diálogo de descarga
            "download.directory_upgrade": True, 
        }

        options = Options()
        options.add_experimental_option("prefs", prefs)

        # para que no sea tan verboso
        options.add_argument("--log-level=3")
        
        chromedriver_path = self.CHROMEDRIVER_PATH 
        service = Service(chromedriver_path, log_path="NUL")

        # Iniciamos el navegador con las opciones configuradas
        self.DRIVER = webdriver.Chrome(service=service, options=options)

    def abrir_navegador(self, pagina):
        self.DRIVER.get(pagina) 

    def _encontrar_id_base(self):
        # La base del id son los primeros 4 caracteres del id del primer div

        if not hasattr(self, 'DRIVER'):
            raise ValueError("el DRIVER no está configurado.")

        # Espera que cargue el primer div dentro del body
        root_div = WebDriverWait(self.DRIVER, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]"))
        )

        # Extrae los primeros 4 caracteres del ID del div
        base_id = root_div.get_attribute("id")[:4]

        print(f"ID dinámico encontrado: {base_id}")

        return base_id

    def iniciar_sesion(self):

        if not hasattr(self, 'DRIVER'):
            raise ValueError("el DRIVER no está configurado.")
        
        if not hasattr(self, 'USUARIO'):
            raise ValueError("el USUARIO no está configurado.")
        
        if not hasattr(self, 'PASSWORD'):
            raise ValueError("el PASSWORD no está configurado.")
        
        # Buscamos la base del ID
        base_id = self._encontrar_id_base()

        # Espera a que el input del usuario sea visible 
        input_usuario = WebDriverWait(self.DRIVER, 10).until(
            EC.visibility_of_element_located((By.ID, base_id + SUFIJO_ID_USUARIO))
        )

        # Hace clic y escribe el usuario
        input_usuario.click()
        input_usuario.send_keys(self.USUARIO)


        # Hace clic y escribe el password
        input_password = self.DRIVER.find_element(By.ID, base_id + SUFIJO_ID_PASSWORD)
        input_password.click()
        input_password.send_keys(self.PASSWORD)

        # Hace clic en el ingreso
        boton_ingreso = self.DRIVER.find_element(By.ID, base_id + SUFIJO_ID_BOTON_INGRESO)
        boton_ingreso.click()

        time.sleep(0.2) # Le damos n margen de tiempo antes de cambiar

    def buscar_expediente(self):  

        if not hasattr(self, 'DRIVER'):
            raise ValueError("el DRIVER no está configurado.")
        
        if not hasattr(self, 'EXPEDIENTE'):
            raise ValueError("el EXPEDIENTE no está configurado.")
        
        # debido a las re-direcciones, verificamos que estemos en la dirección correcta
        WebDriverWait(self.DRIVER, 30).until(
            lambda d: d.current_url == cf.link1
            )

        # Buscamos la base del ID
        base_id = self._encontrar_id_base()

        # Espera a que el input del expediente sea visible
        input_expediente = WebDriverWait(self.DRIVER, 10).until(
            EC.visibility_of_element_located((By.ID, base_id + SUFIJO_ID_EXPEDIENTE))
        )

        # Hace clic y escribe el expediente
        input_expediente.click()
        input_expediente.send_keys(self.EXPEDIENTE)

        # Hace clic en búsqueda
        boton_busqueda = self.DRIVER.find_element(By.ID, base_id + SUFIJO_ID_BOTON_BUSQUEDA_EXPEDIENTE)
        boton_busqueda.click()


    def descargar_expediente(self):  

        if not hasattr(self, 'DRIVER'):
            raise ValueError("el DRIVER no está configurado.")
        
        WebDriverWait(self.DRIVER, 30).until(
            lambda d: d.current_url == cf.link2
            )

        # Buscamos la base del ID
        base_id = self._encontrar_id_base()

        # Espera a que el desplegable sea visible y hacer click
        desplegable = WebDriverWait(self.DRIVER, 30).until(
            EC.visibility_of_element_located((By.ID, base_id + SUFIJO_ID_DESPLEGABLE))
        )
        desplegable.click()
       

        # Hace clic en visualizar
        visualizar = WebDriverWait(self.DRIVER, 30).until(
            EC.visibility_of_element_located((By.ID, base_id + SUFIJO_ID_VISUALIZAR))
        )
        visualizar.click()

        # Hace clic en descarga
        time.sleep(1) # le damos un segundo para que cargue
        
        boton_descarga = WebDriverWait(self.DRIVER, 10).until(
            EC.visibility_of_element_located((By.ID, base_id + SUFIJO_ID_BOTON_DESCARGA))
        )

        boton_descarga.click()

        self.esperar_comenzar_descarga()

        
            

    def apagar(self):
        
        self.DRIVER.quit()

    def esperar_comenzar_descarga(self):
        
        # esperamos para que cargue el Loader 
        time.sleep(0.1)

        # verificamos que haya aparecido y esperamos a que se valla
        WebDriverWait(self.DRIVER, 1).until(
            EC.visibility_of_element_located((By.ID, "zk_showBusy"))
        )
        
        WebDriverWait(self.DRIVER, 60).until(
            EC.invisibility_of_element_located((By.ID, "zk_showBusy")))
        
        time.sleep(0.5) # damos un marguen a que haya comenzado
        

    def verificar_finalizadas_todas_descarga(self):
        # vamos a la pagina de descarga y esperamos a que termine todas la descarga
        
        self.DRIVER.get("chrome://downloads")
        
        # verificamos que hayan terminado las descargas

        timeout = datetime.now() + timedelta(seconds=60)  # Esperar máxima 
        
        while True:
            items = self.DRIVER.execute_script("return document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;")
           
            contador_de_descargas_finalizadas = 0

            for item in items:
                if item["percent"] == 100:
                    contador_de_descargas_finalizadas += 1
                
            if contador_de_descargas_finalizadas == len(items):
                break  

            if datetime.now() > timeout: #Si se supera la espera maxima
                raise TimeoutError("Las descargas no finalizaron a tiempo.")
            
            time.sleep(0.5) # para no gastar mas CPU del necesario
        
        # verificamos que ya no queden archivos temporales de descarga
        
        timeout = datetime.now() + timedelta(seconds=30)  # Esperar máxima 

        while True:
           if not any(f.suffix == ".crdownload" for f in Path(self.CARPETA_DE_DESCARGA).iterdir()):
               break
           
           if datetime.now() > timeout: #Si se supera la espera maxima
                raise TimeoutError("Las descargas no finalizaron a tiempo.")
           
           time.sleep(0.1) # para no gastar mas CPU del necesario
                

