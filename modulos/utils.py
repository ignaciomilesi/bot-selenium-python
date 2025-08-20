import os
import re
import shutil
import zipfile


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

    excel_para_DT = "archivosParaDT\\SP.xlsm"
    word_para_DT =  "archivosParaDT\\SolPed EX.docx" 
    
    # Copiar archivos
    try:
        shutil.copy(excel_para_DT, carpeta_expediente_path)
        print(f"Copiado Excel")
        
        shutil.copy(word_para_DT, carpeta_expediente_path)
        print(f"Copiado Word")

    except Exception as e:
        print(f"Error al copiar archivos")

