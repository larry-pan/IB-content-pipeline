import cohere
from dotenv import dotenv_values
import json

MODEL_NAME = "test-finetune-model"
config = dotenv_values(".env")
co = cohere.ClientV2(config.get("COHERE_KEY"))


def normalize_spaces(text):
    """
    Normalize leading spaces and remove unnecessary indentation in multi-line strings.
    Keeps line breaks, trims each line.
    """
    lines = text.strip().splitlines()
    cleaned_lines = [line.strip() for line in lines]
    return "\n".join(cleaned_lines)


def convert_dataset_format(nested_dataset):
    """
    Convert nested dataset format to flattened format
    """
    converted_messages = []

    for message in nested_dataset["messages"]:
        if message["role"] == "System":
            # Keep system messages as is
            converted_messages.append({"role": "System", "content": message["content"]})
        elif message["role"] == "User":
            # Keep user messages as is
            converted_messages.append({"role": "User", "content": "Numbers and Algebra"})
        elif message["role"] == "Chatbot":
            # Flatten the nested content structure
            content_dict = message["content"]

            # Create the flattened content string
            flattened_content = f"""
            content: {content_dict['content']}
            marks: {content_dict['marks']}
            markscheme: {content_dict['markscheme']}
            subtopics: {content_dict['subtopics']}
            topic: {content_dict['topic']}
            """

            # Create the flattened message
            flattened_message = {"role": "Chatbot", "content": normalize_spaces(flattened_content)}

            converted_messages.append(flattened_message)

    output = {"messages": converted_messages}
    return output


with open("output.json", "w") as f:
    json.dump(convert_dataset_format(eval_data), f)
