import json


class CSJudge:
    def __init__(self, co, model_id):
        self.co = co
        self.model_id = model_id

    def judge_question(self, question):

        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are a judge for IB math questions. 
                        You must output a JSON object with JSON list 'parts' mutating only the new 'content' and 'subtopics' 
                        if they can be improved, and an integer 'score' from 0-100 for how well the question conforms to the guidelines.
                        Strictly follow this format:
                        {
                            "question": string,
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
                            ],
                            "score": int
                        }

                        This is based on the following guidelines:
                        - The question has no errors.
                        - The subtopics are a single string that is a valid IB subtopic.
                        - The questions covers the specified topic and subtopics, without missing any or including concepts outside the topics.
                        - The questions are readable in string format.
                        - The questions make sense and is solvable
                        DO NOT add anything to the fields that does not explicitly fix a problem.
                        """,
                },
                {"role": "user", "content": str(question)},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
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
                        "score": {"type": "integer"},
                    },
                    "required": ["question", "topic", "parts", "score"],
                },
            },
        )
        json_obj = json.loads(response.message.content[0].text)
        score = json_obj["score"]
        json_obj.pop("score", None)
        return json_obj, score

    def judge_markscheme(self, question):

        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a judge for IB math markschemes. 
                    You must output a JSON object with JSON list 'parts' the new 'content', 'marks', 
                    and 'markscheme' if they can be improved and an integer 'score' from 0-100 
                    indicating how well the original question conforms to the guidelines. 
                    Strictly follow this format:
                    {
                        "question": string,
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
                        ],
                        "score": int
                    }

                    This is based on the following factors:
                    - The markscheme has no errors and answers the question correctly.
                    - For coding problems, the markscheme is written in pseudocode.
                    - The markscheme is as concise as possible, with very limited and only strictly needed explanation.
                    - The markscheme focuses as much as possible on short concrete requirements.
                    - The markscheme clearly distributes the correct number of marks to the correct steps.
                    A step worth 1 mark should be marked [M1], a step worth 2 marks is [M2], all the Ms should strictly add up to 'marks'.
                    DO NOT add anything to the fields that does not explicitly fix a problem.""",
                },
                {"role": "user", "content": str(question)},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
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
                        "score": {"type": "integer"},
                    },
                    "required": ["question", "topic", "parts", "score"],
                },
            },
        )
        json_obj = json.loads(response.message.content[0].text)
        score = json_obj["score"]
        json_obj.pop("score", None)
        return json_obj, score
