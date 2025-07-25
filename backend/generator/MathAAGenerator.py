import cohere
from dotenv import dotenv_values
import formatter
import judge


class MathAAGenerator:
    def __init__(self):
        math_aa_generator_v2 = "e89238d1-6894-48a0-944c-011fd837df78-ft"
        self.model_id = math_aa_generator_v2
        self.base_model_id = "command-a-03-2025"

        config = dotenv_values(".env")
        self.co = cohere.ClientV2(config.get("COHERE_KEY"), log_warning_experimental_features=False)
        self.KEY_LIMIT = 10

        self.formatter = formatter.MathAAFormatter(self.co, self.base_model_id)
        self.judge = judge.AAMathJudge(self.co, self.base_model_id)

    def generate_question(self, topic="Number and Algebra"):
        response = self.co.chat(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": """
                    
                    You are an assistant that generates IB-style advanced high school and early university math questions and markschemes. 
                    All mathematical expressions MUST be written in valid LaTeX format. 

                    You will generate a JSON object with a field 'topic' and a list called 'parts', where each element is a sub-question. 
                    Strictly follow this format:
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
                    The whole object must have:
                    - 'topic': the subtopic of the question within the user's requested topic.
                    - 'parts': a list of sub-questions, where each sub-question is a JSON object.

                    Each sub-question must have:
                    - 'content': a clear and challenging question string with equations and numbers in LaTeX.
                    - 'marks': how many marks the question is worth, with more marks for harder questions.
                    - 'markscheme': an IB-style markscheme string which focuses as much as possible on concise numerical steps
                                    with almost no word descriptions, showing the major computational steps in LaTeX to solve the 
                                    problem while including exactly how marks are awarded.
                    - 'subtopics': a list of IB subtopics that the question covers, which may overlap into other topics.
                    - 'order': an integer indicating the order of the question in the topic, counting up from 1

                    Make sure all questions and answers are rigorous and well-aligned with the IB Math syllabus.
                    Make a large variety of questions. If the question has mutliple parts, incorporate different subjects and topics.
                    Some variations include: integration, sequences, limits, proofs, probabilities, etc.
                    """,
                },
                {"role": "user", "content": topic},
            ],
            # response format is not supported for fine-tuned models, so we will enforce json with fix_json
        )
        return response.message.content[0].text

    def generate(self, topic="Calculus", level="SL", max_iterations=2, acceptable_score=95):
        print("Generating...")
        question_str = self.generate_question(topic)
        question = self.formatter.fix_json(question_str, topic)

        print(f"Judging question...")
        for _ in range(max_iterations):
            question, score = self.judge.judge_question(question)

            if score >= acceptable_score:
                break

        print(f"Judging markscheme...")
        for _ in range(max_iterations):
            question, score = self.judge.judge_markscheme(question)

            if score >= acceptable_score:
                break

        print("Question finalized")
        return self.formatter.finalize_json(question)
