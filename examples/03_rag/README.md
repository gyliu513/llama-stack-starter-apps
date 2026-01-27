## RAG

### Simple RAG (`01_simple_rag.py`)

Basic RAG using the file_search tool.

```bash
python -m examples.03_rag.01_simple_rag localhost 8321
```

### Multi-source RAG (`02_multi_source_rag.py`)

RAG across two vector stores using file_search.

```bash
python -m examples.03_rag.02_multi_source_rag localhost 8321
```

### RAG with Metadata (`03_rag_with_metadata.py`)

Filter file_search results by metadata attributes.

```bash
python -m examples.03_rag.03_rag_with_metadata localhost 8321 --source doc_a
```

### Chunking Strategies (`04_chunking_strategies.py`)

Compare different chunk sizes for the same document.

```bash
python -m examples.03_rag.04_chunking_strategies localhost 8321
```

### Hybrid Search (`05_hybrid_search.py`)

Combine file_search with web_search in one response.

```bash
python -m examples.03_rag.05_hybrid_search localhost 8321
```

