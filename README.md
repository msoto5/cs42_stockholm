# Stockholm
Programa que encripta archivos en la carpeta </home/$USER/infection>

## Manual
```
usage: stockholm.py [-h] [-r KEY] [-s] [-v]

Infecto /home/$USER/infection

optional arguments:
  -h, --help            show this help message and exit
  -r KEY, --reverse KEY
                        Junto con la clave introducida, revierte la infeccion
  -s, --silent          Si esta activa, no se mostrara ningun output (no se mostraranlos archivos cifrados durante
                        el proceso
  -v, --version         Muestra la version del programa. En caso de ejecutarse junto a -s, -s es ignorada
```

## Especificaciones
- Unicamente se encriptan los archivos con una de las extensiones a las que infecta [Wanacry](https://www.kaspersky.es/resource-center/threats/ransomware-wannacry). [Extensiones de Wanacry](https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5).
- La clave de encriptación de guarda en "./filekey.key"
- La encriptación y desencriptación se ha realizado con el moódulo ***fernet*** la biblioteca ***criptography***. * *Fernet* * tiene funciones integradas para la generaión de la clave,y el cifrado y el descifrado del texto entre otras. Para instalar la biblioteca * *criptography* * utilice: <pip install cryptography>

## Ejemplos de uso
- Muestra la ayuda del programa
```
$ python3 stockholm.py -h
```
- Mostrar la versión del programa
```
$ python3 stockholm.py -v
```
- Encripta los archivos de </home/$USER/infection>
```
$ python3 stockholm.py
```
- Desencripta los archivos de </home/$USER/infection>
```
$ python3 stockholm.py -r filekey.key
```