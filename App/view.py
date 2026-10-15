import sys
import App.logic as logic
from DataStructures.List import array_list as lt

archivos = {
    "1": "chocolate_sale_100_elementos.csv",
    "2": "chocolate_sale_10_ptc.csv",
    "3": "chocolate_sale_20_ptc.csv",
    "4": "chocolate_sale_30_ptc.csv",
    "5": "chocolate_sale_40_ptc.csv",
    "6": "chocolate_sale_50_ptc.csv",
    "7": "chocolate_sale_60_ptc.csv",
    "8": "chocolate_sale_70_ptc.csv",
    "9": "chocolate_sale_80_ptc.csv",
    "10": "chocolate_sale_90_ptc.csv",
    "11": "chocolate_sale_100_ptc.csv",
}

def new_logic():
    """
        Se crea una instancia del controlador
    """
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    print("\n¿Qué archivo desea cargar?\n")
    print("1- 100 elementos (pruebas rápidas)")
    print("2- 10%")
    print("3- 20%")
    print("4- 30%")
    print("5- 40%")
    print("6- 50%")
    print("7- 60%")
    print("8- 70%")
    print("9- 80%")
    print("10- 90%")
    print("11- 100% (Definitivo)")
    opcion = input("Seleccione una opción: ")
    filename = archivos.get(opcion, archivos["1"])

    start_time = logic.get_time()
    logic.load_data(control, filename)
    end_time = logic.get_time()
    tiempo = logic.delta_time(start_time, end_time)

    resumen = logic.resumen_carga(control)
    print_resumen_datos(tiempo, resumen)
    
def print_resumen_datos(tiempo, resumen):
    
    print("\nTiempo de carga: {0:.2f} ms".format(tiempo))
    print("Total de pedidos cargados: {0}".format(resumen["total"]))

    print("\nPedido de menor cantidad:")
    print_pedido(resumen["menor"])

    print("\nPedido de mayor cantidad:")
    print_pedido(resumen["mayor"])

    print("\nPrimeros 5 registros:")
    for p in resumen["primeros_5"]:
        print_pedido(p)

    print("\nÚltimos 5 registros:")
    for p in resumen["ultimos_5"]:
        print_pedido(p)

def print_pedido(p): 
    print(" {0} | {1} | {2} | {3} | {4} | {5} |${6:.2f} | ${7:.2f}".format(p["Order_ID"], p["Product"], p["Country"], p["Channel"],p["Order_Date"], p["Boxes_Shipped"], p["Price_per_Box"], p["Amount"]))
    #Tomado del reto anterior, que fue realizado utlizando IAG, solo se añade "Boxes Shipped" 


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    pedidos = control["ordenes"]
    total = lt.size(pedidos)
    
    encontrado = None
    i = 0
    while encontrado is None and i < total:
        actual = lt.get_element(pedidos, i)
        if actual["Order_ID"] == id:
            encontrado = actual
        i += 1

    if encontrado is not None:
        print("\nPedido encontrado:")
        print_pedido(encontrado)
    else:
        print("\nNo se encontró ningún pedido con Order_ID = {0}".format(id))
    #Tomado del reto anterior, que fue realizado utlizando IAG

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    anio = input("Ingrese el año (YYYY): ").strip()
    mes = input("Ingrese el mes (MM): ").strip()
    descuento_min = float(input("Ingrese el descuento mínimo: "))
    descuento_max = float(input("Ingrese el descuento máximo: "))
    print(logic.req_1(control, anio, mes, descuento_min, descuento_max))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    
    pais = input("Ingrese un país: ").strip()
    min_cajas = int(input("Número mínimo de cajas enviadas: "))
    max_cajas = int(input("Número máximo de cajas enviadas: "))
    print(logic.req_2(control, pais, min_cajas, max_cajas))

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    
    fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
    min_amount = int(input("Ingrese el Amount mínimo: "))
    max_amount = int(input("Ingrese el Amount máximo: "))
    print(logic.req_3(control, fecha, min_amount, max_amount))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    producto = input("Ingrese el producto: ")
    pais = input("Ingrese el país: ")
    print(logic.req_4(control, producto, pais))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    
    n = int(input("Número de productos a consultar: "))
    pais = input("Ingrese un país: ")
    fecha_inicio = input("Ingrese la fecha inicial del periodo: ")
    fecha_final = input("Ingrese la fecha final del periodo: ")
    print(logic.req_5(control, n, pais, fecha_inicio, fecha_final))


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    producto = input("Ingrese el producto: ")
    fecha_inicial = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
    fecha_final = input("Ingrese la fecha final (YYYY-MM-DD): ")
    n = int(input("Ingrese N (cantidad de países): "))
    print(logic.req_6(control, producto, fecha_inicial, fecha_final, n))

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
