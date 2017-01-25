#!/usr/bin/env python

"""
    Code by Moritz Bunse
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

LOWER = re.compile(r'^([a-z]|_)*$')
LOWER_COLON = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    """ Reorganized and xml element and returns the result as a Python dictionary. """
    node = {}
    if element.tag == "node" or element.tag == "way":
        node["id"] = element.get("id")
        node["visible"] = element.get("visible")
        node["type"] = element.tag
        node["created"] = {}
        for key in CREATED:
            node["created"][key] = element.get(key)
        if element.tag == "node":
            node["pos"] = [float(element.get("lat")), float(element.get("lon"))]

        for tag in element.iter():
            if tag.tag == "tag":
                attr = tag.get("k")
                if attr.count(":") > 1:
                    continue
                if attr.startswith("addr:"):
                    if not node.has_key("address"):
                        node["address"] = {}
                    node["address"][attr.split(":")[1]] = tag.get("v")
                else:
                    node[attr] = tag.get("v")
            elif tag.tag == "nd":
                if not node.has_key("node_refs"):
                    node["node_refs"] = []
                node["node_refs"].append(tag.get("ref"))
        #print node
        return node
    else:
        return None


def process_map(file_in, pretty=False):
    """ Processes file_in and creates a new json file from this file. """
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as outfile:
        for _, element in ET.iterparse(file_in):
            elem = shape_element(element)
            if elem:
                data.append(elem)
                if pretty:
                    outfile.write(json.dumps(elem, indent=2)+"\n")
                else:
                    outfile.write(json.dumps(elem) + "\n")
    return data

def test():
    """ Calls the process_map function and checks the output. """

    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('schwabach.osm', True)

    correct_first_elem = {
        "id": "15848361",
        "type": "node",
        "visible": None,
        "pos": [49.3723114, 11.1581090],
        "created": {
            "changeset": "28510221",
            "user": "sennewald63",
            "version": "6",
            "uid": "372615",
            "timestamp": "2015-01-30T18:18:40Z"
        }
    }
    pprint.pprint(data[0])

    assert data[0] == correct_first_elem


    # assert data[-1]["address"] == {
    #                                 "street": "West Lexington St.",
    #                                 "housenumber": "1412"
    #                                   }
    # assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369",
    #                                 "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()
    