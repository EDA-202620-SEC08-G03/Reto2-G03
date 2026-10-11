from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
import random

def new_map(num_elements, load_factor, prime=109345121):
    capacidad = mf.next_prime(num_elements / load_factor)
    table = [sl.new_list() for i in range(capacidad)]

    mapa = {
        "prime": prime,
        "capacity": capacidad,
        "scale": random.randint(1, prime - 1),
        "shift": random.randint(0, prime - 1),
        "table": table,
        "limit_factor": load_factor,
        "size": 0
    }

    return mapa

def put(map, key, value):
    index = mf.hash_value(map, key)
    chain = map["table"][index]
    node = chain["first"]

    while node is not None:
        entry = node["info"]
        if entry["key"] == key:
            entry["value"] = value
            return
        node = node["next"]

    new_entry = me.new_map_entry(key, value)
    sl.add_last(chain, new_entry)
    map["size"] += 1

    if map["size"] / map["capacity"] > map["limit_factor"]:
        map = rehash(map)
    return map


def get(map, key):
    index = mf.hash_value(map, key)
    chain = map["table"][index]
    node = chain["first"]

    while node is not None:
        entry = node["info"]
        if entry["key"] == key:
            return entry["value"]
        node = node["next"]
    return None


def contains(map, key):
    return get(map, key) is not None


def remove(map, key):
    index = mf.hash_value(map, key)
    chain = map["table"][index]
    node = chain["first"]
    pos = 0

    while node is not None:
        entry = node["info"]
        if entry["key"] == key:
            sl.delete_element(chain, pos)
            map["size"] -= 1
            return
        node = node["next"]
        pos += 1


def size(map):
    return map["size"]


def is_empty(map):
    return map["size"] == 0

import DataStructures.List.array_list as al

def key_set(map):
    keys = al.new_list()
    for chain in map["table"]:
        node = chain["first"]
        while node is not None:
            entry = node["info"]
            al.add_last(keys, entry["key"])
            node = node["next"]
    return keys

def value_set(map):
    values = al.new_list()
    for chain in map["table"]:
        node = chain["first"]
        while node is not None:
            entry = node["info"]
            al.add_last(values, entry["value"])
            node = node["next"]
    return values

def rehash(map):
    old_table = map["table"]
    num_elements = map["size"]
    load_factor = map["limit_factor"]

    new_capacity = mf.next_prime(map["capacity"]*2)


    new_table = [sl.new_list() for i in range(new_capacity)]

    map["capacity"] = new_capacity
    map["table"] = new_table
    map["scale"] = random.randint(1, map["prime"] - 1)
    map["shift"] = random.randint(0, map["prime"] - 1)
    map["size"] = 0


    for chain in old_table:
        node = chain["first"]
        while node is not None:
            entry = node["info"]
            put(map, entry["key"], entry["value"])
            node = node["next"]


    return map
