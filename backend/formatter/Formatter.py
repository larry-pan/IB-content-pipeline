import json
import uuid


class Formatter:

    def __init__(self, co, model_id):
        self.co = co
        self.model_id = model_id

    def fix_json(self, str, topic=None):
        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                        You convert the following response into a JSON with string 'topic' and list 'parts', as strictly defined here: 
                        {
                            "topic": string,
                            "parts": [
                                {
                                    "content": string,
                                    "marks": int,
                                    "markscheme": string,
                                    "subtopics": list of strings,
                                    "order": int
                                },
                                ...
                            ]
                        }
                        Fix all formatting errors.
                        DO NOT CHANGE any of the content of the fields.
                        """,
                },
                {"role": "user", "content": str},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "parts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "content": {"type": "string"},
                                    "marks": {"type": "integer"},
                                    "markscheme": {"type": "string"},
                                    "subtopics": {"type": "array", "items": {"type": "string"}},
                                    "order": {"type": "integer"},
                                },
                                "required": [
                                    "content",
                                    "marks",
                                    "markscheme",
                                    "subtopics",
                                    "order",
                                ],
                            },
                        },
                    },
                    "required": ["topic", "parts"],
                },
            },
        )
        response_json = json.loads(response.message.content[0].text)
        if topic:
            response_json["topic"] = topic
        return response_json

    def finalize_json(self, question_json):
        question_json["id"] = str(uuid.uuid4())
        if "parts" not in question_json:
            question_json["parts"] = []
        if "options" not in question_json:
            question_json["options"] = []

        return question_json

    def combine_json(self, master, new):
        """
        Updates the master dictionary with values from new,
        but only for keys that already exist in master.
        Extra keys in new are ignored.
        """
        return {key: new.get(key, master[key]) for key in master}
