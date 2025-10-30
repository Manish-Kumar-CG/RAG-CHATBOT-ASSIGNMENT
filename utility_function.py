from opensearchpy import OpenSearch
from google.genai.types import EmbedContentConfig 

def create_opensearch_client() -> OpenSearch:
    cluster_url = f"https://localhost:9200"
    client = OpenSearch(
        hosts=[cluster_url],
        http_auth=("admin", "admin"),
        use_ssl=True,
        verify_certs= False
    )
    return client


def embed_text_with_gemini(user_query: str, Client):
    response = Client.models.embed_content(
        model="gemini-embedding-001",
        contents=user_query,
        config=EmbedContentConfig(output_dimensionality=384)
    )
    return response


def search_similar_qa(client: OpenSearch, query_embedding: list,
) -> list:
    search_body = {
        "size": 4,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": 4
                }
            }
        },
        "_source": False,
        "fields": ["question", "answer"]
    }

    result = client.search(index = "questions_embeddings", body=search_body)
    text_results = []

    if "hits" in result and "hits" in result["hits"]:
        for hit in result["hits"]["hits"]:
            fields = hit.get("fields", {})
            question = fields.get("question", [""])[0]
            answer = fields.get("answer", [""])[0]
            text_results.append({"question": question, "answer": answer})

    return text_results

def build_prompt(user_query: str, text_results: list) -> str:
    prompt = [f"""System: You are an Aurora Airline Customer Support Assistant. Based on the following FAQ data, answer the user query after analyzing it..
    User Query: {user_query}
    Instructions:
    - Answer the question in a helpful, conversational tone.
    - Use the information provided in the FAQ data only.
    - If the answer is not found in the FAQ data, respond with: "I have no information related to this.
    - Provide a clear, friendly response.
    FAQ DATA starts from here:
"""]

    for result in text_results:
        result_text = f"Question: {result['question']}\nAnswer: {result['answer']}\n\n"
        prompt[0] += result_text

    return prompt[0]

def get_gemini_response(google_client, prompt: str) -> str:
    response = google_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text