# Stockholm
Encripts files in /home/$USER/infection directory

## Getting started
Before running [stockholm.py](stockholm.py) you need to install the following library:
- Cryptography
```bash
pip install cryptography
```

## Manual
```
usage: stockholm.py [-h] [-r KEY] [-s] [-v]

Encripts files in /home/$USER/infection directory

optional arguments:
  -h, --help            show this help message and exit
  -r KEY, --reverse KEY
                        Decript files in '/home/$USER/infection'. Key file must be specified as argument.
  -s, --silent          No output will be shown in terminal
                        el proceso
  -v, --version         Shows program version
```

## Especificaciones
- [Stockholm.py](stockholm.py) only encripts files with extensions that [Wanacry](https://www.kaspersky.es/resource-center/threats/ransomware-wannacry) infected. Those extensions are included [here](https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5).
- Encription key is save as "filekey.key" in the same directory as stockholm.py
- Encription and decription was made with ***fernet*** module from the ***criptography*** library.


## Examples
- Show program help:
```
$ python3 stockholm.py -h
```

- Print program version:
```
$ python3 stockholm.py -v
```

- Encript files in '/home/$USER/infection' directory
```
$ python3 stockholm.py
```

- Decript files in '/home/$USER/infection' directory
Desencripta los archivos de '/home/$USER/infection'
```
$ python3 stockholm.py -r filekey.key
```
