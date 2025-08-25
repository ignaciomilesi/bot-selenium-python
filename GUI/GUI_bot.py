from modulos.bot import Bot
import modulos.configBot as configBot
import modulos.utils as utils

from GUI.GUI_config import Interface_config

import tkinter as tk


class Interface_bot:
    
    def generar_ventana(self, root : tk.Tk):
        
        root.title("Descargar Expediente")
        root.geometry("350x90")

        # Crear la barra de menú
        barra_menu = tk.Menu(root)
        root.config(menu=barra_menu)

        # Menú del Config
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Abrir", command=self._abrir_config)

        # Agregar los menús a la barra
        barra_menu.add_cascade(label="Config", menu=menu_archivo)

        etiqueta_sup_input = tk.Label(root, text = "Ingrese expediente", font=("Arial", 10), anchor= "w")
        etiqueta_sup_input.pack(padx=5, pady=(4,0), fill='x')

        # Frame para botones 
        frame_input = tk.Frame(root)
        frame_input.pack(fill='x', padx=5) 

        # Configurar las columnas del frame (para que la col 0 se expanda)
        frame_input.columnconfigure(0, weight=1)

        # Botón (Buscar)
        boton_busqueda = tk.Button(frame_input, text="Buscar", command=self._buscar_expediente)
        boton_busqueda.grid(row=0, column=1)

        # Input para el ingreso del expediente
        self.exp_buscado = tk.Entry(frame_input, font=("Arial", 10))
        self.exp_buscado.grid(row=0, column=0, sticky="ew", padx=(2,5))


        # etiqueta_inf_input = tk.Label(root, anchor= "w", font=("Arial", 7),text = "(puede ser mas de uno, solo se necesita ingresar \"EX-####-########\")")
        # etiqueta_inf_input.pack(padx=5, pady=2, fill='x')

        # Focus al input al abrir la ventana y Asociar la tecla Enter a la función
        self.exp_buscado.focus_set()
        self.exp_buscado.bind("<Return>", self._buscar_expediente)

        # Checkbox para marcar si quiero solo descargar
        self.checkbox_solo_busqueda = tk.BooleanVar()
        self.checkbox_solo_busqueda.set(True)
        checkbox = tk.Checkbutton(root, text="Agregar archivos para DT", variable=self.checkbox_solo_busqueda, anchor="w")
        checkbox.pack(padx=2, fill='x')

        

        # guardo la configuración del root dentro de la class
        self.root = root

        # reviso si tengo la configuración
        self._revisar_config()

            
    
    # Función buscar expediente
    def _buscar_expediente(self, event=None):

        if not hasattr(self, 'exp_buscado'):
            raise ValueError("Error al obtener el EXP del GUI")
        
        if not hasattr(self, 'checkbox_solo_busqueda'):
            raise ValueError("Error al obtener el checkbox del GUI")
        
        list_exp_busqueda = utils.listar_ingreso_ajustado(self.exp_buscado.get())

        bot = Bot()
        
        bot.set_config()
        
        bot.iniciar_navegador()
        
        for i, exp_busqueda in enumerate(list_exp_busqueda):

            if i > 0:
                bot.volver_pagina_busqueda()

            print("---------- Realizando", i+1, "de", len(list_exp_busqueda), "expediente ----------")
            
            bot.buscar_expediente(exp_busqueda)

            print("-------------------------------------------------------------")

        print("Verificando descargas")
        bot.verificar_finalizadas_todas_descarga()
        print("Finalizaron todas las descargas")

        lista_carpetas_descomprimidas = utils.descomprimir_archivos_en_carpeta(
                carpeta_contenedora_path = bot.CARPETA_DE_DESCARGA,
                eliminar_comprimido = True)
            
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
