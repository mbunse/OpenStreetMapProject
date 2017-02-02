#!/usr/local/bin/python
# coding: utf8
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
import xml.dom.minidom as minidom
import re
import pprint
import codecs

OSMFILE = "schwabach.osm"
STREET_TYPE_RE = re.compile(r'\b\S+\.?$', re.IGNORECASE)

ZIP_TYPE_RE = re.compile(r'\d{5}')

HOUSENUMBER_TYPE_RE = re.compile(r'\d\d*[a-z]*')

EXPECTED = ["Straße", "Platz", "Allee", "Weg"]

EXPECTED_PATTERNS = [r'\S-Straße$',
                     r'\S+straße$',
                     r'\bStraße$',
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
MAPPING = {"Str.": "Straße",
           "Str": "Straße"
          }

MAPPING_HOUSENUMBER = {'ß20': "28"}

MAPPING_AMENITY = {"childcare": ['amenity', 'kindergarten'],
                   "BRK_Zentrum_Schwabach":  ['amenity', 'social centre'],
                   "schoolyard": ['leisure', 'playground']
                  }

INVESTIGATE_STREET = ["Hembacher Str"]

INVESTIGATE_HOUSENUMBER = ['ß20']

INVESTIGATE_AMENITY = ['childcare',
                       'schoolyard',
                       'BRK_Zentrum_Schwabach'
                      ]

EXPECTED_AMENITY = ["bar",
                    "bbq",
                    "biergarten",
                    "cafe",
                    "drinking_water",
                    "fast_food",
                    "food_court",
                    "ice_cream",
                    "pub",
                    "restaurant",
                    "college",
                    "kindergarten",
                    "library",
                    "public_bookcase",
                    "school",
                    "music_school",
                    "driving_school",
                    "language_school",
                    "university",
                    "bicycle_parking",
                    "bicycle_repair_station",
                    "bicycle_rental",
                    "boat_sharing",
                    "bus_station",
                    "car_rental",
                    "car_sharing",
                    "car_wash",
                    "charging_station",
                    "ferry_terminal",
                    "fuel",
                    "grit_bin",
                    "motorcycle_parking",
                    "parking",
                    "parking_entrance",
                    "parking_space",
                    "taxi",
                    "atm",
                    "bank",
                    "bureau_de_change",
                    "baby_hatch",
                    "clinic",
                    "dentist",
                    "doctors",
                    "hospital",
                    "nursing_home",
                    "pharmacy",
                    "social_facility",
                    "veterinary",
                    "blood_donation",
                    "arts_centre",
                    "brothel",
                    "casino",
                    "cinema",
                    "community_centre",
                    "fountain",
                    "gambling",
                    "nightclub",
                    "planetarium",
                    "social_centre",
                    "stripclub",
                    "studio",
                    "swingerclub",
                    "theatre",
                    "animal_boarding",
                    "animal_shelter",
                    "baking_oven",
                    "bench",
                    "clock",
                    "courthouse",
                    "coworking_space",
                    "crematorium",
                    "crypt",
                    "dive_centre",
                    "dojo",
                    "embassy",
                    "fire_station",
                    "firepit",
                    "game_feeding",
                    "grave_yard",
                    "gym",
                    "hunting_stand",
                    "internet_cafe",
                    "kneipp_water_cure",
                    "marketplace",
                    "photo_booth",
                    "place_of_worship",
                    "police",
                    "post_box",
                    "post_office",
                    "prison",
                    "public_building",
                    "ranger_station",
                    "recycling",
                    "rescue_station",
                    "sauna",
                    "shelter",
                    "shower",
                    "table",
                    "telephone",
                    "toilets",
                    "townhall",
                    "vending_machine",
                    "waste_basket",
                    "waste_disposal",
                    "waste_transfer_station",
                    "watering_place",
                    "water_point",
                    "user defined"
                   ]
EXPECTED_CITY = ["Regelsbach",
                 "Röthenbach bei St. Wolfgang"
                 "Leitelshof",
                 "Wendelstein Großschwarzenlohe"
                 "Wolkersdorf",
                 "Kleinschwarzenlohe",
                 "Rohr",
                 "Büchenbach",
                 "Poppenreuth",
                 "Dietersdorf",
                 "Nürnberg",
                 "Wendelstein",
                 "Wildenbergen",
                 "Barthelmesaurach",
                 "Schwaabch",
                 "Kammerstein-Neppersreuth",
                 "Schaftnach",
                 "wendelstein",
                 "Schwabach",
                 "Kammerstein",
                 "Schwanstetten",
                 "Rednitzhembach"
                ]

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

def audit_zip(zip_types, zipcode):
    """ audit zip code in osm file """
    matched = False
    if ZIP_TYPE_RE.match(zipcode):
        matched = True
    else:
        zip_types.add(zipcode)
    return matched

def audit_housenumber(housenumber_types, housenumber):
    """ audit housenumbers """
    if not HOUSENUMBER_TYPE_RE.match(housenumber):
        housenumber_types.add(housenumber)
        return False
    return True

def audit_city(cities, city):
    """ audit city """
    if city not in EXPECTED_CITY:
        cities.add(city)
        return False
    return True

def audit_amenity(amenities, amenity):
    """ audit city """
    if amenity not in EXPECTED_AMENITY:
        amenities.add(amenity)
        return False
    return True

def audit_leisure(leisures, leisure):
    """ audit leisure """
    leisures.add(leisure)
    return True

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    http://stackoverflow.com/questions/17402323/use-xml-etree-elementtree-to-write-out-nicely-formatted-xml-files
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t", encoding='utf-8')

def is_street_name(elem):
    """ return true if XML element elem is a street """
    return elem.attrib['k'] == "addr:street"

def is_zip(elem):
    """ return true if OSM element elem is a zip code """
    return elem.attrib['k'] == "addr:postcode"

def is_housenumber(elem):
    """ return true if OSM element elem is a housnumber """
    return elem.attrib['k'] == "addr:housenumber"

def is_city(elem):
    """ return true if OSM element elem is a city """
    return elem.attrib['k'] == "addr:city"

def is_amenity(elem):
    """ return true if OSM element elem is an amenity"""
    return elem.attrib['k'] == "amenity"

def is_leisure(elem):
    """ return true if OSM element elem is tagged as leisure"""
    return elem.attrib['k'] == "leisure"

def audit(osmfile):
    """ function to audit data in osm file.
    Returns an array with street types """
    osm_file = codecs.open(osmfile, "r")
    street_types = set()
    zip_types = set()
    housenumber_types = set()
    cities = set()
    amenities = set()
    leisure_types = set()
    with open("investigate_result.txt", "w") as outfile:

        for _, elem in ET.iterparse(osm_file, events=("start",)):

            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    value = tag.attrib['v'].encode('utf-8')
                    if is_street_name(tag):
                        if value in INVESTIGATE_STREET:
                            outfile.write(prettify(elem))
                        audit_street_type(street_types, value)
                    elif is_zip(tag):
                        audit_zip(zip_types, value)
                    elif is_housenumber(tag):
                        if value in INVESTIGATE_HOUSENUMBER:
                            outfile.write(prettify(elem))
                        audit_housenumber(housenumber_types, value)
                    elif is_city(tag):
                        audit_city(cities, value)
                    elif is_amenity(tag):
                        if value in INVESTIGATE_AMENITY:
                            outfile.write(prettify(elem))
                        audit_amenity(amenities, value)
                    elif is_leisure(tag):
                        audit_leisure(leisure_types, value)
        osm_file.close()
    return street_types, zip_types, housenumber_types, cities, amenities, leisure_types


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

def write_set(outfile, settowrite):
    """ write list to file """
    for item in list(settowrite):
        outfile.write("%s\n" % item)
    return

def test():
    """ function to test our implementation """

    audit_street_type(set(), "Agnes-Gerlach-Ring")
    audit_zip(set(), "12345")
    audit_housenumber(set(), "21a")
    assert update_housnumber('ß20', MAPPING_HOUSENUMBER) == "28"
    st_types, zip_types, housenumber_types, cities, amenities, leisure_types = audit(OSMFILE)


    with open("audit_result.txt", "w") as outfile:
        outfile.write("Unmatched street names:\n")
        write_set(outfile, st_types)
        outfile.write("Unmatched zip codes:\n")
        write_set(outfile, zip_types)
        outfile.write("Unmatched housenumbers:\n")
        write_set(outfile, housenumber_types)
        outfile.write("Unmatched cities:\n")
        write_set(outfile, cities)
        outfile.write("Unmatched amenities:\n")
        write_set(outfile, amenities)
        outfile.write("Unmatched leisure_types:\n")
        write_set(outfile, leisure_types)
        outfile.close()

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

"""
Idee:
<tag k="leisure" v="sports_centre"/>
<tag k="sport" v="climbing_adventure"/>
Suche nach Sportarten

"""