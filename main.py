# =====================================================================
#  Caso 3 - Sistema de monitoreo de consumo energético en pequeños
#           comercios.
#
#  Restricciones respetadas:
#    - Sin clases, archivos, BD, librerías externas ni módulos estadísticos.
#    - Solo funciones, ciclos, condicionales, listas, diccionarios,
#      variables y operadores básicos.
#    - La suma (promedio) se resuelve MANUALMENTE con un ciclo.
#    - No se usan sum(), max(), min() ni sorted().
#    - Las 6 funciones se invocan en la ejecución principal (main).
# =====================================================================


# ---------------------------------------------------------------------
# 1) registrar_comercio()
#    Fiel al flujo: maneja el ciclo COMPLETO y retorna la lista de
#    comercios. Cada comercio es un diccionario con una lista 'consumos'
#    vacía que se llenará más adelante.
# ---------------------------------------------------------------------
def registrar_comercio():
    """
    Entrada:  la cantidad de comercios (la pide al usuario).
    Salida:   lista de diccionarios (comercios), aún SIN consumos.
    """
    comercios = []  # lista acumuladora: es la salida de la función

    cantidad = int(input("¿Cuántos comercios desea registrar? "))

    # Ciclo For según el # de comercios (paso 1 del flujo)
    for i in range(cantidad):
        print("\n--- Registro del comercio", i + 1, "---")

        # Construimos el diccionario de UN comercio (pasos 2 y 3 del flujo).
        # La clave 'consumos' arranca como lista vacía y se llena aparte:
        # así los datos viven DENTRO del dict y no como variables sueltas
        # (evitamos "atarnos al scope local", como anotaste en el flujo).
        comercio = {
            "nit":          input("NIT: "),
            "nombre":       input("Nombre: "),
            "tipo":         input("Tipo: "),
            "empleados":    int(input("N° de empleados: ")),
            "meta_semanal": float(input("Meta semanal de consumo: ")),
            "consumos":     []   # se poblará en registrar_consumo()
        }

        comercios.append(comercio)  # agregamos el dict a la lista (paso 4)

    return comercios


# ---------------------------------------------------------------------
# 2) registrar_consumo(comercio)
#    Segundo ciclo (SEPARADO, no anidado dentro del anterior). Registra
#    los 4 consumos semanales de UN comercio, validando que sean > 0.
#    Esa validación protege la división por cero de calcular_variacion().
# ---------------------------------------------------------------------
def registrar_consumo(comercio):
    """
    Entrada:  un comercio (diccionario) con su lista 'consumos' vacía.
    Salida:   la lista con los 4 consumos (además el dict queda mutado).
    """
    semanas = 4  # el caso trabaja con 4 semanas fijas

    print("\nConsumos semanales de:", comercio["nombre"])

    for i in range(semanas):
        consumo = 0  # valor inicial que NO pasa la validación (> 0)

        # Repetimos la lectura hasta obtener un consumo válido (> 0).
        # 'while' se ejecuta al menos una vez porque consumo empieza en 0.
        while consumo <= 0:
            consumo = float(input("  Consumo semana " + str(i + 1) + " (> 0): "))
            if consumo <= 0:
                print("  * El consumo debe ser mayor a cero. Intente de nuevo.")

        # Almacenamos en la posición i de la lista (paso 4 del flujo).
        # Como la lista arranca vacía y recorremos i = 0,1,2,3 en orden,
        # append() deja cada valor exactamente en su posición.
        comercio["consumos"].append(consumo)
        

    return comercio["consumos"]


# ---------------------------------------------------------------------
# 3) calcular_promedio(consumos)
#    Suma MANUAL con ciclo y división entre la cantidad de semanas.
#    No usamos sum(). Contamos los elementos a mano para no depender
#    de len() en el cálculo central.
# ---------------------------------------------------------------------
def calcular_promedio(consumos):
    """
    Entrada:  lista de consumos.
    Salida:   promedio (número). Se RETORNA; la impresión vive en el informe.
    """
    acumulado = 0  # aquí sumamos manualmente cada valor (paso 1)
    cantidad = 0   # contamos los elementos a mano

    for consumo in consumos:
        acumulado = acumulado + consumo  # sumatoria manual
        cantidad = cantidad + 1

    promedio = acumulado / cantidad  # dividimos la sumatoria entre la cantidad (paso 2)
    return promedio                  # (paso 3) devolvemos el resultado


