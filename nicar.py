import csv
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime

def buscar_dominio(driver, dominio, zona):
    try:
        # Navegar a la página de búsqueda de dominios
        driver.get("https://nic.ar/es")

        # Esperar a que el campo de búsqueda esté presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "edit-txtbuscar"))
        )

        # Ingresar el dominio en el campo de búsqueda
        input_dominio = driver.find_element(By.ID, "edit-txtbuscar")
        input_dominio.clear()  # Limpiar el campo antes de escribir
        input_dominio.send_keys(dominio)

        # Seleccionar la zona del dominio
        select_zona = Select(driver.find_element(By.ID, "cmbZonas"))
        select_zona.select_by_value(zona)

        # Hacer scroll para asegurarse de que el botón esté visible
        boton_buscar = driver.find_element(By.ID, "btn-consultar-block-submit")
        ActionChains(driver).move_to_element(boton_buscar).perform()

        # Esperar un momento antes de hacer clic
        time.sleep(1)

        # Hacer clic en el botón de búsqueda
        boton_buscar.click()

        # Esperar a que se cargue la página de resultados
        time.sleep(5)

        # Obtener el contenido de la página de resultados
        resultado = driver.page_source

        # Verificar si el dominio está disponible
        if "El dominio está disponible para registrarlo" in resultado:
            return {"dominio": f"{dominio}{zona}", "estado": "Disponible", "datos": {}}
        elif "El dominio no está disponible para registrarlo" in resultado:
            datos_dominio = {}
            tabla = driver.find_element(By.CLASS_NAME, "table")
            filas = tabla.find_elements(By.TAG_NAME, "tr")
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, "td")
                if len(celdas) == 1:
                    texto = celdas[0].text.strip()
                    if ':' in texto:
                        clave, valor = texto.split(':', 1)
                        datos_dominio[clave.strip()] = valor.strip()
            return {"dominio": f"{dominio}{zona}", "estado": "No disponible", "datos": datos_dominio}
        else:
            return {"dominio": f"{dominio}{zona}", "estado": "Error", "datos": {}}
    except Exception as e:
        return {"dominio": f"{dominio}{zona}", "estado": f"Error: {e}", "datos": {}}

def leer_dominios_desde_archivo(ruta_archivo):
    dominios = []
    zonas_compuestas = [".com.ar", ".net.ar", ".gob.ar", ".int.ar", ".mil.ar", ".musica.ar", ".org.ar", ".tur.ar", ".seg.ar", ".senasa.ar", ".coop.ar", ".mutual.ar", ".bet.ar"]
    
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            dominio_completo = linea.strip()
            if dominio_completo:
                zona_encontrada = None
                for zona in zonas_compuestas:
                    if dominio_completo.endswith(zona):
                        zona_encontrada = zona
                        break
                
                if zona_encontrada:
                    nombre = dominio_completo[:-len(zona_encontrada)]
                    zona = zona_encontrada
                elif dominio_completo.endswith(".ar"):
                    nombre = dominio_completo[:-len(".ar")]
                    zona = ".ar"
                else:
                    print(f"Error: El dominio {dominio_completo} no tiene una zona válida.")
                    continue
                
                dominios.append({"nombre": nombre, "zona": zona})
    return dominios

def procesar_dominio(dominio_completo):
    zonas_compuestas = [".com.ar", ".net.ar", ".gob.ar", ".int.ar", ".mil.ar", ".musica.ar", ".org.ar", ".tur.ar", ".seg.ar", ".senasa.ar", ".coop.ar", ".mutual.ar", ".bet.ar"]
    
    if dominio_completo:
        zona_encontrada = None
        for zona in zonas_compuestas:
            if dominio_completo.endswith(zona):
                zona_encontrada = zona
                break
        
        if zona_encontrada:
            nombre = dominio_completo[:-len(zona_encontrada)]
            zona = zona_encontrada
        elif dominio_completo.endswith(".ar"):
            nombre = dominio_completo[:-len(".ar")]
            zona = ".ar"
        else:
            print(f"Error: El dominio {dominio_completo} no tiene una zona válida.")
            return None
        
        return {"nombre": nombre, "zona": zona}
    return None

