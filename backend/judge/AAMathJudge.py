import json


class AAMathJudge:
    def __init__(self, co, model_id):
        self.co = co
        self.model_id = model_id

    def judge_question(self, question):
        inputs = {
            "content": question["content"],
            "marks": question["marks"],
            "topic": question["topic"],
            "subtopics": question["subtopics"],
        }

        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are a judge for IB math questions. 
                        You must output a JSON with the new 'content' and 'subtopics' if they can be improved and an integer 'score' from 0-100. 
                        Strictly follow this format:
                        {
                            "content": string,
                            "marks": integer,
                            "subtopics": array of strings,
                            "score": integer
                        }
                        This is based on the following factors:
                        - The content has no LaTeX errors.
                        - The question covers the specified topic and subtopics, without missing any or including concepts outside the topics.
                        - The question make sense and is solvable
                        DO NOT add anything to the fields that does not explicitly fix a problem.
                        """,
                },
                {"role": "user", "content": str(inputs)},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "subtopics": {"type": "array", "items": {"type": "string"}},
                        "score": {"type": "integer"},
                    },
                    "required": ["content", "subtopics", "score"],
                },
            },
        )
        return json.loads(response.message.content[0].text)

    def judge_markscheme(self, question):
        inputs = {
            "content": question["content"],
            "marks": question["marks"],
            "markscheme": question["markscheme"],
        }

        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a judge for IB math markschemes. 
                    You must output a JSON with the new 'content', 'marks', 
                    and 'markscheme' if they can be improved and an integer 'score' from 0-100 
                    indicating how well the original question conforms to the guidelines. 
                    Strictly follow this format:
                    {
                        "content": string,
                        "marks": integer,
                        "markscheme": string,
                        "score": integer
                    }

                    This is based on the following factors:
                    - The markscheme has no mathematical errors and answers the question correctly.
                    - The markscheme is as concise as possible, with very limited and only strictly needed explanation.
                    - The markscheme focuses as much as possible on numerical steps, with almost no word descriptions.
                    - The markscheme clearly distributes the correct number of marks to the correct steps by marking a step with [M1], [M2], etc.
                    DO NOT add anything to the fields that does not explicitly fix a problem.""",
                },
                {"role": "user", "content": str(inputs)},
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "marks": {"type": "integer"},
                        "markscheme": {"type": "string"},
                        "score": {"type": "integer"},
                    },
                    "required": ["content", "marks", "markscheme", "score"],
                },
            },
        )
        return json.loads(response.message.content[0].text)
