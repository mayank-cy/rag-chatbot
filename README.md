# RAG based chatbot

## Extraction:

First, the input file is converted to markdown using the `mineru` library.

This makes hierarchal chunking downstream easier.

```bash
pip install "mineru[all]"

chmod +x run_extraction.sh

./run_extraction.sh <input documents dir> <output dir>
```

## Hierarchial chunking:

```
python preprocessing.py
```

