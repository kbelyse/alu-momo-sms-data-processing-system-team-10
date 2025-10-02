import xml.etree.ElementTree as ET
import json

def parse_sms_xml_to_json(xml_file, json_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    messages = []
    for sms in root.findall('sms'):
        msg = sms.attrib  # Get all attributes of <sms>
        messages.append(msg)

    # Save as JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

    print(f"Successfully converted {xml_file} to {json_file}")

# Example usage
if __name__ == "__main__":
    parse_sms_xml_to_json("modified_sms_v2.xml", "sms_data.json")
