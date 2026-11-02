"""
L2 — The RAG Architecture: Prompt Builder  (STARTER)
======================================================
Run with:
    python prompt_builder.py

Your goal: build the prompt assembly step of a RAG pipeline.

Required features:
    1. A SYSTEM_PROMPT string that instructs the model to:
       - Answer ONLY from the provided context
       - Say "I don't have enough information" when the answer isn't in the context
       - Cite sources by name
    2. A format_chunks(chunks) function that formats a list of chunk dicts into
       a single context string — each chunk labelled with its source
    3. A build_prompt(question, chunks) function that returns the complete
       assembled prompt as a string (system prompt + context + question)
    4. A token_estimate(text) helper that returns characters // 4
    5. A run_test(question, chunks) function that assembles and prints the
       full prompt + token count
    6. At least 2 test cases with different questions and chunk sets

Key concepts:
    Chunk dict format:
        {"text": "...", "source": "filename.txt", "distance": 0.42}

    Prompt assembly pattern:
        [System prompt]
        CONTEXT:
        [Source: doc1.txt]
        <chunk text>

        ---

        [Source: doc2.txt]
        <chunk text>
        USER QUESTION: <question>

    Token estimate:
        A rough approximation: len(text) // 4
        (GPT-4 uses ~4 chars per token on average)
"""

# ── System prompt ──────────────────────────────────────────────────────────
# TODO: Write a SYSTEM_PROMPT string that instructs the model to:
#   - Answer ONLY from the context provided
#   - Say "I don't have enough information" if the answer isn't present
#   - Cite sources by mentioning the document name
# Define rules that keep AI answers grounded in retrieved documents.

SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.
If the context does not contain enough information, say:
"I don't have enough information to answer that question."

Cite the source documents by filename when answering.
Do not invent facts or use outside information.
"""


# ── Helpers ────────────────────────────────────────────────────────────────

def format_chunks(chunks: list[dict]) -> str:
    """Format a list of chunk dicts into a context string."""
    # TODO: For each chunk, produce:
    #   [Source: <chunk["source"]>]
    #   <chunk["text"]>
    # Separate chunks with "\n\n---\n\n"

    # Format each retrieved chunk with its source for citation tracking.
    formatted = []

    for chunk in chunks:
        source = chunk["source"]
        text = chunk["text"]

        formatted.append(f"[Source: {source}]\n{text}")

    return "\n\n---\n\n".join(formatted)


def token_estimate(text: str) -> int:
    """Rough token count estimate: characters // 4."""
    # TODO: return len(text) // 4

    # Estimate token usage using approximately 4 characters per token.
    return len(text) // 4


def build_prompt(question: str, chunks: list[dict]) -> str:
    """Assemble the full RAG prompt."""
    # TODO: Combine SYSTEM_PROMPT, "CONTEXT:\n" + format_chunks(chunks),
    #   and "USER QUESTION: " + question into one string

    # Convert retrieved document chunks into labeled context. 
    context = format_chunks(chunks)

    # Combine system instructions, retreived context, and the user question. 
    full_prompt = (
        f"SYSTEM:\n{SYSTEM_PROMPT}\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"USER QUESTION:\n{question}\n\n"
        "ANSWER:"
    )

    # Return the completed prompt for the LLM.
    return full_prompt


# ── Test runner ────────────────────────────────────────────────────────────

def run_test(question: str, chunks: list[dict]) -> None:
    """Assemble and print a prompt with token estimate."""
    # TODO: Call build_prompt(), print the result, print the token estimate
        
    # Build the complete prompt from the question and retrieved chunks.
    full_prompt = build_prompt(question, chunks)

    # Estimate how many tokens the prompt would use.
    estimated_tokens = token_estimate(full_prompt)

    # Display the assembled prompt and estimated token count.
    print("\n" + "=" * 60)
    print("ASSEMBLED RAG PROMPT")
    print("=" * 60)
    print(full_prompt)
    print(f"\nEstimated Tokens: {estimated_tokens}")


# ── Test cases ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    
    # Test 1: Assemble a prompt about FastAPI authentication.
    question_1 = "How does JWT authentication protect API endpoints?"

    chunks_1 = [
        {
            "source": "module5_auth.md",
            "text": "JWT tokens verify user identity before granting access."
        },
        {
            "source": "module5_fastapi.md",
            "text": "FastAPI uses dependencies to protect authenticated routes."
        }
    ]

    run_test(question_1, chunks_1)

    # Test 2: Assemble a prompt about semantic search.
    question_2 = "How does ChromaDB support semantic search?"

    chunks_2 = [
        {
            "source": "module7_chromadb.md",
            "text": "ChromaDB stores document embeddings for similarity searches."
        },
        {
            "source": "module7_embeddings.md",
            "text": "Embeddings represent text as numerical vectors."
        }
    ]

    run_test(question_2, chunks_2)
