import os
import sys
import xml.etree.ElementTree as ET

from NodeDef import Node

xml_filename = ''
if len(sys.argv) == 2:
    xml_filename = sys.argv[1]
else:
    xml_filename = os.path.join('example', 'example.xml')

tree = ET.parse(xml_filename)
all_nodes = tree.getroot()
node_dict = {}

for child in all_nodes:
    child_name = child.attrib['id']
    logic = child.find('gate').text
    node_dict[child_name] = Node(child_name, logic)

for child in all_nodes:
    child_name = child.attrib['id']
    for dep in child.findall('dep'):
        dep_name = dep.text
        if dep_name in node_dict:
            node_dict[child_name].add_child(node_dict[dep_name])
        else:  # Special cases for nodes in <dep> but not <node>
            node_dict[dep_name] = Node(dep_name)
            node_dict[child_name].add_child(node_dict[dep_name])
