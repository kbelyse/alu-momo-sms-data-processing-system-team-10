import xml.etree.ElementTree as ET
import json
import os

def parse_sms_xml(xml_file):
    """Parse the XML file into both list and dict structures."""
    if not os.path.exists(xml_file):
        raise FileNotFoundError(f"{xml_file} not found.")

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"Error parsing XML file: {e}")

    messages_list = []
    messages_dict = {}

    for sms in root.findall("sms"):
        msg = sms.attrib

        # Skip invalid entries without a 'date' attribute
        date_key = msg.get("date")
        if not date_key:
            continue  # or log a warning

        messages_list.append(msg)

        # Ensure unique key for messages_dict
        if date_key in messages_dict:
            # Append a suffix to handle duplicates
            duplicate_count = 1
            new_key = f"{date_key}_{duplicate_count}"
            while new_key in messages_dict:
                duplicate_count += 1
                new_key = f"{date_key}_{duplicate_count}"
            messages_dict[new_key] = msg
        else:
            messages_dict[date_key] = msg

    return messages_list, messages_dict


def save_json(data, filename):
    """Save Python data to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    xml_path = os.path.join("..", "data", "modified_sms_v2.xml")

    messages_list, messages_dict = parse_sms_xml(xml_path)

    save_json(messages_list, "sms_list.json")
    save_json(messages_dict, "sms_dict.json")

    print("✅ JSON files created: sms_list.json and sms_dict.json")

