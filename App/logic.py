import time
import csv
import os

from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll

import time
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.List import array_list as al

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        'ordenes': lt.new_list()
    }
    
    return catalog

def to_float(valor): # Tomado del reto anterior, que fue creado usando IAG
    """
    Convierte un texto a float. Si está vacío o no es válido, retorna None
    """
    if valor is not None and valor.strip() != "":
        return float(valor)
    return None

def to_int(valor): #Tomado del reto anterior, que fue creado usando IAG
    """
    Convierte un texto a int (pasando por float, por si viene como "148.0").
    Si está vacío o no es válido, retorna None
    """
    if valor is not None and valor.strip() != "":
        return int(float(valor))
    return None

# Funciones para la carga de datos
def convertir_fila(fila): #Tomada del reto anterior, que fue creada usando IAG
    """
    Convierte una fila del CSV (dict de strings) en un pedido con tipos correctos
    """
    order = {
        "Order_ID": fila.get("Order_ID") or "Unknown",
        "Product": fila.get("Product") or "Unknown",
        "Country": fila.get("Country") or "Unknown",
        "Channel": fila.get("Channel") or "Unknown",
        "Order_Date": fila.get("Order_Date") or "Unknown",
        "Discount_Pct": to_float(fila.get("Discount_Pct")),
        "Price_per_Box": to_float(fila.get("Price_per_Box")),
        "Marketing_Spend": to_float(fila.get("Marketing_Spend")),
        "Boxes_Shipped": to_int(fila.get("Boxes_Shipped")),
        "Amount": to_float(fila.get("Amount")),
    }

    return order
def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    ruta = os.path.join("Data", filename)

    with open(ruta, encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            pedido = convertir_fila(fila)
            lt.add_last(catalog["ordenes"], pedido)

    return catalog

# Funciones de consulta sobre el catálogo

def resumen_carga(catalog): # Tomado del reto anterior, que fue creado utilizando IAG
    """
    Calcula las estadísticas que pide la Parte 2 sobre los datos ya cargados
    """
    pedidos = catalog["ordenes"]
    total = lt.size(pedidos)

    menor = lt.get_element(pedidos, 0)
    mayor = lt.get_element(pedidos, 0)

    for i in range(total):
        actual = lt.get_element(pedidos, i)

        if actual["Amount"] > mayor["Amount"] or (actual["Amount"] == mayor["Amount"] and actual["Price_per_Box"] < mayor["Price_per_Box"]):
            mayor = actual

        if actual["Amount"] < menor["Amount"] or (actual["Amount"] == menor["Amount"] and actual["Price_per_Box"] < menor["Price_per_Box"]):
            menor = actual

    primeros_5 = []
    cantidad_primeros = min(5, total)
    for i in range(cantidad_primeros):
        primeros_5.append(lt.get_element(pedidos, i))

    ultimos_5 = []
    inicio_ultimos = max(0, total - 5)
    for i in range(inicio_ultimos, total):
        ultimos_5.append(lt.get_element(pedidos, i))

    return {
        "total": total,
        "menor": menor,
        "mayor": mayor,
        "primeros_5": primeros_5,
        "ultimos_5": ultimos_5,
    }

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog, fecha, min_amount, max_amount):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    inicio=get_time()
    pedidos_fecha = msc.get(catalog["pedidos_por_fecha"], fecha)
    if pedidos_fecha is None:
        print("No hay pedidos en esa fecha.")
        return None
    filtrados = al.new_list()
    for pedido in pedidos_fecha["elements"]:
        if min_amount <= pedido["Amount"] <= max_amount:
            al.add_last(filtrados, pedido)
    total_amount=0
    total_marketing=0
    for p in filtrados["elements"]:
        total_amount+=p["Amount"]
        total_marketing+=p["Marketing_Spend"]
    
    total_aporte=total_amount-total_marketing
    def cmp_amount(p1, p2):
        if p1["Amount"] > p2["Amount"]:
            return True
        elif p1["Amount"] == p2["Amount"]:
            aporte1 = p1["Amount"] - p1["Marketing_Spend"]
            aporte2 = p2["Amount"] - p2["Marketing_Spend"]
            if aporte1 > aporte2:
                return True
            elif aporte1 == aporte2:
                return p1["Order_ID"] < p2["Order_ID"]
        return False
    sorted_list = al.merge_sort(filtrados, cmp_amount, "descendente")

    if al.size(sorted_list) > 20:
        resultado = al.sub_list(sorted_list, 1, 10)
        ultimos = al.sub_list(sorted_list, al.size(sorted_list) - 9, 10)
        for p in ultimos["elements"]:
            al.add_last(resultado, p)
    else:
        resultado = sorted_list
    fin=get_time()
    tiempo=delta_time(inicio,fin)
    print(f"Tiempo de ejecución: {tiempo} ms")
    print(f"Número de pedidos filtrados: {al.size(sorted_list)}")
    print(f"Monto total recaudado: {total_amount}")
    print(f"Total Marketing Spend: {total_marketing}")
    print(f"Total Aporte Comercial: {total_aporte}\n")

    for p in resultado["elements"]:
        aporte = p["Amount"] - p["Marketing_Spend"]
        print(p["Order_ID"], p["Product"], p["Country"], p["Order_Date"],
              "Marketing:", p["Marketing_Spend"], "Boxes:", p["Boxes_Shipped"],
              "Amount:", p["Amount"], "Aporte:", aporte)
def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
