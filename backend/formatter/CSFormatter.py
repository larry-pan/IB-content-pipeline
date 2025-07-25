import json
from .BaseFormatter import BaseFormatter


class CSFormatter(BaseFormatter):

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
                        You convert the following response into a JSON with string 'topic' and list 'parts'.
                        If one of the two is not present, just leave the non-existant one as an empty array.
                        Format as strictly defined here: 
                        {
                            "question": string,
                            "parts": [
                                {
                                    "content": string,
                                    "marks": int,
                                    "markscheme": string,
                                    "subtopics": list of strings,
                                    "order": int
                                },
                                ...
                            ],
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
                        "question": {"type": "string"},
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
                    "required": ["question", "parts"],
                },
            },
        )
        response_json = json.loads(response.message.content[0].text)
        if topic:
            response_json["topic"] = topic
        return response_json
