import cohere
from dotenv import dotenv_values
import json

math_aa_generator_v1 = "d9276017-6281-446d-bfab-f8158a6c4969-ft"


class AAMathGenerator:
    def __init__(self):
        config = dotenv_values(".env")
        self.co = cohere.ClientV2(config.get("COHERE_KEY"))
        self.base_model_id = "command-a-03-2025"
        self.model_id = math_aa_generator_v1

    def generate_question(self, topic="Number and Algebra"):
        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You will generate a JSON called for a university level IB-style math question.
                    Strictly follow this format:
                    {
                        "content": string,
                        "marks": integer,
                        "markscheme": string,
                        "subtopics": array of strings
                    }
                    All mathematical expressions MUST be written in LaTeX.

                    Output must have the following fields:
                    - 'content' for the question string with equations and numbers in LaTeX.
                    - 'marks' for how many marks the question is worth, with more marks for harder questions.
                    - 'markscheme' for an IB-style markscheme string which focuses as much as possible on concise numerical steps with almost no word descriptions, showing the major computational steps in LaTeX to solve the problem while including exactly how marks are awarded.
                    - 'subtopics' for a list of IB subtopics that the question covers, which may overlap into other topics.
                    """,
                },
                {"role": "user", "content": topic},
            ],
            # response format is not supported for fine-tuned models, so we will enforce json with fix_json
        )
        return topic, response.message.content[0].text

    def fix_json(self, str, topic=None):
        response = self.co.chat(
            model=self.base_model_id,
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

    def judge_question(self, question):
        inputs = {
            "content": question["content"],
            "marks": question["marks"],
            "topic": question["topic"],
            "subtopics": question["subtopics"],
        }

        response = self.co.chat(
            model=self.base_model_id,
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
        print(response.message.content[0].text)
        return json.loads(response.message.content[0].text)

    def judge_markscheme(self, question):
        inputs = {
            "content": question["content"],
            "marks": question["marks"],
            "markscheme": question["markscheme"],
        }

        response = self.co.chat(
            model=self.base_model_id,
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
        print(response.message.content[0].text)
        return json.loads(response.message.content[0].text)

    def combine_json(self, master, new):
        """
        Updates the master dictionary with values from new,
        but only for keys that already exist in master.
        Extra keys in new are ignored.
        """
        return {key: new.get(key, master[key]) for key in master}

    def generate(self, topic="Number and algebra", max_iterations=3, acceptable_score=95):
        question_str = self.generate_question(topic)
        question = self.fix_json(question_str, topic)

        for i in range(max_iterations):
            judged_question = self.judge_question(question)
            question = self.combine_json(question, judged_question)

            if judged_question["score"] >= acceptable_score:
                break

        for i in range(max_iterations):
            judged_markscheme = self.judge_markscheme(question)
            question = self.combine_json(question, judged_markscheme)

            if judged_markscheme["score"] >= acceptable_score:
                break

        return question


generator = AAMathGenerator()
print(generator.generate())
