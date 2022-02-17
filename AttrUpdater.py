# This program was created to replace attributes
# in YAML file (processors/resource/attributes)
# with Web Request attributes from XML file.

import xml.etree.ElementTree as ET
import yaml

try:
    class AttrUpdater:

        def __init__(self, file_xml, file_yaml):
            tree = ET.parse(file_xml)
            self.root = tree.getroot()
            self.file_yaml = file_yaml

        def value_replace(self):
            request = {}
            for child in self.root.iter('WebRequest'):
                for i in range(len(child)):
                    if child[i].text:
                        request[child[i].tag.lower()] = child[i].text

            try:
                if len(request) == 0:

                    raise Exception("The XML file has no web request attributes. Try another file.")

                old_type = 'requesttype'
                new_type = 'request.type'

                old_code = 'statuscode'
                new_code = 'app.status_code'

                request[new_type] = request.pop(old_type)
                request[new_code] = request.pop(old_code)

            except Exception as error:
                print(error)

            with open(self.file_yaml) as f:
                data_map = yaml.safe_load(f)

            try:
                for dicts in data_map['processors']['resource']['attributes']:
                    for tags, texts in request.items():
                        if tags == dicts.get("key"):
                            if texts.isnumeric():
                                dicts["value"] = int(texts)
                            else:
                                dicts["value"] = texts

            except TypeError:
                print("The YAML file does not have the appropriate attributes.")

            with open(self.file_yaml, 'w') as f:
                yaml.safe_dump(data_map, f, sort_keys=False, default_flow_style=False)

            print("The file has been updated successfully!")
            return self.file_yaml

except FileNotFoundError:
    print("Indicated file(s) doesn't exist")
