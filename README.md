# NIC.AR - consulta de dominios

![Static Badge](https://img.shields.io/badge/3-blue?style=plastic&label=Python&color=blue) ![Static Badge](https://img.shields.io/badge/selenium-blue?style=plastic&color=blue)


Script para hacer consulta de dominios en nic.ar

El script permite consultar a través del sitio nic.ar la disponibilidad de varios dominios de forma secuencial, 
tambien es válido si se define un único dominio. Requiere chromedriver y selenium para funcionar adecuadamente.

## Requisitos:

Python 3 (probado en 3.10.11): https://www.python.org/downloads/<br />
Selenium (se instala desde pip)<br />
Chromedriver <br />

## **Instalación**

Paso 1: Crear una carpeta en un directorio, descargar chromedriver y colocarlo en la misma carpeta donde se descargará el script

Paso 2: Ejecutar los pasos para descargar script e instalar requisitos:

```cmd
git clone https://github.com/dev-lang/nicar-consulta/
cd nicar-consulta
pip install -r requirements.txt
```

Paso 3: mover chromedriver a la carpeta

## **Ejecución**

El script posee actualmente dos modos de ejecución. 
Podrás ejecutar el script tanto con salida por consola como incluir el exportar los resultados a un archivo .csv

Antes de ejecutar debes crear un archivo con la lista de dominios a consultar (p.e: dominios.txt)

### Con exportación de .CSV:

⚠️ **Se creará por defecto un archivo llamado "resultados_dominios.csv" en el directorio del script**

```cmd
python3 nicar.py --archivo dominios.txt --csv
```

### Sin exportar a .CSV:

❌ **NO Se creará un archivo, la salida de resultados se dará exclusivamente en consola**

```cmd
python3 nicar.py --archivo dominios.txt
```

### Dominio único:

Se debe declarar el dominio único a revisar

```cmd
python3 nicar.py --dominio dominio.com.ar
```

### Dominio único (exportar a .csv):

Si se agrega el parámetro --csv, se guardará en un archivo .csv

```cmd
python3 nicar.py --dominio dominio.com.ar --csv
```

### Ayuda integrada:

Ofrece una ayuda rápida para saber como ejecutar el programa

```cmd
python3 nicar.py -h
```
