import csv
import time
import json

# Constantes para las conversiones
PULGADAS_A_CM = 2.54
LIBRAS_A_KG = 0.45

# Función para cargar los datos del archivo de origen
def cargar_datos(archivo_origen):
    with open(archivo_origen, 'r', encoding='UTF-8') as archivo:
        reader = csv.reader(archivo)
        cabecera = next(reader)
        datos = list(reader)
    return cabecera, datos

# Función para traducir nombres de columnas y datos
def traducir_nombres_y_datos(cabecera, datos):
    traducciones = {
        'Name': 'Nom',
        'Team': 'Equip',
        'Position': 'Posició',
        'Heigth': 'Alçada',
        'Weigth': 'Pes',
        'Age': 'Edat'
    }

    traducciones_posiciones = {
        'Point Guard': 'Base',
        'Shooting Guard': 'Escorta',
        'Small Forward': 'Aler',
        'Power Forward': 'Ala-pivot',
        'Center': 'Pivot'
    }

    cabecera_traducida = [traducciones.get(nombre, nombre) for nombre in cabecera]

    for fila in datos:
        fila[cabecera.index('Position')] = traducciones_posiciones.get(fila[cabecera.index('Position')], fila[cabecera.index('Position')])
        fila[cabecera.index('Heigth')] = round(float(fila[cabecera.index('Heigth')]) * PULGADAS_A_CM, 2)
        fila[cabecera.index('Weigth')] = round(float(fila[cabecera.index('Weigth')]) * LIBRAS_A_KG, 2)
        fila[cabecera.index('Age')] = int(float(fila[cabecera.index('Age')]))

    return cabecera_traducida, datos

# Función para escribir los datos en el archivo de salida
def escribir_datos(archivo_salida, cabecera_traducida, datos_traducidos):
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo, delimiter='^')
        writer.writerow(cabecera_traducida)
        writer.writerows(datos_traducidos)

# Función para obtener estadísticas
def obtener_estadisticas(datos, cabecera):
    indice_nombre, indice_peso, indice_altura, indice_posicion, indice_edad = [cabecera.index(columna) for columna in ['Nom', 'Pes', 'Alçada', 'Posició', 'Edat']]

    jugador_peso_mas_alto = max(datos, key=lambda x: float(x[indice_peso]))
    nombre_peso_mas_alto, peso_mas_alto = jugador_peso_mas_alto[indice_nombre], float(jugador_peso_mas_alto[indice_peso])

    jugador_altura_mas_pequena = min(datos, key=lambda x: float(x[indice_altura]))
    nombre_altura_mas_pequena, altura_mas_pequena = jugador_altura_mas_pequena[indice_nombre], float(jugador_altura_mas_pequena[indice_altura])

    estadisticas_por_posicion_y_equipo, conteo_posiciones, distribucion_edades = {}, {}, {}

    for fila in datos:
        posicion, equipo, peso, altura, edad = [fila[indice] for indice in [indice_posicion, indice_nombre, indice_peso, indice_altura, indice_edad]]

        # Estadísticas por posición y equipo
        if posicion not in estadisticas_por_posicion_y_equipo:
            estadisticas_por_posicion_y_equipo[posicion] = {}
        
        if equipo not in estadisticas_por_posicion_y_equipo[posicion]:
            estadisticas_por_posicion_y_equipo[posicion][equipo] = {'peso_total': 0, 'altura_total': 0, 'cantidad_jugadores': 0}
        
        estadisticas_por_posicion_y_equipo[posicion][equipo]['peso_total'] += peso
        estadisticas_por_posicion_y_equipo[posicion][equipo]['altura_total'] += altura
        estadisticas_por_posicion_y_equipo[posicion][equipo]['cantidad_jugadores'] += 1

        # Conteo de posiciones
        conteo_posiciones[posicion] = conteo_posiciones.get(posicion, 0) + 1

        # Distribución por edades
        distribucion_edades[edad] = distribucion_edades.get(edad, 0) + 1

    for pos, equipos in estadisticas_por_posicion_y_equipo.items():
        for equipo, stats in equipos.items():
            stats['peso_promedio'] = stats['peso_total'] / stats['cantidad_jugadores']
            stats['altura_promedio'] = stats['altura_total'] / stats['cantidad_jugadores']

    return nombre_peso_mas_alto, peso_mas_alto, nombre_altura_mas_pequena, altura_mas_pequena, estadisticas_por_posicion_y_equipo, conteo_posiciones, distribucion_edades



