# AI-Lara QLoRA training from Google Colab (phone-friendly)

This is a **starter experiment**, not a claim that AI-Lara is already trained. It fine-tunes the open-weight `Qwen/Qwen2.5-1.5B-Instruct` base model using 4-bit QLoRA and saves only the small adapter. The model card lists Apache-2.0 licensing; review the model card and terms before deployment: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct. QLoRA uses 4-bit quantization plus trainable LoRA adapters; see https://huggingface.co/docs/peft/developer_guides/quantization.

## Important limitations

- The curated seed dataset is only 40 examples. It proves the pipeline can be exercised; it is far too small for a useful production model and may overfit badly.
- This first model learns a narrow JSON specification task, **not complete Kotlin code generation and not APK compilation**.
- Outputs must be validated. Do not deploy generated code or connect this adapter to the public API without evaluation and safety checks.
- Colab GPU availability varies by account and session. The script requires a CUDA GPU; no GPU means training will stop with a clear message.
- The held-out test set is saved after training. It is not used for gradient updates. Run evaluation and inspect every prediction.

## Run from an Android phone

1. Open https://colab.research.google.com/ in Chrome. If needed, enable **Desktop site** in Chrome's menu.
2. Create a new notebook.
3. In **Runtime → Change runtime type**, select a GPU accelerator (T4 if available), then save.
4. Run these cells in order. If Colab disconnects, reconnect and rerun the setup cells.

### Cell 1 — install libraries

```python
!pip -q install -U "transformers>=4.46,<5" "peft>=0.13" "accelerate>=1.1" "bitsandbytes>=0.44" "safetensors"
```

### Cell 2 — connect Google Drive to preserve the adapter

```python
from google.colab import drive
drive.mount('/content/drive')
```

### Cell 3 — download the repository

```python
!git clone https://github.com/thatosenyum95-ship-it/AI-Lara.git /content/AI-Lara
```

If the folder already exists after a reconnect, use `!git -C /content/AI-Lara pull` instead.

### Cell 4 — validate the dataset

```python
!python /content/AI-Lara/training/validate_dataset.py
```

### Cell 5 — train

```python
%env AILARA_OUTPUT_DIR=/content/drive/MyDrive/AI-Lara-Training/adapter
!python /content/AI-Lara/training/train_qlora.py
```

The first run downloads the base model and can take time. Keep the Colab tab open while training. The adapter, tokenizer, summary, and held-out test file are saved in Google Drive.

### Cell 6 — evaluate the held-out examples

```python
%env AILARA_OUTPUT_DIR=/content/drive/MyDrive/AI-Lara-Training/adapter
!python /content/AI-Lara/training/evaluate.py
```

Check JSON validity and feature/screen matches; read the printed predictions. Since the test set is tiny, results are only a first signal. Add more varied, human-reviewed examples, rerun training, and compare against the existing rule-based baseline.

## Dataset format

Each line of `examples.jsonl` is one JSON object with `prompt` and `target`. Targets contain `project_name`, `features`, and `screens`, aligned to the first training task. The trainer deterministically splits the examples into train, validation, and held-out test subsets.

## Next engineering step

After the model is demonstrably better than the rule-based baseline, implement a dedicated model inference adapter and strict JSON/schema validation in `backend/main.py`. Keep the current deterministic generator as fallback. Do not claim APK creation until a real Android build succeeds for each generated project.
