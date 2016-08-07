import json


class JSonisable:
    def to_json(self):
        """
        Converts the configuration to a json object
        """
        return json.dumps(self.__dict__, sort_keys=True)

    def from_json(self, json_content):
        """
        Import config values from a json object.
        """
        content = json.loads(json_content)
        for k, v in content.items():
            setattr(self, k, v)
        return self