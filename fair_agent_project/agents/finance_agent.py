from transformers import pipeline

class FinanceAgent:
    def __init__(self, model_name="meta-llama/Llama-2-7b-hf"):
        self.generator = pipeline("text-generation", model=model_name)

    def answer_question(self, context: str, question: str) -> str:
        prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
        responses = self.generator(prompt, max_length=150, do_sample=False)
        answer = responses[0]['generated_text'].split("Answer:")[-1].strip()
        return answer