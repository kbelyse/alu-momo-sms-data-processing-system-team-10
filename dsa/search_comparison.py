import time
import random
from data_parser import parse_sms_xml

def linear_search(messages_list, target_id):
    """Linear search through list of dicts."""
    for msg in messages_list:
        if msg["date"] == target_id:
            return msg
    return None

def dict_lookup(messages_dict, target_id):
    """Dictionary lookup by key."""
    return messages_dict.get(target_id)

if __name__ == "__main__":
    xml_path = "../data/modified_sms_v2.xml"
    messages_list, messages_dict = parse_sms_xml(xml_path)

    # Pick 20 random IDs from the dict
    sample_ids = random.sample(list(messages_dict.keys()), 20)

    print("Comparing linear search vs dict lookup...\n")

    for tid in sample_ids:
        # Linear search
        start = time.time()
        linear_result = linear_search(messages_list, tid)
        linear_time = (time.time() - start) * 1e6  # microseconds

        # Dict lookup
        start = time.time()
        dict_result = dict_lookup(messages_dict, tid)
        dict_time = (time.time() - start) * 1e6  # microseconds

        print(f"ID {tid} → Linear: {linear_time:.2f}µs | Dict: {dict_time:.2f}µs")

