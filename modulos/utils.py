import os
import re
import shutil
import zipfile
import PyPDF2
from pathlib import Path

import modulos.confidencial as cf


# descomprime todos los archivos comprimidos en una carpeta 
def descomprimir_archivos_en_carpeta(carpeta_contenedora_path, eliminar_comprimido):
    
    lista_path_carpeta_descomprimida =[]

    for archivo in os.listdir(carpeta_contenedora_path):

        if archivo.lower().endswith('.zip'):

            ruta_zip = os.path.join(carpeta_contenedora_path, archivo)
            print(f"Descomprimiendo: {archivo}")

            # Nombre de la carpeta destino = nombre del zip (sin extensión)
            nombre_expediente = os.path.splitext(archivo)[0]

            # lo paso por una expresion regular para quedarme con lo que me interesa
            nombre_expediente = re.findall(r'EX-\d{4}-\d{8}', nombre_expediente)[0]

            ruta_destino = os.path.join(carpeta_contenedora_path, nombre_expediente)

            # Crear carpeta si no existe
            if not os.path.exists(ruta_destino):
                os.makedirs(ruta_destino)
            
            try:
                with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                    zip_ref.extractall(ruta_destino)
                    print("Extraído correctamente.")

                lista_path_carpeta_descomprimida.append(ruta_destino)

                if eliminar_comprimido:
                    os.remove(ruta_zip)
            
            except zipfile.BadZipFile:
                print(f"Error: El archivo no es un .zip válido.")
            
            except Exception as e:
                print(f"Error al descomprimir: {e}")
    
    return lista_path_carpeta_descomprimida


def copiar_archivos_para_dt(carpeta_expediente_path):
    
    # Verificar si la carpeta destino existe
    if not os.path.isdir(carpeta_expediente_path):
        raise FileNotFoundError(f"La carpeta de destino no existe.")

    numero_de_SP = obtener_numero_sp(carpeta_expediente_path)
    numero_de_exp = re.findall(r'\d{8}', carpeta_expediente_path)[0]

    excel_para_DT = "archivosParaDT\\SP.xlsm"
    word_para_DT =  "archivosParaDT\\SolPed EX.docx" 
    
    # Copiar archivos
    try:
        destino_con_nuevo_nombre_excel_para_DT = os.path.join(carpeta_expediente_path,"SP "+ numero_de_SP + ".xlsm")
        shutil.copy(excel_para_DT, destino_con_nuevo_nombre_excel_para_DT)
        print(f"Copiado Excel")
        
        destino_con_nuevo_nombre_word_para_DT = os.path.join(carpeta_expediente_path,"SolPed "+ numero_de_SP+ " EX "+ numero_de_exp +".docx")
        shutil.copy(word_para_DT, destino_con_nuevo_nombre_word_para_DT)
        print(f"Copiado Word")

    except Exception as e:
        print(f"Error al copiar archivos:\n\n", e)


# devuelve una lista con los input ingresados con la forma necesaria de búsqueda
def listar_ingreso_ajustado(input : str):

    # lo paso por una expresión regular para quedarme con lo que me interesa
    list_input = re.findall(r'EX-\d{4}-\d{8}', input)

    list_input_modif = [n + cf.final_input for n in list_input]

    return list_input_modif


def obtener_numero_sp(carpeta_contenedora):

    expresion_palabra_sp = r'Sol\.Ped\.'  # Encuentra la palabra Sol.Ped.
    expresion_numero_sp = r'\d{8}'  # Encuentra números de solped


    ruta = Path(carpeta_contenedora)

    for f in ruta.iterdir():
        
        if f.is_file():
            
            with open(f, 'rb') as file:
                
                reader = PyPDF2.PdfReader(file)
                primer_pagina = reader.pages[0].extract_text()

                if re.search(expresion_palabra_sp, primer_pagina):
                    
                    # Dividimos el texto en líneas
                    lines = primer_pagina.splitlines()
                    
                    for line in lines:
                
                        if re.search(expresion_palabra_sp, line):
                            
                            numero_solped = re.search(expresion_numero_sp, line)
                            
                            return numero_solped[0]


