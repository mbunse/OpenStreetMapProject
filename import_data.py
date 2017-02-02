#!/usr/bin/env python
# coding: utf8
"""
    Code by Moritz Bunse
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import audit

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
                tag = audit.update_tag(tag)
                attr = tag.get("k")
                attributes = attr.split(":")
                value = tag.get("v")
                if len(attributes) > 2:
                    continue
                if attributes[0] == "addr":
                    if not node.has_key("address"):
                        node["address"] = {}
                    node["address"][attributes[1]] = value
                else:
                    if len(attributes) > 1:
                        if not node.has_key(attributes[0]):
                            node[attributes[0]] = {}
                        elif not isinstance(node[attributes[0]], dict):
                            continue
                        node[attributes[0]][attributes[1]] = value
                    else:
                        node[attributes[0]] = value
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
    with codecs.open(file_out, "w", encoding="utf-8") as outfile:
        for _, element in ET.iterparse(file_in):
            elem = shape_element(element)
            if elem:
                data.append(elem)
                if pretty:
                    outfile.write(
                        json.dumps(elem, indent=2, ensure_ascii=False)+"\n"
                        )
                else:
                    outfile.write(json.dumps(elem, ensure_ascii=False) + "\n")
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
    