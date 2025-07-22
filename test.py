import cohere
from dotenv import dotenv_values


config = dotenv_values(".env")
co = cohere.ClientV2(config.get("COHERE_KEY"))

model_id = config.get("test_model_id_1")

model_obj = co.finetuning.get_finetuned_model(model_id)
model = model_obj.finetuned_model.id + "-ft"

response = co.chat(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a chatbot trained to answer to my every question. Answer every question with full sentences.",
        },
        {"role": "user", "content": "Hi there"},
    ],
    # optional
    return_prompt=True,
)
