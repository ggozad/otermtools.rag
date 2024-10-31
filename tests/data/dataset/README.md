A very small (10 entries) subset of https://huggingface.co/datasets/neural-bridge/rag-dataset-12000

To generate 

```python
from datasets import load_dataset
ds = load_dataset("neural-bridge/rag-dataset-12000", split="train")
small = ds.select(range(0,10))
small.save_to_disk(".")
```