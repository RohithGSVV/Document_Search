import os
import numpy as np
import faiss

EMBEDDINGS_DIR = "../embeddings/embeddings_generated"
TITLE_EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "title_embeddings.npy")
ABSTRACT_EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "chunk_embeddings.npy")
CONTEXT_EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "context_embeddings.npy")

TITLE_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "title_faiss_index.idx")
ABSTRACT_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "chunk_faiss_index.idx")
CONTEXT_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "context_faiss_index.idx")

def create_faiss_index(embeddings_path, index_path):
    """
        Create a FAISS index from the given embeddings file and save it to disk.

        Args:
            embeddings_path (str): Path to the NumPy `.npy` file containing embeddings.
            index_path (str): Path to save the generated FAISS index file.

        Process:
            1. Load the embeddings from the `.npy` file.
            2. Convert the embeddings to `float32` (required by FAISS).
            3. Create a `faiss.IndexFlatL2` object (brute-force nearest neighbor search).
            4. Add the embeddings to the index.
            5. Save the index to the specified file path.

        Raises:
            Exception: If an error occurs during loading, indexing, or saving.
        """
    try:
        embeddings = np.load(embeddings_path).astype("float32")
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        faiss.write_index(index, index_path)
        print(f"FAISS index created and saved at {index_path}")
    except Exception as e:
        print(f"Error creating FAISS index for {embeddings_path}: {e}")

create_faiss_index(TITLE_EMBEDDINGS_PATH, TITLE_INDEX_PATH)
create_faiss_index(ABSTRACT_EMBEDDINGS_PATH, ABSTRACT_INDEX_PATH)
create_faiss_index(CONTEXT_EMBEDDINGS_PATH, CONTEXT_INDEX_PATH)
