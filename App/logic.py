import time
import time
from DataStructures import map_separate_chaining as msc
from DataStructures import array_list as al

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    pass


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    pass

# Funciones de consulta sobre el catálogo


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
