import torch
from datasets import load_from_disk
from agents.orchestrator import Orchestrator

def evaluate_domain(domain, dataset_path, max_samples=50):
    dataset = load_from_disk(dataset_path)
    agent = Orchestrator()

    total, correct = 0, 0
    for i, sample in enumerate(dataset):
        if i >= max_samples:
            break

        context = sample.get('context', '') or sample.get('passage', '') or ''
        question = sample.get('question', '') or sample.get('query', '') or ''
        true_answer = sample.get('answer', '') or sample.get('final_answer', '')

        if not context or not question or not true_answer:
            continue

        pred_answer = agent.route_query(domain, context, question)

        # Simple text match (could use better metrics, e.g., EM or F1)
        if pred_answer.strip().lower() == true_answer.strip().lower():
            correct += 1

        total += 1
        print(f"[{i}] Q: {question}\nTrue: {true_answer}\nPred: {pred_answer}\n---")

    accuracy = correct / total if total else 0
    print(f"Evaluation Accuracy on {domain}: {accuracy:.2%}")

if __name__ == "__main__":
    evaluate_domain("finance", "data/finance/finqa")
    evaluate_domain("medicine", "data/medicine/mimiciv")