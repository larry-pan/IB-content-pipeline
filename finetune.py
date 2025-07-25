import cohere
from dotenv import dotenv_values
from cohere.finetuning import Settings, FinetunedModel, BaseModel

MODEL_NAME = "test-finetune-model"


config = dotenv_values(".env")
co = cohere.ClientV2(config.get("COHERE_KEY"))

chat_dataset = co.datasets.create(
    name="chat-dataset-with-eval",
    data=open("training.jsonl", "rb"),
    eval_data=open("eval.jsonl", "rb"),
    type="chat-finetune-input",
)
result = co.wait(chat_dataset)
print(result)

print("------------")
create_response = co.finetuning.create_finetuned_model(
    request=FinetunedModel(
        name="math-aa-generator-v1",
        settings=Settings(
            base_model=BaseModel(
                base_type="BASE_TYPE_CHAT",
            ),
            dataset_id=chat_dataset.id,
        ),
    ),
)
print(create_response)
