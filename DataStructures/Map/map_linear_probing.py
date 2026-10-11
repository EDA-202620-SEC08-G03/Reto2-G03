import random
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al

def new_map(num_elements, load_factor, prime=109345121):
    capacidad = mf.next_prime(num_elements / load_factor)
    tabla = al.new_list()
    for _ in range(capacidad):
        al.add_last(tabla, {"key": None, "value": None})

    mapa = {
        'prime': prime,
        'capacity': capacidad,
        'scale': random.randint(1, prime - 1),
        'shift': random.randint(0, prime - 1),
        'table': tabla,
        'limit_factor': load_factor,
        'size': 0,
        'current_factor': 0
    }
    return mapa

def size(map):
    return map["size"]

def hash_value(map, key):
    h = hash(key)
    a = map['scale']
    b = map['shift']
    p = map['prime']
    m = map['capacity']
    return int((abs(h*a + b) % p) % m)

def find_slot(map, key, pos):
    first_avail = None
    occupied = False
    i = 0

    while i < map["capacity"]:
        entry = al.get_element(map["table"], pos)

        if entry["key"] is None or entry["key"] == "__EMPTY__":
            if first_avail is None:
                first_avail = pos
            break
        elif entry["key"] == key:
            first_avail = pos
            occupied = True
            break

        pos = (pos + 1) % map["capacity"]
        i += 1

    return occupied, first_avail

def put(map, key, value):
    if map["size"] / map["capacity"] >= map["limit_factor"]:
        map = rehash(map)

    pos = hash_value(map, key)
    occupied, first_avail = find_slot(map, key, pos)

    if occupied:
        entry = al.get_element(map["table"], first_avail)
        entry["value"] = value
        al.change_info(map["table"], first_avail, entry)
    else:
        new_entry = {"key": key, "value": value}
        al.change_info(map["table"], first_avail, new_entry)
        map["size"] += 1
        map["current_factor"] = map["size"] / map["capacity"]
    
def get(map, key):
    pos = hash_value(map, key)
    steps = 0
    while steps < map["capacity"]:
        entry = al.get_element(map["table"], pos)
        if entry["key"] == key:
            return entry["value"]
        if entry["key"] is None:
            return None
        pos = (pos + 1) % map["capacity"]
        steps += 1
    return None

def contains(map, key):
    return get(map, key) is not None

def remove(map, key):
    pos = hash_value(map, key)
    steps = 0
    while steps < map["capacity"]:
        entry = al.get_element(map["table"], pos)
        if entry["key"] == key:
            al.change_info(map["table"], pos, {"key": "__EMPTY__", "value": None})
            map["size"] -= 1
            map["current_factor"] = map["size"] / map["capacity"]
            return
        if entry["key"] is None:
            return
        pos = (pos + 1) % map["capacity"]
        steps += 1

def rehash(map):
    old_table = map["table"]
    old_capacity = map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)
    new_table = al.new_list()
    for _ in range(new_capacity):
        al.add_last(new_table, {"key": None, "value": None})

    map["capacity"] = new_capacity
    map["table"] = new_table
    map["size"] = 0
    map["current_factor"] = 0


    for i in range(al.size(old_table)):
        entry = al.get_element(old_table, i)
        if entry and entry["key"] not in (None, "__EMPTY__"):
            pos = hash_value(map, entry["key"])
            _, first_avail = find_slot(map, entry["key"], pos)
            al.change_info(map["table"], first_avail, {"key": entry["key"], "value": entry["value"]})
            map["size"] += 1

    map["current_factor"] = map["size"] / map["capacity"]
    return map
