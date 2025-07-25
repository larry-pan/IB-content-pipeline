import cohere
from dotenv import dotenv_values
import formatter
import judge


class AAMathGenerator:
    def __init__(self):
        math_aa_generator_v1 = "d9276017-6281-446d-bfab-f8158a6c4969-ft"
        self.model_id = math_aa_generator_v1
        self.base_model_id = "command-a-03-2025"

        config = dotenv_values(".env")
        self.co = cohere.ClientV2(config.get("COHERE_KEY"), log_warning_experimental_features=False)
        self.KEY_LIMIT = 10

        self.formatter = formatter.Formatter(self.co, self.base_model_id)
        self.judge = judge.AAMathJudge(self.co, self.base_model_id)

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

    def generate(self, topic="Number and algebra", max_iterations=3, acceptable_score=95):

        question_str = self.generate_question(topic)
        question = self.formatter.fix_json(question_str, topic)
        print(f"Initial '{topic}' question generated")

        for _ in range(max_iterations):
            judged_question = self.judge.judge_question(question)
            question = self.formatter.combine_json(question, judged_question)

            if judged_question["score"] >= acceptable_score:
                break
        print("Question finalized")

        for _ in range(max_iterations):
            judged_markscheme = self.judge.judge_markscheme(question)
            question = self.formatter.combine_json(question, judged_markscheme)

            if judged_markscheme["score"] >= acceptable_score:
                break
        print("Markscheme finalized")

        return question
