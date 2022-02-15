import xml.etree.ElementTree as ET
import yaml

try:
    class AttrUpdater:

        def __init__(self, file_xml, file_yaml):
            tree = ET.parse(file_xml)
            self.root = tree.getroot()
            self.file_yaml = file_yaml

        def value_replace(self):
            requests = {}
            for child in self.root.iter('WebRequest'):
                for i in range(len(child)):
                    if child[i].text:
                        requests[child[i].tag.lower()] = child[i].text

            old_type = 'requesttype'
            new_type = 'request.type'

            old_code = 'statuscode'
            new_code = 'app.status_code'

            requests[new_type] = requests.pop(old_type)
            requests[new_code] = requests.pop(old_code)

            with open(self.file_yaml) as f:
                data_map = yaml.safe_load(f)

            for dicts in data_map['processors']['resource']['attributes']:
                for tags, texts in requests.items():
                    if tags == dicts.get("key"):
                        if texts.isnumeric():
                            dicts["value"] = int(texts)
                        else:
                            dicts["value"] = texts

            with open(self.file_yaml, 'w') as f:
                yaml.safe_dump(data_map, f, sort_keys=False, default_flow_style=False)

            return self.file_yaml


    d1 = AttrUpdater('xml_test_file.xml', 'zadanko_bartek.yaml')
    print(d1.value_replace())

except FileNotFoundError:
    print("Indicated file(s) doesn't exist")

