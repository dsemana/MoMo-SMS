import xml.etree.ElementTree as ET
import json
 
 
def parse_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
 
    records = []
    idx = 1
 
    for sms in root.findall('sms'):
        record = {
            'id':           idx,
            'address':      sms.get('address'),
            'date':         sms.get('date'),
            'readable_date': sms.get('readable_date'),
            'body':         sms.get('body'),
            'type':         sms.get('type'),
            'read':         sms.get('read'),
        }
        records.append(record)
        idx += 1
 
    return json.loads(json.dumps(records))
 
 
if __name__ == '__main__':
    data = parse_xml(r'C:\Users\rusan\Downloads\modified_sms_v2.xml')
    print(json.dumps(data, indent=2))