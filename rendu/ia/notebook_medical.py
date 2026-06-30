# Fine-Tuning Médical Expérimental (LoRA / QLoRA)
# Ce code est conçu pour être exécuté dans Google Colab avec un GPU (T4 ou supérieur).

# 1. Installation des dépendances requises dans Colab
# !pip install -q transformers bitsandbytes peft accelerate datasets trl

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from datasets import load_dataset
from trl import SFTTrainer

# Configuration
MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"
DATASET_NAME = "ruslanmv/ai-medical-chatbot"
OUTPUT_DIR = "./phi3.5-medical-lora"

print("🧠 Chargement du tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

print("💾 Chargement et formatage du dataset médical...")
# Charger le dataset médical
dataset = load_dataset(DATASET_NAME, split="train")

# Formater pour Phi-3.5 instruct (Instruction -> Output)
def format_prompts(batch):
    formatted_texts = []
    for q, a in zip(batch['Patient'], batch['Doctor']):
        text = f"<|user|>\n{q}<|end|>\n<|assistant|>\n{a}<|end|>"
        formatted_texts.append(text)
    return {"text": formatted_texts}

dataset = dataset.map(format_prompts, batched=True)
# Spliter pour validation
dataset_split = dataset.train_test_split(test_size=0.1)

print("⚡ Configuration de la quantification 4-bit...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

print("🧠 Chargement du modèle de base Phi-3.5...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
model = prepare_model_for_kbit_training(model)

print("🔧 Configuration de LoRA...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["qkv_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)

print("🚀 Configuration du Trainer et entraînement...")
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    max_steps=100, # Limité pour une expérimentation rapide et économie de ressources
    fp16=True,
    optim="paged_adamw_8bit"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset_split["train"],
    eval_dataset=dataset_split["test"],
    dataset_text_field="text",
    max_seq_length=512,
    tokenizer=tokenizer,
    args=training_args,
)

trainer.train()
print("🎉 Entraînement terminé ! Adaptateurs LoRA sauvegardés.")
trainer.model.save_pretrained(OUTPUT_DIR)
