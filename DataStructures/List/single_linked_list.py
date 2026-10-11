def new_list():
    newlist={
        "first":None,"last":None,"size":0,
    }
    return newlist
def add_first(lista,element):
    new={
        "info":element,"next":lista["first"]
    }
    lista["first"]=new
    if lista["size"]==0:
        lista["last"]=new
    lista["size"]+=1
    return lista
def add_last(lista,element):
    new={
        "info":element,"next":None
    }
    if lista["size"]==0:
        lista["first"]=new
    else:
        lista["last"]["next"]=new
    lista["size"]+=1
    lista["last"]=new
    return lista

def size(lista):
    return lista["size"]

def first_element(lista):
    
    if is_empty(lista):
      raise Exception('IndexError: list index out of range')
    return lista["first"]["info"]
def is_empty(lista):
    if lista["size"]==0:
        return True
    return False
def last_element(lista):
    if is_empty(lista):
      raise Exception('IndexError: list index out of range')
    return lista["last"]["info"]
def delete_element(lista,pos):
    if pos < 0 or pos >= size(lista):
        raise Exception('IndexError: list index out of range')
    if pos ==0:
        
        borrado=lista["first"]
        lista["first"]=lista["first"]["next"]
        lista["size"]-=1
        if lista["size"]==0:
            lista["last"]=None
    
    else:
        actual=lista["first"]
        i=0
        while i<pos-1:
            actual=actual["next"]
            i+=1
        borrado=actual["next"]
        actual["next"]=borrado["next"]
        if pos == lista["size"]-1:
            lista["last"]=actual
        lista["size"]-=1
    return lista
def remove_first(lista):
    if is_empty(lista):
        raise Exception("IndexError: list index out of range")
    
    borrado=lista["first"]
    lista["first"]=lista["first"]["next"]
    if lista ["first"] is None:
        lista["last"]=None
    lista["size"]-=1
    return borrado["info"]
def remove_last(lista):
    if is_empty(lista):
        raise Exception("IndexError: list index out of range")
    borrado=lista["last"]
    if lista["size"]==1:
        lista["first"]=None
        lista["last"]=None
    else:
        actual=lista["first"]
        while actual["next"] != lista["last"]:
            actual=actual["next"]
        
        actual["next"]=None
        lista["last"]=actual
    lista["size"]-=1
    return borrado["info"]
def insert_element(lista,elemento,pos):
    if pos < 0 or pos > size(lista):
        raise Exception('IndexError: list index out of range')
    else:
        new={
            "info":elemento,
            "next":None
        }
        if pos==0:
            new["next"]=lista["first"]
            lista["first"]=new
            if lista["size"]==0:
                lista["last"] = new
        else:
            i=0
            actual=lista["first"]
            while i<pos-1:
                actual=actual["next"]
                i+=1
            new["next"]=actual["next"]
            actual["next"]=new
            if pos ==lista["size"]:
                lista["last"]=new
    lista["size"]+=1

    return lista
def change_info(lista,pos,nueva_info):
    if pos <0 or pos >=lista["size"]:

        raise Exception ("IndexError: list index out of range")

    anterior=lista["first"]
    i=0
    while i<pos:
        anterior=anterior["next"]
        i+=1
    anterior["info"]=nueva_info
    return lista
def exchange(lista,pos1,pos2):
    if pos1<0 or pos2<0 or pos1>=lista["size"] or pos2>=lista["size"]:
        raise Exception("IndexError. list index out of range")
    i=0
    elemento1=lista["first"]
    while i<pos1:
        elemento1=elemento1["next"]
        i+=1
    j=0
    elemento2=lista["first"]
    while j<pos2:
        elemento2=elemento2["next"]
        j+=1
    cambio=elemento1

    elemento1["info"]=elemento2["info"]
    elemento2["info"]=cambio["info"]
    
    return lista
def sub_list(lista,pos,num_elements):
    if pos<0 or pos>=lista["size"] or num_elements>lista["size"]-pos:
        raise Exception ("IndexError:list index out of range")
    primero_sub=lista["first"]
    for i in range(pos):
        primero_sub=primero_sub["next"]
    
    if num_elements==0:
        sublista=new_list()
        
    else:
        sublista=new_list()
    
        elemento_sub=primero_sub
        for i in range(num_elements):
            
            add_last(sublista,elemento_sub["info"])
            elemento_sub=elemento_sub["next"]    
        
    return sublista        
def get_element(lista,pos):
    searchpos=0
    node=lista["first"]
    while searchpos<pos:
        node=node["next"]
        searchpos+=1
    return node["info"]
def is_present(lista,elemento,cmp_function):
    is_in_array=False
    temp=lista["first"]
    count=0
    while not is_in_array and temp is not None:
        if cmp_function(elemento,temp["info"])==0:
            is_in_array=True
        else:
            temp=temp["next"]
            count+=1
    if not is_in_array:
        count= -1
    return count
def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(lista, cmp_function=default_sort_criteria):
    if lista["size"] > 1:
        current = lista["first"]
        while current is not None:
            min_node = current
            next_node = current["next"]
            while next_node is not None:
                if not cmp_function(min_node["info"], next_node["info"]):
                    min_node = next_node
                next_node = next_node["next"]
            if min_node != current:
                current["info"], min_node["info"] = min_node["info"], current["info"]
            current = current["next"]
    return lista

def insertion_sort(lista, cmp_function=default_sort_criteria):
    if lista["size"] > 1:
        current = lista["first"]["next"]
        while current is not None:
            key = current["info"]
            prev = lista["first"]
            while prev != current and cmp_function(prev["info"], key):
                prev = prev["next"]
            if prev != current:
                carry = prev["info"]
                prev["info"] = key
                node = prev["next"]
                while node != current:
                    next_carry = node["info"]
                    node["info"] = carry
                    carry = next_carry
                    node = node["next"]
                node["info"] = carry  # node == current aquí
            current = current["next"]
    return lista

def shell_sort(lista, cmp_function=default_sort_criteria):
    n = lista["size"]
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = get_element(lista, i)
            j = i
            while j >= gap and not cmp_function(get_element(lista, j - gap), temp):
                change_info(lista, j, get_element(lista, j - gap))
                j -= gap
            change_info(lista, j, temp)
        gap //= 2
    return lista
def merge_sort(lista, cmp_function=default_sort_criteria):
    if lista["size"] <= 1:
        return lista
    medio = lista["size"] // 2
    izq = merge_sort(sub_list(lista, 0, medio), cmp_function)
    der = merge_sort(sub_list(lista, medio, medio), cmp_function)
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
    pivot = first_element(lista)
    left = new_list()
    right = new_list()
    actual = lista["first"]["next"]
    while actual is not None:
        if cmp_function(actual["info"], pivot):
            add_last(left, actual["info"])
        else:
            add_last(right, actual["info"])
        actual = actual["next"]
    left_sorted = quick_sort(left, cmp_function)
    right_sorted = quick_sort(right, cmp_function)
    result = new_list()
    actual = left_sorted["first"]
    while actual is not None:
        add_last(result, actual["info"])
        actual = actual["next"]
    add_last(result, pivot)
    actual = right_sorted["first"]
    while actual is not None:
        add_last(result, actual["info"])
        actual = actual["next"]
    return result
