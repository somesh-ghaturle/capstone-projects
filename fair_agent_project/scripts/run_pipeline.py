from agents.orchestrator import Orchestrator

def main():
    orchestrator = Orchestrator()

    finance_context = "The earnings report shows a revenue increase of 15%."
    finance_question = "What is the percentage revenue growth?"

    medical_context = "The patient exhibits symptoms of fever and cough with a history of asthma."
    medical_question = "What could be the most likely diagnosis?"

    finance_answer = orchestrator.route_query("finance", finance_context, finance_question)
    medical_answer = orchestrator.route_query("medicine", medical_context, medical_question)

    print("Finance Agent Answer:", finance_answer)
    print("Medical Agent Answer:", medical_answer)

if __name__ == "__main__":
    main()