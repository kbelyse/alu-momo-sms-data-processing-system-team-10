import xml.etree.ElementTree as ET
import json
import os

def parse_sms_xml(xml_file):
    """Parse the XML file into both list and dict structures."""
    if not os.path.exists(xml_file):
        raise FileNotFoundError(f"{xml_file} not found.")

    tree = ET.parse(xml_file)
    root = tree.getroot()

    messages_list = []
    messages_dict = {}

    for sms in root.findall("sms"):
        msg = sms.attrib
        messages_list.append(msg)
        # use the unique "date" as ID
        messages_dict[msg["date"]] = msg

    return messages_list, messages_dict

def save_json(data, filename):
    """Save Python data to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    xml_path = "../data/modified_sms_v2.xml"
    messages_list, messages_dict = parse_sms_xml(xml_path)

    save_json(messages_list, "sms_list.json")
    save_json(messages_dict, "sms_dict.json")

    print("✅ JSON files created: sms_list.json and sms_dict.json")
