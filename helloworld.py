import time
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

# prepare the model input
prompt = "Give me a short introduction to large language models."
messages = [
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=True   # Switches between thinking and non-thinking modes.
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# conduct text completion
t1 = time.time()
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=32768
)
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
t2 = time.time()
print(f"Generated {len(output_ids)} tokens in {(t2 - t1):.2f} seconds.")
tks_per_sec = len(output_ids) / (t2 - t1)
print(f"({tks_per_sec:.2f} tokens/second)\n")
# the result will begin with thinking content in <think></think> tags,
# followed by the actual response
print(tokenizer.decode(output_ids, skip_special_tokens=True))
