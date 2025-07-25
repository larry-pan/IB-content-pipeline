import cohere
from dotenv import dotenv_values
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import formatter
import judge


class CSGenerator:
    def __init__(self):
        # math_aa_generator_v2 = "e89238d1-6894-48a0-944c-011fd837df78-ft"
        # self.model_id = math_aa_generator_v2
        self.base_model_id = "command-a-03-2025"

        config = dotenv_values(".env")
        self.co = cohere.ClientV2(config.get("COHERE_KEY"), log_warning_experimental_features=False)
        self.KEY_LIMIT = 10

        self.Formatter = formatter.CSFormatter(self.co, self.base_model_id)
        # self.Judge = judge.AAMathJudge(self.co, self.base_model_id)

    def generate_question(self, topic="Problem-solving and Programming"):
        response = self.co.chat(
            model=self.base_model_id,
            messages=[
                {
                    "role": "system",
                    "content": """You are an assistant that generates IB-style Computer Science questions and markschemes. Topics and subtopics are:
                     You must output a JSON as follows:
                      {
                        "question": string,
                        "options": [
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
                      System Fundamentals: Systems in organizations, System design basics  
                      Computer Organization: Computer organization  
                      Networks: Networks  
                      Computational Thinking: Computational Thinking, 
                      Problem-solving and Programming: General principles, Connecting computational thinking and program design, Introduction to programming  
                      Abstract Data Structures: Abstract data structures  
                      Resource Management: Resource management  
                      Control: Control

                      Each subquestion may test different topics than the main topic, so combine different topics.
                      All coding questions should be in pseudocode.
                      You will generate a JSON object containing the string 'question' and the list called 'options', where each element is a subquestion. Each sub-question must have:
                        - 'question': General info that introduces the subquestions.
                        - 'content': a clear and challenging question string that tests of one or more
                        - 'marks': how many marks the question is worth, with more marks for questions requiring deeper analysis or discussion.
                        - 'markscheme': an IB-style markscheme string that shows acceptable answers with mark allocations in the format 'Award [X max]' followed by bullet points of acceptable responses, using semicolons to separate alternative answers and including specific technical terminology.
                        - 'subtopics': a list of relevant subtopics that the subquestion covers.
                        - 'order': an integer indicating the order of the question in the topic, counting up from 1
                      """,
                },
                {"role": "user", "content": topic},
            ],
            # response format is not supported for fine-tuned models, so we will enforce json with fix_json
        )
        print(response)
        return response.message.content[0].text

    def generate(
        self, topic="Problem-solving and Programming", max_iterations=2, acceptable_score=95
    ):
        print("Generating")
        question_str = self.generate_question(topic)
        print("Formatting")
        question = self.Formatter.fix_json(question_str, topic)
        print(f"Initial '{topic}' question generated")
        print("------------")
        print(question)
        print("------------\n\n\n")

        # for _ in range(max_iterations):
        #     question, score = self.Judge.judge_question(question)

        #     if score >= acceptable_score:
        #         break

        # print("Question finalized")
        # print("------------")
        # print(question)
        # print("------------\n\n\n")

        # for _ in range(max_iterations):
        #     question, score = self.Judge.judge_markscheme(question)

        #     if score >= acceptable_score:
        #         break

        # print("Markscheme finalized")

        return self.Formatter.finalize_json(question)
