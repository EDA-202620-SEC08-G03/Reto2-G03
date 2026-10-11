def new_list():
    
    newlist = {
        "elements": [],
        "size": 0,
    }
    
    return newlist

def get_element(my_list, index):
    
    return my_list["elements"][index]

def is_present(my_list, element, cmp_function):
    
    size = my_list["size"]
    if size > 0:
        keyexist = False
        for keypos in range(0, size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1

def add_first (my_list, element):
    
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    
    return my_list

def add_last (my_list, element):
    
    my_list["elements"].append(element)
    my_list["size"] += 1
    
    return my_list

def is_empty (my_list):
    
    booleano = False
    if my_list["size"] == 0: 
        booleano = True
    
    return booleano

def size (my_list):
    
    return my_list["size"]

def delete_element (my_list, pos):
    
    if not (0 <= pos < size(my_list)):
        raise IndexError("list index out of range")
    
    my_list["elements"].pop(pos)
    my_list["size"] = my_list["size"] - 1
    
    return my_list   

def remove_first (my_list):
    
    if is_empty(my_list):
        raise IndexError("list index out of range")
    
    borrado = my_list["elements"].pop(0)
    my_list["size"] -= 1
    
    return borrado

def remove_last (my_list):
    
    if is_empty(my_list):
        raise IndexError("list index out of range")
    
    borrado = my_list["elements"].pop(-1)
    
    my_list["size"] -= 1
    
    return borrado

def insert_element (my_list, element, pos):
    
    my_list["elements"].insert(pos, element)
    
    my_list["size"] += 1

    return my_list
def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")
    my_list["elements"][pos] = new_info
    return my_list["elements"][pos]

def exchange (my_list, pos_1, pos_2):
    
    if pos_1 < 0 or pos_1 >= my_list["size"] or pos_2 < 0 or pos_2 >= my_list["size"]:
        raise IndexError("list index out of range")
    
    valor_1 = my_list["elements"][pos_1]
    valor_2 = my_list["elements"][pos_2]
    
    change_info(my_list, pos_1, valor_2)
    change_info(my_list, pos_2, valor_1)
    
    return my_list

def sub_list (my_list, pos_i, num_elements):
    
    if pos_i < 0 or pos_i >= my_list["size"]:
        raise IndexError("list index out of range")
    
    elementos = my_list["elements"][pos_i : pos_i + num_elements]
    lista_nueva = {
        "size": len(elementos),
        "elements": elementos
    }
    
    return lista_nueva

def first_element (my_list):
    
    if is_empty(my_list):
        raise IndexError("list index out of range")
    
    elemento = my_list["elements"][0]
    return elemento

def last_element (my_list):
    
    if is_empty(my_list):
        raise IndexError("list index out of range")
        
    elemento = my_list["elements"][my_list["size"] - 1]
    return elemento

def default_sort_criteria (element_1, element_2) -> bool:
    
    is_sorted = False
    if element_1 < element_2:
        is_sorted = True
    return is_sorted
    
def selection_sort (my_list, sort_crit):
    
    tamaño = size(my_list)

    for indice in range(tamaño):
        posicion_menor = indice
        for posicion in range(indice + 1, tamaño):
            if sort_crit(get_element(my_list, posicion), get_element(my_list, posicion_menor)):
                posicion_menor = posicion
        if posicion_menor != indice:
            my_list = exchange(my_list, indice, posicion_menor)

    return my_list

def insertion_sort (my_list, sort_crit):

    tamaño = size(my_list)

    for indice in range(1, tamaño):
        posicion = indice
        while posicion > 0 and sort_crit(get_element(my_list, posicion), get_element(my_list, posicion - 1)):
            my_list = exchange(my_list, posicion, posicion - 1)
            posicion -= 1

    return my_list

def shell_sort (my_list, sort_crit):
    
    tamaño = size(my_list)

    if tamaño <= 1:
        return my_list

    salto = tamaño // 2
    while salto > 0:
        for indice in range(salto, tamaño):
            posicion = indice
            while posicion >= salto and sort_crit(get_element(my_list, posicion), get_element(my_list, posicion - salto)):
                my_list = exchange(my_list, posicion, posicion - salto)
                posicion -= salto
        salto = salto // 2

    return my_list
def merge_sort(my_list, cmp_function=default_sort_criteria):
    if my_list["size"] <= 1:
        return my_list
    
    medio = my_list["size"] // 2
    izq = merge_sort(sub_list(my_list, 0, medio), cmp_function)
    der = merge_sort(sub_list(my_list,medio, my_list["size"]), cmp_function)
    
    result = new_list()
    i = 0
    j = 0
    
    while i < izq["size"] and j < der["size"]:
        elem_izq = get_element(izq, i)
        elem_der = get_element(der, j)
        
        if cmp_function(elem_izq, elem_der): 
            add_last(result, elem_izq)  
            i += 1
        else:
            add_last(result, elem_der)
            j += 1
            
    while i < izq["size"]:
        add_last(result, get_element(izq, i))
        i += 1
        
    while j < der["size"]:
        add_last(result, get_element(der, j))
        j += 1
        
    return result
def quick_sort(lista, cmp_function=default_sort_criteria):
    if lista["size"] <= 1:
        return lista
    pivot = get_element(lista,0)
    left = new_list()
    right = new_list()
    i=1
    while i<lista["size"]:
        actual=get_element(lista,i)
        if cmp_function(actual, pivot):
            add_last(left, actual)
        else:
            add_last(right, actual)
        i+=1
    left_sorted = quick_sort(left, cmp_function)
    right_sorted = quick_sort(right, cmp_function)
    result = new_list()
    j=0
    while j<size(left_sorted):
        actual = get_element(left_sorted,j)
        add_last(result, actual)
        j+=1
    add_last(result, pivot)
    j=0
    while j<size(right_sorted):
        actual = get_element(right_sorted,j)
        add_last(result, actual)
        j+=1
    return result
