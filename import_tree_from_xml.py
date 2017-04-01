import os#  Throw coin for all leaves
        for leaf in leaf_node_dict:
            # http://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
            leaf_node_dict[leaf].state = bool(random.getrandbits(1))
import sys
import xml.etree.ElementTree as ET

from NodeDef import Node


def import_tree_from_xml(xml_filename):
    tree = ET.parse(xml_filename)
    all_nodes = tree.getroot()
    node_dict = {}

    # As we will perform monte carlo on leaves, keep a dict for easier access.
    leaf_node_dict = {}

    # First iter, build all nodes (except nodes only appear in <dep>)
    # and put them in node_dict
    for node in all_nodes:
        node_name = node.attrib['id']
        logic = node.find('gate').text
        if node_name in node_dict:
            raise ValueError("Different nodes with same name")
        node_dict[node_name] = Node(node_name, logic)

    # Second iter, build parent-child relationship and put leaves in another
    # dict.
    for node in all_nodes:
        node_name = node.attrib['id']
        if node.findall('dep'):
            for dep in node.findall('dep'):
                dep_name = dep.text
                if dep_name in node_dict:
                    node_dict[node_name].add_child(node_dict[dep_name])
                else:  # Special cases for nodes in <dep> but not <node>
                    node_dict[dep_name] = Node(dep_name)
                    node_dict[node_name].add_child(node_dict[dep_name])
                    leaf_node_dict[dep_name] = node_dict[dep_name]
        else:
            leaf_node_dict[node_name] = node_dict[node_name]

    return node_dict, leaf_node_dict