# ---------------------------------------------------------------------
# 4) calcular_variacion(consumos)
#    Variación porcentual entre la primera y la última semana.
#    Fórmula:  (Semana[3] - Semana[0]) / Semana[0] * 100
#    Se conserva el SIGNO: negativo = el consumo bajó respecto a la semana 1.
# ---------------------------------------------------------------------
def calcular_variacion(consumos):
    """
    Entrada:  lista de consumos (4 semanas).
    Salida:   variación en porcentaje (número, con signo).
    """
    semana_inicial = consumos[0]  # Semana[0]
    semana_final = consumos[3]    # Semana[3] (el caso es de 4 semanas fijas)

    # (final - inicial) / inicial  -> proporción de cambio
    # * 100                        -> lo expresamos en porcentaje
    variacion = (semana_final - semana_inicial) / semana_inicial * 100
    return variacion


# ---------------------------------------------------------------------
# 5) clasificar_consumo(promedio, meta, variacion)
#    Función PURA: recibe valores ya calculados y solo retorna la etiqueta.
#    Reglas:
#      - Eficiente:      promedio <= meta y variacion <= 5
#      - En observación: promedio <= meta y variacion > 5
#      - Alto:           promedio > meta y exceso <= 20
#      - Crítico:        promedio > meta y exceso > 20
#    (exceso = cuánto supera el promedio a la meta, en %)
# ---------------------------------------------------------------------
def clasificar_consumo(promedio, meta, variacion):
    """
    Entrada:  promedio, meta y variacion (números).
    Salida:   la clasificación (str).
    """
    if promedio <= meta:
        # Dentro de la meta: distinguimos por estabilidad (la variación).
        if variacion <= 5:
            return "Eficiente"
        else:
            return "En observación"
    else:
        # Supera la meta: medimos EN CUÁNTO la supera, en porcentaje.
        exceso = (promedio - meta) / meta * 100
        if exceso <= 20:
            return "Alto"
        else:
            return "Crítico"


# ---------------------------------------------------------------------
# 6) generar_informe(comercios)
#    Recorre los comercios ya procesados (con promedio, variación y
#    clasificación persistidos en cada dict), imprime el detalle y
#    agrupa los nombres en 4 listas según su clasificación.
# ---------------------------------------------------------------------
def generar_informe(comercios):
    """
    Entrada:  lista de comercios ya procesados.
    Salida:   diccionario con las 4 listas de clasificados (y lo imprime).
    """
    # Cuatro listas vacías, una por categoría (paso 3 del flujo).
    clasificados = {
        "Eficiente":      [],
        "En observación": [],
        "Alto":           [],
        "Crítico":        []
    }

    print("\n==================== INFORME DE CONSUMO ====================")

    # Ciclo según el # de comercios.
    for comercio in comercios:
        # Pasos 1 y 2: extraemos del diccionario los datos ya calculados.
        nombre        = comercio["nombre"]
        promedio      = comercio["promedio"]
        meta          = comercio["meta_semanal"]
        variacion     = comercio["variacion"]
        clasificacion = comercio["clasificacion"]

        # Detalle por comercio.
        print("\nComercio:", nombre)
        print("  Promedio de consumo:", promedio)
        print("  Meta semanal:       ", meta)
        print("  Variación:          ", variacion, "%")
        print("  Clasificación:      ", clasificacion)

        # Paso 3: agregamos el nombre a la lista de su clasificación.
        clasificados[clasificacion].append(nombre)

    # Resumen agrupado por categoría.
    print("\n-------------------- RESUMEN AGRUPADO ---------------------")
    for categoria in clasificados:
        print(categoria + ":", clasificados[categoria])
    print("===========================================================")

    return clasificados


# ---------------------------------------------------------------------
# Ejecución principal: aquí se INVOCAN las 6 funciones.
# ---------------------------------------------------------------------
def main():
    # 1) Registramos todos los comercios (ciclo completo dentro de la función).
    comercios = registrar_comercio()

    # 2) En un ciclo SEPARADO (no anidado) llenamos los consumos de cada uno.
    for comercio in comercios:
        registrar_consumo(comercio)

    # 3) Procesamos cada comercio y PERSISTIMOS los resultados en su dict.
    for comercio in comercios:
        consumos  = comercio["consumos"]
        promedio  = calcular_promedio(consumos)
        variacion = calcular_variacion(consumos)
        clasificacion = clasificar_consumo(promedio, comercio["meta_semanal"], variacion)

        comercio["promedio"]      = promedio
        comercio["variacion"]     = variacion
        comercio["clasificacion"] = clasificacion

    # 4) Generamos el informe final.
    generar_informe(comercios)


# Punto de entrada del programa.
if __name__ == "__main__":
    main()