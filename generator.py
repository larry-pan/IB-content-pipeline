import cohere
from dotenv import dotenv_values
import json


class AAMathGenerator:
    def __init__(self):
        config = dotenv_values(".env")
        self.co = cohere.ClientV2(config.get("COHERE_KEY"))
        self.model_id = "command-a-03-2025"

    def generate_question(self, topic="Number and algebra"):
        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": "You will generate the JSON list called 'parts' for an advanced high school math question which may have several sub-questions. All mathematical expressions MUST be written in LaTeX.The field 'parts' contains a list of JSON objects, each representing one subquestion. Every element of 'parts' must have the following fields:  - 'content' for the question string with equations and numbers in latex. - 'marks' for how many marks the question is worth, with more marks for harder questions. - 'markscheme' for an IB-style markscheme string which focuses as much as possible on concise numerical steps with almost no word descriptions, showing the major computational steps in latex to solve the problem while including exactly how mark are awarded. - 'subtopics' for a list of IB subtopics that the question covers, which may overlap into other topics.",
                },
                {"role": "user", "content": topic},
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
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": "You are a judge for IB math questions. You must output JSON with the new 'content' and 'subtopics' if they can be improved and an integer 'score' from 0-100. This is based on the following factors:\n"
                    "- The content has no LaTex errors.\n"
                    "- The question covers the specified topic and subtopics, without missing any or including concepts outside the topics.\n"
                    "- The question make sense and is solvable\n"
                    "DO NOT add anything to the fields that does not explicitly fix a problem.",
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
                    "content": "You are a judge for IB math markschemes. You must output JSON with the new 'content', 'marks', and 'markscheme' if they can be improved and an integer 'score' from 0-100 indicating how well the original quetion conforms to the guidelines. This is based on the following factors:\n"
                    "- The markscheme has no mathematical errors and answers the question correctly.\n"
                    "- The markscheme is as concise as possible, with no very limited and only strictly needed explaination.\n"
                    "- The markscheme focuses as much as possible on numerical steps, with almost no word descriptions.\n"
                    "- The markscheme clearly distributes the correct number of marks to the correct steps.\n"
                    "DO NOT add anything to the fields that does not explicitly fix a problem.",
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

    def combine_json(self, master, new):
        """
        Updates the master dictionary with values from new,
        but only for keys that already exist in master.
        Extra keys in new are ignored.
        """
        return {key: new.get(key, master[key]) for key in master}

    def generate(self, topic="Number and algebra", max_iterations=3, acceptable_score=95):
        question = self.generate_question(topic)
        final = question

        for i in range(max_iterations):
            judged_question = self.judge_question(question)
            question = self.combine_json(question, judged_question)

            if judged_question["score"] >= acceptable_score:
                break

        for i in range(max_iterations):
            judged_markscheme = self.judge_markscheme(question)
            final = self.combine_json(question, judged_markscheme)

            if judged_markscheme["score"] >= acceptable_score:
                break

        return final


generator = AAMathGenerator()
print(generator.generate())