def generar_nombre_csv():
    # Generar un nombre de archivo con la fecha y hora actual
    fecha_actual = datetime.now().strftime("%m%d%Y%H%M%S")
    return f"resultados-dominios_{fecha_actual}.csv"

def main(archivo_dominios, dominio_unico, generar_csv, nombre_csv):
    # Configurar el navegador
    driver = webdriver.Chrome()  # Asegúrate de tener ChromeDriver instalado

    # Abrir un archivo CSV para guardar los resultados (si se especifica el parámetro --csv)
    if generar_csv:
        if not nombre_csv:
            nombre_csv = generar_nombre_csv()
        csv_file = open(nombre_csv, mode="w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Dominio", "Estado", "Nombre y Apellido", "CUIT/CUIL/ID", "Fecha de Alta", "Fecha de vencimiento"])

    try:
        if dominio_unico:
            # Modo dominio único
            dominio_info = procesar_dominio(dominio_unico)
            if dominio_info:
                nombre_dominio = dominio_info["nombre"]
                zona = dominio_info["zona"]
                resultado = buscar_dominio(driver, nombre_dominio, zona)
                print(f"Resultado para {resultado['dominio']}: {resultado['estado']}")
                if resultado["estado"] == "No disponible":
                    print("Datos del dominio:")
                    for clave, valor in resultado["datos"].items():
                        print(f"{clave}: {valor}")
                    if generar_csv:
                        csv_writer.writerow([
                            resultado["dominio"],
                            resultado["estado"],
                            resultado["datos"].get("Nombre y Apellido", ""),
                            resultado["datos"].get("CUIT/CUIL/ID", ""),
                            resultado["datos"].get("Fecha de Alta", ""),
                            resultado["datos"].get("Fecha de vencimiento", "")
                        ])
                else:
                    if generar_csv:
                        csv_writer.writerow([resultado["dominio"], resultado["estado"], "", "", "", ""])
                print("-" * 50)
        else:
            # Modo archivo
            dominios = leer_dominios_desde_archivo(archivo_dominios)
            for dominio_info in dominios:
                nombre_dominio = dominio_info["nombre"]
                zona = dominio_info["zona"]
                resultado = buscar_dominio(driver, nombre_dominio, zona)
                print(f"Resultado para {resultado['dominio']}: {resultado['estado']}")
                if resultado["estado"] == "No disponible":
                    print("Datos del dominio:")
                    for clave, valor in resultado["datos"].items():
                        print(f"{clave}: {valor}")
                    if generar_csv:
                        csv_writer.writerow([
                            resultado["dominio"],
                            resultado["estado"],
                            resultado["datos"].get("Nombre y Apellido", ""),
                            resultado["datos"].get("CUIT/CUIL/ID", ""),
                            resultado["datos"].get("Fecha de Alta", ""),
                            resultado["datos"].get("Fecha de vencimiento", "")
                        ])
                else:
                    if generar_csv:
                        csv_writer.writerow([resultado["dominio"], resultado["estado"], "", "", "", ""])
                print("-" * 50)
    finally:
        driver.quit()
        if generar_csv:
            csv_file.close()
            print(f"Resultados guardados en '{nombre_csv}'.")

if __name__ == "__main__":
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Buscar disponibilidad de dominios en NIC Argentina.")
    parser.add_argument("--archivo", help="Ruta del archivo de texto con la lista de dominios.")
    parser.add_argument("--dominio", help="Buscar un solo dominio (ejemplo: dominio.com.ar).")
    parser.add_argument("--csv", action="store_true", help="Generar un archivo CSV con los resultados.")
    parser.add_argument("--output", help="Nombre personalizado para el archivo CSV.")
    args = parser.parse_args()

    # Validar argumentos
    if not args.archivo and not args.dominio:
        parser.error("Debes proporcionar un archivo de dominios (--archivo) o un dominio único (--dominio).")

    # Ejecutar la función principal
    main(args.archivo, args.dominio, args.csv, args.output)
