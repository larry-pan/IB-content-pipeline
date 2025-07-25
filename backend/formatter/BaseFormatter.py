import json
import uuid

class BaseFormatter:

    def __init__(self, co, model_id):
        self.co = co
        self.model_id = model_id

    def finalize_json(self, question_json):
        question_json["id"] = str(uuid.uuid4())

        return question_json

    def combine_json(self, master, new):
        """
        Updates the master dictionary with values from new,
        but only for keys that already exist in master.
        Extra keys in new are ignored.
        """
        return {key: new.get(key, master[key]) for key in master}
