import json


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
                        You convert the following response into a JSON with fields 'content', 'marks', 'markscheme', and 'subtopics'. 
                        Fix all formatting errors, including:

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
                        "content": {"type": "string"},
                        "marks": {"type": "integer"},
                        "markscheme": {"type": "string"},
                        "subtopics": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["content", "marks", "markscheme", "subtopics"],
                },
            },
        )
        response_json = json.loads(response.message.content[0].text)
        if topic:
            response_json["topic"] = topic
        return response_json

    def combine_json(self, master, new):
        """
        Updates the master dictionary with values from new,
        but only for keys that already exist in master.
        Extra keys in new are ignored.
        """
        return {key: new.get(key, master[key]) for key in master}
