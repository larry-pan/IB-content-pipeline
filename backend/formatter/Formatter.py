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

    # def combine_json(self, master, new):
    #     """
    #     Updates the master dictionary with values from new,
    #     but only for keys that already exist in master.
    #     Extra keys in new are ignored.
    #     """
    #     return {key: new.get(key, master[key]) for key in master}

    # def combine_json(self, master, new):
    #     """
    #     Updates the master dictionary with values from new, but only for keys that already exist in master.
    #     Handles nested objects and arrays recursively.
    #     Extra keys in new are ignored.
    #     """
    #     if not isinstance(master, dict) or not isinstance(new, dict):
    #         return master

    #     result = {}

    #     for key in master:
    #         if key not in new:
    #             # Key doesn't exist in new, keep master value
    #             result[key] = master[key]
    #         elif isinstance(master[key], dict) and isinstance(new[key], dict):
    #             # Both are dictionaries, recursively combine
    #             result[key] = self.combine_json(master[key], new[key])
    #         elif isinstance(master[key], list) and isinstance(new[key], list):
    #             # Both are lists, combine them intelligently
    #             result[key] = self._combine_lists(master[key], new[key])
    #         else:
    #             # Direct replacement for non-nested values
    #             result[key] = new[key]

    #     return result

    # def _combine_lists(self, master_list, new_list):
    #     """
    #     Helper function to combine lists intelligently.
    #     For lists of dictionaries, tries to match and update based on common patterns.
    #     For simple lists, replaces with new list.
    #     """
    #     if not master_list or not new_list:
    #         return new_list if new_list else master_list

    #     # If both lists contain dictionaries, try to match and update them
    #     if (isinstance(master_list[0], dict) if master_list else False) and (
    #         isinstance(new_list[0], dict) if new_list else False
    #     ):

    #         # Create a copy of master list to work with
    #         result = master_list.copy()

    #         # Try to match items by 'order' field first, then by index
    #         for new_item in new_list:
    #             matched = False

    #             # Try to match by 'order' field if it exists
    #             if "order" in new_item:
    #                 for i, master_item in enumerate(result):
    #                     if (
    #                         isinstance(master_item, dict)
    #                         and master_item.get("order") == new_item["order"]
    #                     ):
    #                         result[i] = self.combine_json(master_item, new_item)
    #                         matched = True
    #                         break

    #             # If no match by order, try to match by index
    #             if not matched:
    #                 new_index = new_list.index(new_item)
    #                 if new_index < len(result):
    #                     result[new_index] = self.combine_json(result[new_index], new_item)
    #                 else:
    #                     # If new list is longer, append the extra items
    #                     result.append(new_item)

    #         return result
    #     else:
    #         # For non-dictionary lists, replace entirely
    #         return new_list
