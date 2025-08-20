from modulos.bot import Bot
import modulos.configBot as configBot
import modulos.utils as utils

from GUI.GUI_config import Interface_config

import tkinter as tk


class Interface_bot:
    
    def generar_ventana(self, root : tk.Tk):
        
        root.title("Descargar Expediente")
        root.geometry("320x120")

        # Frame para contener el botón de config
        frame_superior = tk.Frame(root)
        frame_superior.pack(pady=10, fill='x')  

        # Botón (Config)
        boton_Config = tk.Button(frame_superior, text="Abrir Config", command=self._abrir_config)
        boton_Config.pack(side="left", padx=5)


        # Input para el ingreso del expediente
        self.exp_buscado = tk.Entry(root, font=("Arial", 10), width=40)
        self.exp_buscado.pack(padx=5, pady=5, fill='x')

        # Focus al input al abrir la ventana
        self.exp_buscado.focus_set()

        # Asociar la tecla Enter a la función mostrar_input
        self.exp_buscado.bind("<Return>", self._buscar_expediente)


        # Frame para checkbox y botón de búsqueda
        frame_inferior = tk.Frame(root)
        frame_inferior.pack(pady=5, fill='x')  

        # Checkbox para marcar si quiero solo descargar
        self.checkbox_solo_busqueda = tk.BooleanVar()
        self.checkbox_solo_busqueda.set(True)
        checkbox = tk.Checkbutton(frame_inferior, text="Agregar archivos para DT", variable=self.checkbox_solo_busqueda)
        checkbox.pack(side="left", padx=5)

        # Botón (Buscar), alineado a la derecha
        boton_busqueda = tk.Button(frame_inferior, text="Buscar", command=self._buscar_expediente)
        boton_busqueda.pack(side="right", padx=5)

        # guardo la configuración del root dentro de la class
        self.root = root

        # reviso si tengo la configuración
        self._revisar_config()

            
    
    # Función buscar expediente
    def _buscar_expediente(self, event=None):

        if not hasattr(self, 'config_bot'):
            raise ValueError("No se cargó la configuración del bot.")
        
        if not hasattr(self, 'exp_buscado'):
            raise ValueError("Error al obtener el EXP del GUI")
        
        if not hasattr(self, 'checkbox_solo_busqueda'):
            raise ValueError("Error al obtener el checkbox del GUI")
        
        bot = Bot()
        
        bot.set_config(
            USUARIO = self.config_bot["USUARIO"], 
            PASSWORD = self.config_bot["PASSWORD"],
            CARPETA_DE_DESCARGA = self.config_bot["CARPETA_DE_DESCARGA"],
            CHROMEDRIVER_PATH = self.config_bot["CHROMEDRIVER_PATH"])

        bot.set_expediente(self.exp_buscado.get())

        bot.iniciar_driver()

        bot.abrir_navegador(self.config_bot["LINK_DE_COMIENZO"]) 


        try:
            #time.sleep(1) # esperamos 1 segundos para que cargue mejor la pagina
            bot.iniciar_sesion()
            print("sesión iniciada")

            #time.sleep(2) 
            bot.buscar_expediente()
            print("Expediente encontrado")
            
            #time.sleep(3) 
            bot.descargar_expediente()
            print("Comenzó la descarga del expediente")

            bot.verificar_finalizadas_todas_descarga()
            print("Se descargo el expediente")
        
        except Exception as e:
            print("\n\n ----- ERROR!!! ----- \n\n")
            print(e)
            print("\n\n ----- ERROR!!! ----- \n\n")

        
        lista_carpetas_descomprimidas = utils.descomprimir_archivos_en_carpeta(
            carpeta_contenedora_path=self.config_bot["CARPETA_DE_DESCARGA"],
            eliminar_comprimido=True)
        
        if self.checkbox_solo_busqueda.get():
            for carpeta in lista_carpetas_descomprimidas:

                utils.copiar_archivos_para_dt(carpeta)

        bot.apagar()

        self.root.destroy()


    # Función para el segundo botón
    def _abrir_config(self):
        
        # Crear la ventana desde acá
        config_window = tk.Toplevel(self.root)

        # Hacerla modal
        config_window.transient(self.root)
        config_window.grab_set()

        # Delegar la interfaz a Interface_config

        GUI_config = Interface_config()

        GUI_config.generar_ventana(config_window)

        # Esperar que se cierre antes de seguir
        config_window.wait_window()



    def _revisar_config(self):
        
        if not configBot.existe_config():
            self._abrir_config()

        self.config_bot = configBot.obtener_config()
