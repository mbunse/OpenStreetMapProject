#!/usr/local/bin/python
# coding: utf-8
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes
    needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area
    you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "schwabach.osm"
STREET_TYPE_RE = re.compile(r'\b\S+\.?$', re.IGNORECASE)


EXPECTED = ["Stra\xdfe", "Platz", "Allee", "Weg"]

EXPECTED_PATTERNS = [r'\S-Stra\xdfe$',
                     r'\S+stra\xdfe$',
                     r'\bStra\xdfe$',
                     r'\S-Weg$',
                     r'weg$',
                     r'\bWeg$',
                     r'gasse',
                     r'\S-Gasse$',
                     r'\bGasse$',
                     r'Am\b',
                     r'^An der\b',
                     r'^An den\b',
                     r'^Auf der\b',
                     r'^Im\b',
                     r'^In der\b',
                     r'\S-Ring$',
                     r'\Sring$',
                     r'\Sallee$',
                     r'\Sgrund$',
                     r'\Sgraben',
                     r'\Sberg$',
                     r'\Splatz$',
                     r'\S-Platz$'
                    ]

# UPDATE THIS VARIABLE
MAPPING = {"Str.": "Stra\xdfe",
           "Str": "Stra\xdfe"
          }


def audit_street_type(street_types, street_name):
    """ check the street type """
    matched = False
    for pattern in EXPECTED_PATTERNS:
        match = re.search(pattern, street_name)
        if match:
            matched = True
            break

    if not matched:
        street_types.add(street_name)


def is_street_name(elem):
    """ return true if XML element elem is a street """
    return elem.attrib['k'] == "addr:street"


def audit(osmfile):
    """ function to audit data in osm file.
    Returns an array with street types """
    osm_file = open(osmfile, "r")
    street_types = set()
    for _, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    """ Function to update a street name according to our rules """
    match = STREET_TYPE_RE.search(name)
    if match:
        street_type = match.group()
        if street_type in mapping:
            name = STREET_TYPE_RE.sub(mapping[street_type], name)
    return name


def test():
    """ function to test our implementation """

    audit_street_type(set(), "Agnes-Gerlach-Ring")
    st_types = audit(OSMFILE)
    pprint.pprint(st_types)
    # assert len(st_types) == 3

    # for _, ways in st_types.iteritems():
    #     for name in ways:
    #         better_name = update_name(name, MAPPING)
    #         print name, "=>", better_name
    #         if name == "West Lexington St.":
    #             assert better_name == "West Lexington Street"
    #         if name == "Baldwin Rd.":
    #             assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()
