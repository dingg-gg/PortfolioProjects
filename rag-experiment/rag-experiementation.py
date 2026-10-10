import ollama

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

# Each element is a tuple: (chunk, embedding)
VECTOR_DB = []


def load_dataset(path='cat-facts.txt'):
    with open(path, 'r') as file:
        # skip blank lines so we don't embed empty strings
        lines = [line.strip() for line in file if line.strip()]
    print(f'Loaded {len(lines)} entries')
    return lines


def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    return dot_product / (norm_a * norm_b)


def retrieve(query, top_n=3):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    similarities = [
        (chunk, cosine_similarity(query_embedding, embedding))
        for chunk, embedding in VECTOR_DB
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]


def main():
    dataset = load_dataset()

    for i, chunk in enumerate(dataset):
        add_chunk_to_database(chunk)
        print(f'Added chunk {i + 1}/{len(dataset)} to the database')

    while True:
        input_query = input('\nAsk me a question (or type "quit"): ').strip()
        if input_query.lower() in ('quit', 'exit', ''):
            break

        retrieved_knowledge = retrieve(input_query)

        print('Retrieved knowledge:')
        for chunk, similarity in retrieved_knowledge:
            print(f' - (similarity: {similarity:.2f}) {chunk}')

        context = '\n'.join(f' - {chunk}' for chunk, _ in retrieved_knowledge)
        instruction_prompt = (
            "You are a helpful chatbot.\n"
            "Use only the following pieces of context to answer the question. "
            "Don't make up any new information:\n"
            f"{context}\n"
        )

        stream = ollama.chat(
            model=LANGUAGE_MODEL,
            messages=[
                {'role': 'system', 'content': instruction_prompt},
                {'role': 'user', 'content': input_query},
            ],
            stream=True,
        )

        print('Chatbot response:')
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
        print()


if __name__ == '__main__':
    main()