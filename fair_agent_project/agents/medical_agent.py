from transformers import pipeline

class MedicalAgent:
    def __init__(self, model_name="google/biobert_v1.1_pubmed"):
        self.generator = pipeline("text-generation", model=model_name)

    def answer_question(self, context: str, question: str) -> str:
        prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
        responses = self.generator(prompt, max_length=150, do_sample=False)
        answer = responses[0]['generated_text'].split("Answer:")[-1].strip()
        return answer