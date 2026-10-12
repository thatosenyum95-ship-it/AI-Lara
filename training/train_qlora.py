"""Small, Colab-friendly QLoRA trainer for AI-Lara's app-spec JSON task.

Input JSONL rows: {"prompt": "...", "target": {"project_name": "...", "features": [...], "screens": [...]}}
Only the adapter is saved; the base model is not copied into the output folder.
"""
import json, os, random
from pathlib import Path

import torch
from torch.utils.data import Dataset
from transformers import (
    AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
    Trainer, TrainingArguments, set_seed
)
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model

ROOT = Path(__file__).resolve().parent
DATA_PATH = Path(os.environ.get("AILARA_DATA_PATH", ROOT / "examples.jsonl"))
OUTPUT_DIR = Path(os.environ.get("AILARA_OUTPUT_DIR", "/content/drive/MyDrive/AI-Lara-Training/adapter"))
MODEL_ID = os.environ.get("AILARA_BASE_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
MAX_LENGTH = int(os.environ.get("AILARA_MAX_LENGTH", "768"))
SEED = 42
SYSTEM_PROMPT = (
    "Kamu adalah AI-Lara, asisten perancang spesifikasi aplikasi Android. "
    "Balas hanya dengan JSON valid berisi tepat tiga kunci: project_name (string), "
    "features (array string), screens (array string). Gunakan fitur yang didukung: "
    "search, login, notes, todo, camera, calculator, offline, notifications, profile, database. "
    "Screens wajib berisi home; gunakan login, notes, tasks, profile, calculator, camera "
    "sesuai fitur yang relevan. Jangan sertakan markdown atau teks di luar JSON."
)

def read_rows():
    rows=[]
    for line_no,line in enumerate(DATA_PATH.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line)
        if not row.get("prompt") or not isinstance(row.get("target"),dict):
            raise ValueError(f"Baris {line_no} tidak punya prompt/target")
        rows.append(row)
    if len(rows)<20:
        raise ValueError(f"Butuh setidaknya 20 contoh untuk menjalankan baseline; ditemukan {len(rows)}")
    # Shuffle deterministically, then hold out separate validation and test samples.
    random.Random(SEED).shuffle(rows)
    test_n=max(2,round(len(rows)*0.1)); val_n=max(2,round(len(rows)*0.1))
    if test_n+val_n >= len(rows): raise ValueError("Dataset terlalu kecil untuk split.")
    train_rows=rows[:len(rows)-test_n-val_n]
    val_rows=rows[len(rows)-test_n-val_n:len(rows)-test_n]
    test_rows=rows[len(rows)-test_n:]
    return train_rows,val_rows,test_rows

class TokenDataset(Dataset):
    def __init__(self, rows, tokenizer):
        self.items=[]
        for row in rows:
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":row["prompt"]},
            ]
            prompt_ids=tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
            full_messages=messages+[{"role":"assistant","content":json.dumps(row["target"],ensure_ascii=False,separators=(",",":"))}]
            full_ids=tokenizer.apply_chat_template(full_messages,tokenize=True,add_generation_prompt=False)
            if len(full_ids)>MAX_LENGTH:
                raise ValueError(f"Contoh terlalu panjang ({len(full_ids)} token), prompt: {row['prompt']}")
            labels=list(full_ids)
            labels[:len(prompt_ids)]=[-100]*min(len(prompt_ids),len(labels))
            self.items.append({"input_ids":torch.tensor(full_ids,dtype=torch.long),"labels":torch.tensor(labels,dtype=torch.long)})
    def __len__(self): return len(self.items)
    def __getitem__(self,index): return self.items[index]

class PadCollator:
    def __init__(self, pad_id): self.pad_id=pad_id
    def __call__(self,items):
        width=max(x["input_ids"].numel() for x in items)
        ids=torch.full((len(items),width),self.pad_id,dtype=torch.long)
        labels=torch.full((len(items),width),-100,dtype=torch.long)
        mask=torch.zeros((len(items),width),dtype=torch.long)
        for i,item in enumerate(items):
            n=item["input_ids"].numel()
            ids[i,:n]=item["input_ids"]; labels[i,:n]=item["labels"]; mask[i,:n]=1
        return {"input_ids":ids,"labels":labels,"attention_mask":mask}

def main():
    if not torch.cuda.is_available():
        raise SystemExit("GPU tidak ditemukan. Di Google Colab pilih Runtime > Change runtime type > T4 GPU, lalu jalankan ulang.")
    set_seed(SEED)
    train_rows,val_rows,test_rows=read_rows()
    print(f"Model: {MODEL_ID}; contoh train={len(train_rows)}, validasi={len(val_rows)}, test={len(test_rows)}")
    tokenizer=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=True)
    if tokenizer.pad_token_id is None: tokenizer.pad_token=tokenizer.eos_token
    compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    qconfig=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=compute_dtype)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=qconfig,device_map="auto",torch_dtype=compute_dtype,trust_remote_code=True)
    model.config.use_cache=False
    model=prepare_model_for_kbit_training(model)
    lora=LoraConfig(r=16,lora_alpha=32,lora_dropout=0.05,bias="none",task_type="CAUSAL_LM",target_modules="all-linear")
    model=get_peft_model(model,lora)
    model.print_trainable_parameters()
    train_ds=TokenDataset(train_rows,tokenizer); val_ds=TokenDataset(val_rows,tokenizer)
    args=TrainingArguments(
        output_dir=str(OUTPUT_DIR / "checkpoints"),
        num_train_epochs=float(os.environ.get("AILARA_EPOCHS","3")),
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        logging_steps=2,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=compute_dtype==torch.float16,
        bf16=compute_dtype==torch.bfloat16,
        gradient_checkpointing=True,
        optim="paged_adamw_8bit",
        report_to="none",
        seed=SEED,
        data_seed=SEED,
        remove_unused_columns=False,
    )
    trainer=Trainer(model=model,args=args,train_dataset=train_ds,eval_dataset=val_ds,data_collator=PadCollator(tokenizer.pad_token_id))
    trainer.train()
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    (OUTPUT_DIR/"training_summary.json").write_text(json.dumps({
        "base_model":MODEL_ID,"method":"QLoRA (4-bit NF4 + LoRA adapters)",
        "train_examples":len(train_rows),"validation_examples":len(val_rows),"held_out_test_examples":len(test_rows),
        "epochs":args.num_train_epochs,"max_length":MAX_LENGTH,
        "note":"Held-out test examples were not used for training; run evaluate.py before deployment."
    },ensure_ascii=False,indent=2),encoding="utf-8")
    test_file=OUTPUT_DIR/"held_out_test.jsonl"
    test_file.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in test_rows)+"\n",encoding="utf-8")
    print(f"Adapter tersimpan di: {OUTPUT_DIR}")
    print("Langkah berikutnya: jalankan evaluate.py terhadap held_out_test.jsonl. Jangan integrasikan ke API sebelum hasilnya ditinjau.")

if __name__=="__main__": main()