# Función para mostrar estadísticas
def mostrar_estadisticas(nombre_peso_mas_alto, peso_mas_alto, nombre_altura_mas_pequena, altura_mas_pequena, estadisticas_por_posicion_y_equipo, conteo_posiciones, distribucion_edades):
    print("a) Nom del jugador amb el pes més alt:")
    print(f"Nom: {nombre_peso_mas_alto}, Pes: {peso_mas_alto} kg")

    print("\nMostrant les estadístiques en 5 segons...")
    time.sleep(5)

    print("\nb) Nom del jugador amb l'alçada més petita:")
    print(f"Nom: {nombre_altura_mas_pequena}, Alçada: {altura_mas_pequena} cm")

    print("\nMostrant les estadístiques en 5 segons...")
    time.sleep(5)

    print("\nc) Estadísticas de pes i alçada per posició i equip:")
    for posicion, equipos in estadisticas_por_posicion_y_equipo.items():
        for equipo, datos in equipos.items():
            print(f"Posició: {posicion}, Equip: {equipo}")
            print(f"Mitjana de Pes: {datos['peso_promedio']} kg")
            print(f"Mitjana d'Alçada: {datos['altura_promedio']} cm")
            print("-" * 30)

    print("\nMostrant les estadístiques en 5 segons...")
    time.sleep(5)

    print("\nd) Recompte de jugadors per posició:")
    for posicion, cantidad in conteo_posiciones.items():
        print(f"{posicion}: {cantidad} jugadors")

    print("\nMostrant les estadístiques en 5 segons...")
    time.sleep(5)

    print("\ne) Distribució de jugadors per edat:")
    for edad, cantidad in distribucion_edades.items():
        print(f"Edat {edad}: {cantidad} jugadors")




# Función para convertir CSV a JSON

def csv_to_json(csv_file, json_file):
    # Lista para almacenar los datos
    datos = []

    # Leer el archivo CSV
    with open(csv_file, 'r', encoding='utf-8') as archivo:
        reader = csv.reader(archivo, delimiter='^')
        cabecera = next(reader)
        for fila in reader:
            datos.append({
                cabecera[0]: fila[0],
                cabecera[1]: fila[1],
                cabecera[2]: fila[2],
                cabecera[3]: float(fila[3]),
                cabecera[4]: float(fila[4]),
                cabecera[5]: int(fila[5])
            })

    # Escribir los datos en un nuevo archivo JSON con ensure_ascii=False
    with open(json_file, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)










def main():
    # Archivos de entrada y salida
    archivo_origen = 'basket_players.csv'
    archivo_salida = 'new_basket_players.csv'
    archivo_json = 'new_basket_players.json'

    # Cargar datos y traducir nombres y datos
    cabecera, datos = cargar_datos(archivo_origen)
    cabecera_traducida, datos_traducidos = traducir_nombres_y_datos(cabecera, datos)

    # Escribir datos en el archivo de salida
    escribir_datos(archivo_salida, cabecera_traducida, datos_traducidos)

    # Obtener estadísticas
    nombre_peso_mas_alto, peso_mas_alto, nombre_altura_mas_pequena, altura_mas_pequena, estadisticas_por_posicion_y_equipo, conteo_posiciones, distribucion_edades = obtener_estadisticas(datos_traducidos, cabecera_traducida)

    # Mostrar estadísticas
    mostrar_estadisticas(nombre_peso_mas_alto, peso_mas_alto, nombre_altura_mas_pequena, altura_mas_pequena, estadisticas_por_posicion_y_equipo, conteo_posiciones, distribucion_edades)

    # Conversión de CSV a JSON
    csv_to_json(archivo_salida, archivo_json)

    print('Datos traducidos y estadísticas calculadas correctamente.')

if __name__ == "__main__":
    main()