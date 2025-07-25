import cohere
from dotenv import dotenv_values
from cohere.finetuning import Settings, FinetunedModel, BaseModel
from pathlib import Path

MODEL_NAME = "cs-generator-v1"
training_path = Path("data/compsci/training.jsonl")
eval_path = Path("data/compsci/eval.jsonl")


config = dotenv_values(Path("../.env"))
co = cohere.ClientV2(config.get("COHERE_KEY"))

chat_dataset = co.datasets.create(
    name="cs-dataset",
    data=open(training_path, "rb"),
    eval_data=open(eval_path, "rb"),
    type="chat-finetune-input",
)
result = co.wait(chat_dataset)
print(result)

print("------------")
create_response = co.finetuning.create_finetuned_model(
    request=FinetunedModel(
        name=MODEL_NAME,
        settings=Settings(
            base_model=BaseModel(
                base_type="BASE_TYPE_CHAT",
            ),
            dataset_id=chat_dataset.id,
        ),
    ),
)
print(create_response)
