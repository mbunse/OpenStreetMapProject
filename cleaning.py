#!/usr/bin/env python
# coding: utf8
"""
    Code by Moritz Bunse

    Module for data cleaning of schwabach OSM data
"""
from audit import STREET_TYPE_RE, is_street_name, is_housenumber, is_amenity

MAPPING = {"Str.": "Straße",
           "Str": "Straße"
          }

MAPPING_HOUSENUMBER = {'ß20': "28"}

MAPPING_AMENITY = {"childcare": ['amenity', 'kindergarten'],
                   "BRK_Zentrum_Schwabach":  ['amenity', 'social centre'],
                   "schoolyard": ['leisure', 'playground']
                  }

def update_name(name, mapping):
    """ Function to update a street name according to our rules """
    match = STREET_TYPE_RE.search(name)
    if match:
        street_type = match.group()
        if street_type in mapping:
            name = STREET_TYPE_RE.sub(mapping[street_type], name)
    return name

def update_housnumber(housenumber, mapping):
    """ Function to update a street name according to our rules """
    if housenumber in mapping:
        return mapping[housenumber]
    else:
        return housenumber

def update_amenity(key, amenity, mapping):
    """ Function to update a street name according to our rules """
    if amenity in mapping:
        return mapping[amenity]
    else:
        return key, amenity

def update_tag(elem):
    """ function to update tag in OSM according to our findings """
    value = elem.attrib['v'].encode('utf-8')
    key = elem.attrib['k'].encode('utf-8')
    if is_street_name(elem):
        value = update_name(value, MAPPING)
    elif is_housenumber(elem):
        value = update_housnumber(value, MAPPING_HOUSENUMBER)
    elif is_amenity(elem):
        key, value = update_amenity(key, value, MAPPING_AMENITY)
    else:
        return elem
    elem.attrib['v'] = value.decode('utf-8')
    elem.attrib['k'] = key.decode('utf-8')
    return elem

def test():
    """ function to run test on functions in this module """
    assert update_housnumber('ß20', MAPPING_HOUSENUMBER) == "28"
    assert update_amenity("amenity", "childcare", MAPPING_AMENITY) == ['amenity', 'kindergarten']
    assert update_name("Hembacher Str", MAPPING) == "Hembacher Straße"

if __name__ == '__main__':
    test()
