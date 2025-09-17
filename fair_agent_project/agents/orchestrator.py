from agents.finance_agent import FinanceAgent
from agents.medical_agent import MedicalAgent

class Orchestrator:
    def __init__(self, finance_model_name=None, medical_model_name=None):
        self.finance_agent = FinanceAgent(model_name=finance_model_name or "meta-llama/Llama-2-7b-hf")
        self.medical_agent = MedicalAgent(model_name=medical_model_name or "google/biobert_v1.1_pubmed")

    def route_query(self, domain: str, context: str, question: str) -> str:
        if domain.lower() == "finance":
            return self.finance_agent.answer_question(context, question)
        elif domain.lower() == "medicine":
            return self.medical_agent.answer_question(context, question)
        else:
            raise ValueError(f"Unsupported domain: {domain}")