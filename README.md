# NIC.AR - consulta de dominios

![Static Badge](https://img.shields.io/badge/3-blue?style=plastic&label=Python&color=blue) ![Static Badge](https://img.shields.io/badge/selenium-blue?style=plastic&color=blue)


Script para hacer consulta de dominios en nic.ar

El script permite consultar a través del sitio nic.ar la disponibilidad de varios dominios de forma secuencial, 
tambien es válido si se define un único dominio. El script utiliza Selenium para consultar la disponibilidad de dominios en nic.ar y obtener información de los registros. <br>
Selenium Manager permite gestionar automáticamente ChromeDriver en las versiones compatibles de Selenium.

## Requisitos

- Python 3 (probado en Python 3.13.12): https://www.python.org/downloads/
- Selenium 4.21.0.
- Google Chrome instalado.

## Instalación

Clonar el repositorio e instalar las dependencias:

```bash
git clone https://github.com/dev-lang/nicar-consulta/
cd nicar-consulta
python -m pip install -r requirements.txt
```

Selenium 4.21.0 incluye Selenium Manager, que puede detectar, descargar y configurar automáticamente una versión compatible de ChromeDriver cuando sea necesario. <br>
En una instalación estándar, no es necesario descargarlo ni configurarlo manualmente.

Para que la descarga automática funcione cuando sea necesaria, Selenium Manager debe poder acceder a Internet.

## **Ejecución**

El script posee actualmente dos modos de ejecución. 
Podrás ejecutar el script tanto con salida por consola como incluir el exportar los resultados a un archivo .csv

Nota: si no se utiliza el parámetro --output, el nombre de archivo tomará por defecto el nombre hardcodeado (incluye fecha y hora de creacion)

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

### Nombre de archivo personalizado

Permite la creación del archivo CSV con un nombre personalizado (funciona tanto con dominio como con archivo)

```cmd
python3 nicar.py --dominio dominio.com.ar --csv --output consulta.csv
```

### Ayuda integrada:

Ofrece una ayuda rápida para saber como ejecutar el programa

```cmd
python3 nicar.py -h
```
