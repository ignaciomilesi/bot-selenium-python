import tkinter as tk

import modulos.configBot as configBot

class Interface_config:
    def generar_ventana(self, root : tk.Tk):
       
        modificacion = configBot.existe_config() #para determinar si creo o modifico


        texto_ventana = "Editar config" if modificacion else "Nueva config"

        root.title(texto_ventana)
        root.geometry("620x240")

        if modificacion:
            config = configBot.obtener_config()
        
        else:
            config = {
                "USUARIO" : "",
                "PASSWORD" : "",
                "CARPETA_DE_DESCARGA" : "",
                "LINK_DE_COMIENZO" : "",
                "CHROMEDRIVER_PATH" : ""
            }

        self.entradas = {}  # Para guardar las Entry widgets


        texto_titulo = "Editar config:" if modificacion else "Archivo config no encontrado. Cree archivo config:"
        
        titulo = tk.Label(root, text=texto_titulo, font=("Arial", 10))
        titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Crear los labels y entries dinámicamente
        for i, (campo, valor) in enumerate(config.items(), start=1):
           
            tk.Label(root, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            
            entrada = tk.Entry(root, width=75)
            entrada.insert(0, valor)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            
            self.entradas[campo] = entrada

        # Botón para guardar
        
        texto_boton = "Guardar" if modificacion else "Crear"
            
        
        boton_guardar = tk.Button(root, text=texto_boton, command=self.guardar)
        boton_guardar.grid(row=len(config)+1, column=0, columnspan=2, pady=15)

        # guardo la configuración del root dentro de la class
        self.root = root

    def guardar(self):
        nuevos_valores = {campo: entry.get() for campo, entry in self.entradas.items()}
        
        configBot.guarda_config(nuevos_valores)

        print("Nuevos valores guardados:")

        self.root.destroy()
