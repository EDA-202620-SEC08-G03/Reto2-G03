import time
import csv
import os

from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.List import array_list as al

csv.field_size_limit(2147483647)
default_limit = 1000

def cmp_comparacion_amount(dato1, dato2):
    if dato1["Amount"] != dato2["Amount"]:
        return dato1["Amount"] > dato2["Amount"]
    return dato1["Order_ID"] < dato2["Order_ID"]


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """ 
    catalog = {
        'ordenes': lt.new_list(),
        'canales': msc.new_map(10, 0.5),
        "pedidos_por_fecha": msc.new_map(10, 0.5),
        'pedidos_por_pais': msc.new_map(10, 0.5),
        "productos":msc.new_map(10,0.5),
        'fecha_min': None,
        'fecha_max': None,
        'pedidos_por_mes': mlp.new_map(10, 0.5),
        'pedidos_por_producto_pais': mlp.new_map(10, 0.5)
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
            if pedido["Amount"] is not None:
                lt.add_last(catalog["ordenes"], pedido)
                
                canal = pedido["Channel"]
                cuenta = msc.get(catalog["canales"], canal)
                if cuenta is None:
                    msc.put(catalog["canales"], canal, 1)
                else:
                    msc.put(catalog["canales"], canal, cuenta + 1)

                    
                pais = pedido["Country"]
                lista_pais = msc.get(catalog["pedidos_por_pais"], pais)
                if lista_pais is None:
                    lista_pais = lt.new_list()
                    msc.put(catalog["pedidos_por_pais"], pais, lista_pais)
                lt.add_last(lista_pais, pedido)
                
                fecha = pedido["Order_Date"]
                lista_fecha = msc.get(catalog["pedidos_por_fecha"], fecha)
                if lista_fecha is None:
                    lista_fecha = lt.new_list()
                    msc.put(catalog["pedidos_por_fecha"], fecha, lista_fecha)
                lt.add_last(lista_fecha, pedido)
                
                
                producto=pedido["Product"]
                lista_pedidos = msc.get(catalog["productos"],producto)
                if lista_pedidos is None:
                    lista_pedidos = lt.new_list()
                    msc.put(catalog["productos"],producto,lista_pedidos)
                
                lt.add_last(lista_pedidos,pedido)
                
                mes = fecha[:7]
                lista_mes = mlp.get(catalog["pedidos_por_mes"], mes)
                if lista_mes is None:
                    lista_mes = lt.new_list()
                    mlp.put(catalog["pedidos_por_mes"], mes, lista_mes)
                lt.add_last(lista_mes, pedido)

                clave_pp = producto + "|" + pais
                lista_pp = mlp.get(catalog["pedidos_por_producto_pais"], clave_pp)
                if lista_pp is None:
                    lista_pp = lt.new_list()
                    mlp.put(catalog["pedidos_por_producto_pais"], clave_pp, lista_pp)
                lt.add_last(lista_pp, pedido)
                
                if catalog["fecha_min"] is None or fecha < catalog["fecha_min"]:
                    catalog["fecha_min"] = fecha
                if catalog["fecha_max"] is None or fecha > catalog["fecha_max"]:
                    catalog["fecha_max"] = fecha


    return catalog

# Funciones de consulta sobre el catálogo

def resumen_carga(catalog): # Tomado y modificado con respecto al reto anterior, donde fue creado utilizando IAG
    """
    Calcula las estadísticas que pide la Parte 2 sobre los datos ya cargados
    """
    pedidos = catalog["ordenes"]
    total = lt.size(pedidos)

    ordenados = lt.merge_sort(pedidos, cmp_comparacion_amount)
    n = min(5, total)

    canales = []
    claves = msc.key_set(catalog["canales"])
    for i in range(lt.size(claves)):
        clave = lt.get_element(claves, i)
        canales.append([clave, msc.get(catalog["canales"], clave)])

    return {
        "total": total,
        "canales": canales,
        "fecha_min": catalog["fecha_min"],
        "fecha_max": catalog["fecha_max"],
        "mayor": lt.first_element(ordenados),
        "menor": lt.last_element(ordenados),
        "primeros_5": lt.sub_list(ordenados, 0, n)["elements"],
        "ultimos_5": lt.sub_list(ordenados, total - n, n)["elements"],
    }

def cmp_req1(e1, e2):
    if e1["Discount_Pct"] != e2["Discount_Pct"]:
        return e1["Discount_Pct"] > e2["Discount_Pct"]
    elif e1["Amount"] != e2["Amount"]:
        return e1["Amount"] > e2["Amount"]
    else:
        return e1["Order_ID"] < e2["Order_ID"]

def req_1(catalog, anio, mes, descuento_min, descuento_max):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    
    tiempo_inicial = get_time()
    mes_int = int(mes)
    if mes_int < 10:
        clave_mes = str(anio) + "-0" + str(mes_int)
    else:
        clave_mes = str(anio) + "-" + str(mes_int)
    pedidos = mlp.get(catalog["pedidos_por_mes"], clave_mes)
    
    filtrados = lt.new_list()
    total_amount = 0
    
    if pedidos != None:
        tamaño_lista = lt.size(pedidos)
        for i in range(tamaño_lista):
            pedido = lt.get_element(pedidos, i)
            descuento = pedido["Discount_Pct"]
            if descuento != None and descuento_min <= descuento <= descuento_max:
                lt.add_last(filtrados, pedido)
                total_amount += pedido["Amount"]
    
    resultado = {
        "total" : lt.size(filtrados),
        "total_amount" : total_amount,
        "promedio_price_per_box" : 0,
        "promedio_boxes_shipped" : 0
    }
    
    total_price = 0
    total_boxes = 0                    
    
    for i in range(lt.size(filtrados)):
        pedido = lt.get_element(filtrados, i)
        if pedido["Price_per_Box"] != None:
            total_price += pedido["Price_per_Box"]
        if pedido["Boxes_Shipped"] != None:
            total_boxes += pedido["Boxes_Shipped"]
            
    if lt.size(filtrados) > 0:
        resultado["promedio_price_per_box"] = total_price / lt.size(filtrados) 
        resultado["promedio_boxes_shipped"] = total_boxes / lt.size(filtrados)
        
    ordenados = lt.merge_sort(filtrados, cmp_req1)
    if lt.size(ordenados) > 20:
        resultado["primeros_10"] = lt.sub_list(ordenados, 0, 10)["elements"]
        resultado["ultimos_10"] = lt.sub_list(ordenados, lt.size(ordenados) - 10, 10)["elements"]
    else:
        resultado["lista"] = ordenados["elements"]
    
    tiempo_final = get_time()
    resultado["tiempo"] = delta_time(tiempo_inicial, tiempo_final)
    
    return resultado
    

def comparacion_req2 (e1, e2):
    if e1["Boxes_Shipped"] != e2["Boxes_Shipped"]:
        return e1["Boxes_Shipped"] < e2["Boxes_Shipped"]
    if e1["Order_Date"] != e2["Order_Date"]:
        return e1["Order_Date"] > e2["Order_Date"]
    return e1["Order_ID"] < e2["Order_ID"]

def req_2(catalog, pais, min_cajas, max_cajas):
    """
    Retorna el resultado del requerimiento 2
    """
    tiempoinicial = get_time()
    
    lista_pais = msc.get(catalog["pedidos_por_pais"], pais)
    filtrados = lt.new_list()
    conteo_productos = msc.new_map(10, 0.5)
    suma_marketing = 0
    suma_amount = 0
    
    if lista_pais is not None:
        for i in range(lt.size(lista_pais)):
            producto = lt.get_element(lista_pais, i)
            cajas = producto["Boxes_Shipped"]
            if cajas is not None and (min_cajas <= cajas and cajas <= max_cajas):
                lt.add_last(filtrados, producto)
                suma_marketing += producto["Marketing_Spend"]
                suma_amount += producto["Amount"]
                c = msc.get(conteo_productos, producto["Product"])
                if c is None:
                    msc.put(conteo_productos, producto["Product"], 1)
                else:
                    msc.put(conteo_productos, producto["Product"], c + 1)
                
    totalfiltrados = lt.size(filtrados)
    resultado = {
        "total": totalfiltrados,
        "n_productos": 0,
        "promedio_marketing": 0,
        "promedio_amount": 0,
        "producto_top": None,
        "pedidos_top": 0,
        "lista": lt.new_list()
    }
    if totalfiltrados > 0:
        claves = msc.key_set(conteo_productos)
        resultado["n_productos"] = lt.size(claves)
        
        mejor = None
        mejor_cuenta = 0
        for i in range(lt.size(claves)):
            producto2 = lt.get_element(claves, i)
            cuenta = msc.get(conteo_productos, producto2)
            if cuenta > mejor_cuenta or (cuenta == mejor_cuenta and producto2 < mejor):
                mejor = producto2
                mejor_cuenta = cuenta
        
        resultado["producto_top"] = mejor
        resultado["pedidos_top"] = mejor_cuenta
        resultado["promedio_marketing"] = suma_marketing / totalfiltrados
        resultado["promedio_amount"] = suma_amount / totalfiltrados
        
        ordenados = lt.merge_sort(filtrados, comparacion_req2)
        if totalfiltrados > 20:
            salida = lt.new_list()
            for i in range(10):
                lt.add_last(salida, lt.get_element(ordenados, i))
            for i in range(totalfiltrados - 10, totalfiltrados):
                lt.add_last(salida, lt.get_element(ordenados, i))
            resultado["lista"] = salida
        else:
            resultado["lista"] = ordenados
            
    tiempofinal = get_time()
    resultado["tiempo"] = delta_time(tiempoinicial, tiempofinal)
    return resultado

def cmp_req3(p1, p2):
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
def req_3(catalog, fecha, min_amount, max_amount):
    """
    Retorna el resultado del requerimiento 3
    """
    inicio=get_time()
    filtrados = al.new_list()
    lista_pais = msc.get(catalog["pedidos_por_fecha"], fecha)
    
    
    i=0
    pedido = lt.get_element(lista_pais, i)
    while pedido is not None and i < lt.size(lista_pais):
        pedido = lt.get_element(lista_pais, i)
        if min_amount <= pedido["Amount"] <= max_amount:
            al.add_last(filtrados, pedido)
        
        i += 1
    if filtrados is None:
        print("No hay pedidos en esa fecha.")
        return None
    
    total_amount=0
    total_marketing=0
    for pedidos in filtrados["elements"]:
        total_amount+=pedidos["Amount"]
        total_marketing+=pedidos["Marketing_Spend"]
    
    total_aporte=total_amount-total_marketing
    sorted_list = al.merge_sort(filtrados, cmp_req3)

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

    for pedidos in resultado["elements"]:
        aporte = pedidos["Amount"] - pedidos["Marketing_Spend"]
        print(pedidos["Order_ID"], pedidos["Product"], pedidos["Country"], pedidos["Order_Date"],
              "Marketing:", pedidos["Marketing_Spend"], "Boxes:", pedidos["Boxes_Shipped"],
              "Amount:", pedidos["Amount"], "Aporte:", aporte)
        
def cmp_req4(p1, p2):
    if p1["Amount"] != p2["Amount"]:
        return p1["Amount"] > p2["Amount"]
    elif p1["Marketing_Spend"] != p2["Marketing_Spend"]:
        return p1["Marketing_Spend"] < p2["Marketing_Spend"]
    else: 
        return p1["Order_ID"] < p2["Order_ID"]

def req_4(catalog, producto, pais):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    
    tiempo_inicial = get_time()
    
    clave = producto + "|" + pais
    filtrados = mlp.get(catalog["pedidos_por_producto_pais"], clave)
    
    total = 0
    if filtrados != None:
        total = lt.size(filtrados)
    
    resultado = {
        "total" : total,
        "promedio_price_per_box" : 0,
        "promedio_discount_pct" : 0,
        "promedio_marketing_spend" : 0,
        "promedio_boxes_shipped" : 0
    }
    
    total_price = 0
    total_discount = 0
    total_marketing = 0
    total_boxes = 0
    
    if total > 0:
        for i in range(total):
            pedido = lt.get_element(filtrados, i)
            if pedido["Price_per_Box"] != None:
                total_price += pedido["Price_per_Box"]
            if pedido["Discount_Pct"] != None:
                total_discount += pedido["Discount_Pct"]
            if pedido["Marketing_Spend"] != None:
                total_marketing += pedido["Marketing_Spend"]
            if pedido["Boxes_Shipped"] != None:
                total_boxes += pedido["Boxes_Shipped"]
        
        resultado["promedio_price_per_box"] = total_price / total
        resultado["promedio_discount_pct"] = total_discount / total
        resultado["promedio_marketing_spend"] = total_marketing / total
        resultado["promedio_boxes_shipped"] = total_boxes / total
        
        ordenados = lt.merge_sort(filtrados, cmp_req4)
        resultado["dos_primeros"] = lt.sub_list(ordenados, 0, min(2, total))["elements"]
    
    tiempo_final = get_time()
    resultado["tiempo"] = delta_time(tiempo_inicial, tiempo_final)
    
    return resultado
    

def comparacion_req5 (e1, e2):
    if e1["recaudo"] != e2["recaudo"]:
        return e1["recaudo"] > e2["recaudo"]
    if e1["cajas"] != e2["cajas"]:
        return e1["cajas"] > e2["cajas"]
    return e1["producto"] < e2["producto"]

def req_5(catalog, n, pais, fecha_inicio, fecha_fin):
    """
    Retorna el resultado del requerimiento 5
    """
    tiempoinicio = get_time()
    
    lista_pais = msc.get(catalog["pedidos_por_pais"], pais)
    acumulados = msc.new_map(10, 0.5)
    total_pedidos = 0
    recaudo_total = 0
    
    if lista_pais is not None and fecha_inicio <= fecha_fin:
        for i in range(lt.size(lista_pais)):
            producto = lt.get_element(lista_pais, i)
            if fecha_inicio <= producto["Order_Date"] and producto["Order_Date"] <= fecha_fin:
                total_pedidos += 1
                recaudo_total += producto["Amount"]
                acum = msc.get(acumulados, producto["Product"])
                if acum is None:
                    acum = {
                        "producto": producto["Product"], 
                        "pedidos": 0,
                        "cajas": 0,
                        "recaudo": 0,
                        "suma_precio": 0,
                        "suma_descuento": 0,
                        "marketing": 0
                    }
                    msc.put(acumulados, producto["Product"], acum)
                acum["pedidos"] += 1
                acum["cajas"] += producto["Boxes_Shipped"]
                acum["recaudo"] += producto["Amount"]
                acum["suma_precio"] += producto["Price_per_Box"]
                acum["suma_descuento"] += producto["Discount_Pct"]
                acum["marketing"] += producto["Marketing_Spend"]
                
    claves = msc.key_set(acumulados)
    n_productos = lt.size(claves)
    
    lista_acum = lt.new_list()
    for i in range(n_productos):
        acum = msc.get(acumulados, lt.get_element(claves, i))
        acum["promedio_precio"] = acum["suma_precio"] / acum["pedidos"]
        acum["promedio_descuento"] = acum["suma_descuento"] / acum["pedidos"]
        lt.add_last(lista_acum, acum)
        
    ordenados = lt.merge_sort(lista_acum, comparacion_req5)
    top = lt.new_list()
    for i in range(min(n, n_productos)):
        lt.add_last(top, lt.get_element(ordenados, i))
        
    tiempofinal = get_time()
    return {
        "tiempo": delta_time(tiempoinicio, tiempofinal),
        "total_pedidos": total_pedidos,
        "n_productos": n_productos,
        "recaudo_total": recaudo_total,
        "top": top
    }
    
def cmp_req_6(p1, p2):
        if p1["Eficiencia"] > p2["Eficiencia"]:
            return True
        elif p1["Eficiencia"] == p2["Eficiencia"]:
            if p1["Amount_total"] > p2["Amount_total"]:
                return True
            elif p1["Amount_total"] == p2["Amount_total"]:
                return p1["Country"] < p2["Country"]
        return False

def req_6(catalog, producto, fecha_inicial, fecha_final, n):
    """
    Retorna el resultado del requerimiento 6
    """

    inicio = get_time()
    
    filtrados = al.new_list()
    for i in range(al.size(catalog["ordenes"])):
        pedido = al.get_element(catalog["ordenes"], i)
        if pedido["Product"] == producto and fecha_inicial <= pedido["Order_Date"] <= fecha_final:
            al.add_last(filtrados, pedido)
        
    lista_paises=msc.get(catalog["productos"],producto)
    pedido=al.get_element(lista_paises,0)
    i=0
    while i < al.size(lista_paises):
        pedido = al.get_element(lista_paises, i)
        if pedido["Product"] == producto and fecha_inicial <= pedido["Order_Date"] <= fecha_final:
            al.add_last(filtrados, pedido)
        i+=1

    paises_map = msc.new_map(100,4)
    for pedido in filtrados["elements"]:
        pais = pedido["Country"]
        pais_info = msc.get(paises_map, pais)
        if pais_info is None:
            pais_info = {
                "Country": pais,
                "Pedidos": 0,
                "Amount_total": 0,
                "Marketing_total": 0,
                "Boxes_total": 0
            }
            msc.put(paises_map, pais, pais_info)
        pais_info["Pedidos"] += 1
        pais_info["Amount_total"] += pedido["Amount"]
        pais_info["Marketing_total"] += pedido["Marketing_Spend"]
        pais_info["Boxes_total"] += pedido["Boxes_Shipped"]

    paises_lista = al.new_list()
    for bucket in paises_map["table"]:
        nodo = bucket["first"]
        while nodo is not None:
            entry = nodo["info"]
            info = entry["value"]
            if info["Marketing_total"] > 0:
                info["Eficiencia"] = info["Amount_total"] / info["Marketing_total"]
                al.add_last(paises_lista, info)
            nodo = nodo["next"]

    

    paises_ordenados = al.merge_sort(paises_lista, cmp_req_6)
    n_total = al.size(paises_ordenados)
    if n > n_total:
        n = n_total
    top_n = al.sub_list(paises_ordenados,0, n)

    total_amount = sum(p["Amount_total"] for p in paises_lista["elements"])
    total_marketing = sum(p["Marketing_total"] for p in paises_lista["elements"])

    fin = get_time()
    tiempo = delta_time(inicio,fin)

    print(f"Tiempo de ejecución: {tiempo} ms")
    print(f"Número total de pedidos filtrados: {al.size(filtrados)}")
    print(f"Número total de países encontrados: {n_total}")
    print(f"Amount total: {total_amount}")
    print(f"Marketing total: {total_marketing}\n")

    print(f"Top {n} países con mayor eficiencia de mercadeo:")
    for p in top_n["elements"]:
        print(p["Country"], 
              "Pedidos:", p["Pedidos"], 
              "Amount:", p["Amount_total"], 
              "Marketing:", p["Marketing_total"], 
              "Boxes:", p["Boxes_total"], 
              "Eficiencia:", round(p["Eficiencia"], 2))



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
