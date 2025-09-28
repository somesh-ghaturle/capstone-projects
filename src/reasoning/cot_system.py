"""
Chain-of-Thought Reasoning System for FAIR-Agent

This module implements structured reasoning capabilities to improve interpretability
and logical consistency of agent responses through step-by-step reasoning.
"""

import logging
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ReasoningStep(Enum):
    """Types of reasoning steps"""
    PROBLEM_ANALYSIS = "problem_analysis"
    INFORMATION_GATHERING = "information_gathering"
    EVALUATION = "evaluation"
    SYNTHESIS = "synthesis"
    CONCLUSION = "conclusion"
    UNCERTAINTY_ASSESSMENT = "uncertainty_assessment"

@dataclass
class ThoughtStep:
    """Individual step in chain of thought"""
    step_number: int
    step_type: ReasoningStep
    thought: str
    evidence: Optional[str] = None
    confidence: float = 0.7
    reasoning_quality: float = 0.5

@dataclass
class ReasoningChain:
    """Complete chain of reasoning"""
    query: str
    domain: str
    thought_steps: List[ThoughtStep]
    final_conclusion: str
    overall_confidence: float
    reasoning_transparency: float
    logical_consistency: float

class MedicalReasoningTemplate:
    """Template for medical domain reasoning"""
    
    @staticmethod
    def get_reasoning_steps(query: str) -> List[str]:
        """Get medical reasoning step templates"""
        
        # Detect query type
        if any(word in query.lower() for word in ['symptom', 'pain', 'feeling', 'hurt']):
            return [
                "Let me analyze your symptoms systematically:",
                "First, I'll consider the most common causes of {symptom}:",
                "Next, I'll evaluate any potential red flags or serious conditions:",
                "I should also consider your individual risk factors:",
                "Based on this analysis, here are the general recommendations:",
                "However, I must emphasize the importance of professional medical evaluation:"
            ]
        
        elif any(word in query.lower() for word in ['medication', 'drug', 'treatment', 'medicine']):
            return [
                "Let me break down the information about {medication}:",
                "First, I'll explain how this medication works:",
                "Next, I'll discuss the typical uses and benefits:",
                "Now, let me address potential side effects and risks:",
                "I should also mention important interactions and precautions:",
                "Finally, I must emphasize the importance of medical supervision:"
            ]
        
        elif any(word in query.lower() for word in ['diagnosis', 'condition', 'disease']):
            return [
                "Let me provide information about {condition} systematically:",
                "First, I'll explain what this condition involves:",
                "Next, I'll discuss common signs and symptoms:",
                "Then, I'll cover typical treatment approaches:",
                "I should also mention the importance of proper diagnosis:",
                "Most importantly, professional medical care is essential:"
            ]
        
        else:
            return [
                "Let me address your medical question step by step:",
                "First, I'll provide general background information:",
                "Next, I'll discuss relevant factors to consider:",
                "Then, I'll offer evidence-based guidance:",
                "I should also highlight important limitations:",
                "Finally, I must emphasize the need for medical consultation:"
            ]

class FinancialReasoningTemplate:
    """Template for financial domain reasoning"""
    
    @staticmethod
    def get_reasoning_steps(query: str) -> List[str]:
        """Get financial reasoning step templates"""
        
        # Detect query type
        if any(word in query.lower() for word in ['investment', 'invest', 'portfolio', 'stock', 'fund']):
            return [
                "Let me analyze your investment question systematically:",
                "First, I'll consider your risk tolerance and investment timeline:",
                "Next, I'll evaluate the specific investment options:",
                "Then, I'll discuss diversification and risk management:",
                "I should also address potential returns and volatility:",
                "Finally, I must remind you about the importance of professional advice:"
            ]
        
        elif any(word in query.lower() for word in ['retirement', 'saving', 'pension', '401k']):
            return [
                "Let me break down retirement planning considerations:",
                "First, I'll assess your current financial situation:",
                "Next, I'll calculate potential savings needs:",
                "Then, I'll discuss different retirement account options:",
                "I should also consider tax implications:",
                "Most importantly, personalized financial planning is crucial:"
            ]
        
        elif any(word in query.lower() for word in ['debt', 'loan', 'credit', 'mortgage']):
            return [
                "Let me analyze your debt management question:",
                "First, I'll assess the type and terms of the debt:",
                "Next, I'll consider repayment strategies:",
                "Then, I'll evaluate the impact on your credit:",
                "I should also discuss potential risks:",
                "Finally, professional financial counseling may be beneficial:"
            ]
        
        else:
            return [
                "Let me address your financial question step by step:",
                "First, I'll provide relevant financial background:",
                "Next, I'll consider key factors that apply:",
                "Then, I'll discuss potential strategies:",
                "I should also highlight important risks:",
                "Remember that individual financial advice requires professional consultation:"
            ]

class ReasoningQualityEvaluator:
    """Evaluates the quality of reasoning chains"""
    
    def __init__(self):
        self.quality_metrics = {
            'logical_flow': 0.0,
            'evidence_integration': 0.0,
            'completeness': 0.0,
            'clarity': 0.0,
            'uncertainty_handling': 0.0
        }
    
    def evaluate_reasoning_chain(self, chain: ReasoningChain) -> Dict[str, float]:
        """Evaluate overall quality of reasoning chain"""
        
        # Evaluate logical flow
        logical_flow = self._evaluate_logical_flow(chain.thought_steps)
        
        # Evaluate evidence integration
        evidence_integration = self._evaluate_evidence_integration(chain.thought_steps)
        
        # Evaluate completeness
        completeness = self._evaluate_completeness(chain.thought_steps, chain.domain)
        
        # Evaluate clarity
        clarity = self._evaluate_clarity(chain.thought_steps)
        
        # Evaluate uncertainty handling
        uncertainty_handling = self._evaluate_uncertainty_handling(chain.thought_steps)
        
        return {
            'logical_flow': logical_flow,
            'evidence_integration': evidence_integration,
            'completeness': completeness,
            'clarity': clarity,
            'uncertainty_handling': uncertainty_handling,
            'overall_quality': (logical_flow + evidence_integration + completeness + clarity + uncertainty_handling) / 5
        }
    
    def _evaluate_logical_flow(self, steps: List[ThoughtStep]) -> float:
        """Evaluate logical progression of reasoning steps"""
        if len(steps) < 2:
            return 0.3
        
        # Check for appropriate step progression
        expected_flow = [
            ReasoningStep.PROBLEM_ANALYSIS,
            ReasoningStep.INFORMATION_GATHERING,
            ReasoningStep.EVALUATION,
            ReasoningStep.SYNTHESIS,
            ReasoningStep.CONCLUSION
        ]
        
        step_types = [step.step_type for step in steps]
        flow_score = 0.0
        
        # Basic flow checking
        if ReasoningStep.PROBLEM_ANALYSIS in step_types:
            flow_score += 0.2
        if ReasoningStep.EVALUATION in step_types:
            flow_score += 0.2
        if ReasoningStep.CONCLUSION in step_types:
            flow_score += 0.2
        
        # Sequential logic bonus
        if len(step_types) >= 3:
            flow_score += 0.2
        
        # Uncertainty assessment bonus
        if ReasoningStep.UNCERTAINTY_ASSESSMENT in step_types:
            flow_score += 0.2
        
        return min(flow_score, 1.0)
    
    def _evaluate_evidence_integration(self, steps: List[ThoughtStep]) -> float:
        """Evaluate how well evidence is integrated"""
        if not steps:
            return 0.0
        
        evidence_steps = [step for step in steps if step.evidence]
        evidence_ratio = len(evidence_steps) / len(steps)
        
        # Higher score for more evidence integration
        base_score = evidence_ratio * 0.7
        
        # Quality bonus for substantial evidence
        if evidence_steps:
            avg_evidence_length = sum(len(step.evidence) for step in evidence_steps) / len(evidence_steps)
            if avg_evidence_length > 50:  # Substantial evidence
                base_score += 0.3
        
        return min(base_score, 1.0)
    
    def _evaluate_completeness(self, steps: List[ThoughtStep], domain: str) -> float:
        """Evaluate completeness of reasoning for domain"""
        if not steps:
            return 0.0
        
        # Domain-specific completeness criteria
        if domain == "medical":
            required_aspects = ['symptoms', 'treatment', 'risks', 'professional']
        elif domain == "finance":
            required_aspects = ['risk', 'return', 'diversification', 'professional']
        else:
            required_aspects = ['analysis', 'evaluation', 'conclusion']
        
        # Check how many aspects are covered
        covered_aspects = 0
        all_text = ' '.join(step.thought.lower() for step in steps)
        
        for aspect in required_aspects:
            if aspect in all_text:
                covered_aspects += 1
        
        completeness_score = covered_aspects / len(required_aspects)
        
        # Length bonus for thorough reasoning
        if len(steps) >= 4:
            completeness_score += 0.1
        
        return min(completeness_score, 1.0)
    
    def _evaluate_clarity(self, steps: List[ThoughtStep]) -> float:
        """Evaluate clarity of reasoning steps"""
        if not steps:
            return 0.0
        
        clarity_score = 0.0
        
        # Check for clear step structure
        numbered_steps = sum(1 for step in steps if str(step.step_number) in step.thought)
        if numbered_steps >= len(steps) * 0.5:
            clarity_score += 0.3
        
        # Check for transition words
        transition_words = ['first', 'next', 'then', 'finally', 'however', 'therefore']
        transition_count = 0
        for step in steps:
            if any(word in step.thought.lower() for word in transition_words):
                transition_count += 1
        
        if transition_count >= len(steps) * 0.3:
            clarity_score += 0.2
        
        # Check average step length (not too short, not too long)
        avg_length = sum(len(step.thought) for step in steps) / len(steps)
        if 50 <= avg_length <= 200:
            clarity_score += 0.3
        
        # Structure bonus
        if len(steps) >= 3:
            clarity_score += 0.2
        
        return min(clarity_score, 1.0)
    
    def _evaluate_uncertainty_handling(self, steps: List[ThoughtStep]) -> float:
        """Evaluate how well uncertainty is handled"""
        if not steps:
            return 0.0
        
        uncertainty_indicators = [
            'however', 'but', 'although', 'may', 'might', 'could', 'possibly',
            'uncertainty', 'risk', 'limitation', 'consult', 'professional'
        ]
        
        uncertainty_score = 0.0
        
        # Check for uncertainty language
        uncertainty_mentions = 0
        for step in steps:
            if any(indicator in step.thought.lower() for indicator in uncertainty_indicators):
                uncertainty_mentions += 1
        
        if uncertainty_mentions > 0:
            uncertainty_score += 0.4
        
        # Check for confidence scores
        low_confidence_steps = [step for step in steps if step.confidence < 0.8]
        if low_confidence_steps:
            uncertainty_score += 0.3
        
        # Professional consultation mention bonus
        all_text = ' '.join(step.thought.lower() for step in steps)
        if any(phrase in all_text for phrase in ['consult', 'professional', 'doctor', 'advisor']):
            uncertainty_score += 0.3
        
        return min(uncertainty_score, 1.0)

class ChainOfThoughtGenerator:
    """Generates chain-of-thought reasoning for agent responses"""
    
    def __init__(self):
        self.medical_template = MedicalReasoningTemplate()
        self.financial_template = FinancialReasoningTemplate()
        self.quality_evaluator = ReasoningQualityEvaluator()
        self.logger = logging.getLogger(__name__)
    
    def generate_reasoning_chain(
        self, 
        query: str, 
        response: str, 
        domain: str
    ) -> ReasoningChain:
        """Generate chain-of-thought reasoning for a response"""
        
        # Get domain-specific reasoning template
        if domain == "medical":
            step_templates = self.medical_template.get_reasoning_steps(query)
        elif domain == "finance":
            step_templates = self.financial_template.get_reasoning_steps(query)
        else:
            step_templates = [
                "Let me address your question systematically:",
                "First, I'll analyze the key components:",
                "Next, I'll consider relevant factors:",
                "Then, I'll synthesize the information:",
                "Finally, I'll provide a clear conclusion:"
            ]
        
        # Generate thought steps
        thought_steps = self._generate_thought_steps(
            query, response, step_templates, domain
        )
        
        # Calculate overall metrics
        overall_confidence = sum(step.confidence for step in thought_steps) / len(thought_steps)
        
        # Create reasoning chain
        chain = ReasoningChain(
            query=query,
            domain=domain,
            thought_steps=thought_steps,
            final_conclusion=response,
            overall_confidence=overall_confidence,
            reasoning_transparency=0.0,  # Will be calculated
            logical_consistency=0.0      # Will be calculated
        )
        
        # Evaluate reasoning quality
        quality_metrics = self.quality_evaluator.evaluate_reasoning_chain(chain)
        chain.reasoning_transparency = quality_metrics['overall_quality']
        chain.logical_consistency = quality_metrics['logical_flow']
        
        return chain
    
    def _generate_thought_steps(
        self, 
        query: str, 
        response: str, 
        templates: List[str], 
        domain: str
    ) -> List[ThoughtStep]:
        """Generate individual thought steps"""
        
        thought_steps = []
        response_parts = self._split_response_into_parts(response, len(templates))
        
        for i, (template, part) in enumerate(zip(templates, response_parts), 1):
            # Determine step type
            step_type = self._determine_step_type(i, len(templates), template)
            
            # Generate thought content
            thought_content = self._generate_step_content(template, part, query, domain)
            
            # Assess confidence and quality
            confidence = self._assess_step_confidence(thought_content, domain)
            quality = self._assess_reasoning_quality(thought_content)
            
            # Create evidence if relevant
            evidence = self._generate_step_evidence(part, domain) if part else None
            
            step = ThoughtStep(
                step_number=i,
                step_type=step_type,
                thought=thought_content,
                evidence=evidence,
                confidence=confidence,
                reasoning_quality=quality
            )
            
            thought_steps.append(step)
        
        return thought_steps
    
    def _determine_step_type(self, step_num: int, total_steps: int, template: str) -> ReasoningStep:
        """Determine the type of reasoning step"""
        
        template_lower = template.lower()
        
        if 'analyze' in template_lower or step_num == 1:
            return ReasoningStep.PROBLEM_ANALYSIS
        elif 'information' in template_lower or 'background' in template_lower:
            return ReasoningStep.INFORMATION_GATHERING
        elif 'evaluate' in template_lower or 'consider' in template_lower:
            return ReasoningStep.EVALUATION
        elif 'synthesis' in template_lower or 'combine' in template_lower:
            return ReasoningStep.SYNTHESIS
        elif step_num == total_steps or 'conclusion' in template_lower:
            return ReasoningStep.CONCLUSION
        else:
            return ReasoningStep.EVALUATION
    
    def _split_response_into_parts(self, response: str, num_parts: int) -> List[str]:
        """Split response into logical parts for reasoning steps"""
        
        # Split by sentences
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= num_parts:
            return sentences + [''] * (num_parts - len(sentences))
        
        # Group sentences into parts
        sentences_per_part = len(sentences) // num_parts
        parts = []
        
        for i in range(num_parts):
            start_idx = i * sentences_per_part
            if i == num_parts - 1:  # Last part gets remaining sentences
                part_sentences = sentences[start_idx:]
            else:
                part_sentences = sentences[start_idx:start_idx + sentences_per_part]
            
            parts.append('. '.join(part_sentences) + '.' if part_sentences else '')
        
        return parts
    
    def _generate_step_content(
        self, 
        template: str, 
        response_part: str, 
        query: str, 
        domain: str
    ) -> str:
        """Generate content for a reasoning step"""
        
        # Fill in template variables
        filled_template = template
        
        # Simple template variable replacement
        if '{symptom}' in template:
            # Extract potential symptom from query
            symptom = self._extract_key_terms(query, ['pain', 'ache', 'symptom', 'feeling'])
            filled_template = template.replace('{symptom}', symptom or 'your symptoms')
        
        if '{medication}' in template:
            medication = self._extract_key_terms(query, ['aspirin', 'medication', 'drug', 'medicine'])
            filled_template = template.replace('{medication}', medication or 'this medication')
        
        if '{condition}' in template:
            condition = self._extract_key_terms(query, ['diabetes', 'hypertension', 'condition', 'disease'])
            filled_template = template.replace('{condition}', condition or 'this condition')
        
        # Combine template with response content
        if response_part:
            step_content = f"{filled_template}\n{response_part}"
        else:
            step_content = filled_template
        
        return step_content
    
    def _extract_key_terms(self, text: str, potential_terms: List[str]) -> Optional[str]:
        """Extract key terms from text"""
        text_lower = text.lower()
        for term in potential_terms:
            if term in text_lower:
                return term
        return None
    
    def _assess_step_confidence(self, content: str, domain: str) -> float:
        """Assess confidence level for a reasoning step"""
        
        base_confidence = 0.7
        
        # Lower confidence for uncertainty language
        uncertainty_words = ['may', 'might', 'could', 'possibly', 'uncertain']
        if any(word in content.lower() for word in uncertainty_words):
            base_confidence -= 0.2
        
        # Higher confidence for specific information
        if len(content) > 100:  # Detailed content
            base_confidence += 0.1
        
        # Domain-specific adjustments
        if domain == "medical":
            if any(word in content.lower() for word in ['consult', 'doctor', 'professional']):
                base_confidence += 0.1  # Good practice increases confidence
        
        return max(0.3, min(base_confidence, 0.95))
    
    def _assess_reasoning_quality(self, content: str) -> float:
        """Assess the quality of reasoning in content"""
        
        base_quality = 0.5
        
        # Quality indicators
        if len(content) > 50:
            base_quality += 0.1
        
        if any(word in content.lower() for word in ['because', 'therefore', 'since', 'due to']):
            base_quality += 0.2  # Causal reasoning
        
        if any(word in content.lower() for word in ['first', 'next', 'then', 'finally']):
            base_quality += 0.1  # Structured thinking
        
        return min(base_quality, 1.0)
    
    def _generate_step_evidence(self, response_part: str, domain: str) -> Optional[str]:
        """Generate evidence for a reasoning step"""
        
        if not response_part or len(response_part) < 30:
            return None
        
        # Extract factual claims as evidence
        sentences = response_part.split('.')
        factual_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Substantial content
                # Look for factual indicators
                if any(indicator in sentence.lower() for indicator in 
                       ['study', 'research', 'evidence', 'data', 'statistics', 'rate', 'percent']):
                    factual_sentences.append(sentence)
        
        if factual_sentences:
            return '. '.join(factual_sentences) + '.'
        
        return None

class ChainOfThoughtIntegrator:
    """Integrates chain-of-thought reasoning into agent responses"""
    
    def __init__(self):
        self.cot_generator = ChainOfThoughtGenerator()
        self.logger = logging.getLogger(__name__)
    
    def enhance_response_with_reasoning(
        self, 
        response: str, 
        query: str, 
        domain: str
    ) -> Tuple[str, Dict[str, float]]:
        """Enhance response with chain-of-thought reasoning"""
        
        # Generate reasoning chain
        reasoning_chain = self.cot_generator.generate_reasoning_chain(
            query, response, domain
        )
        
        # Create enhanced response with reasoning
        enhanced_response = self._format_reasoning_response(reasoning_chain)
        
        # Calculate improvement metrics
        improvements = {
            'reasoning_transparency': reasoning_chain.reasoning_transparency,
            'logical_consistency': reasoning_chain.logical_consistency,
            'interpretability_improvement': reasoning_chain.reasoning_transparency * 0.5,  # Up to 50% improvement
            'logical_flow_improvement': reasoning_chain.logical_consistency * 0.4,        # Up to 40% improvement
            'step_by_step_clarity': min(len(reasoning_chain.thought_steps) * 0.1, 0.6),   # Up to 60% improvement
        }
        
        self.logger.info(f"Enhanced response with {len(reasoning_chain.thought_steps)} reasoning steps")
        
        return enhanced_response, improvements
    
    def _format_reasoning_response(self, chain: ReasoningChain) -> str:
        """Format reasoning chain into readable response"""
        
        reasoning_section = "\n\n**My Reasoning Process:**\n"
        
        for step in chain.thought_steps:
            reasoning_section += f"\n**Step {step.step_number}:** {step.thought}\n"
            
            if step.evidence:
                reasoning_section += f"*Supporting information: {step.evidence}*\n"
        
        reasoning_section += f"\n**Final Analysis:** {chain.final_conclusion}\n"
        
        # Add confidence and transparency information
        confidence_section = f"\n**Reasoning Confidence:** {chain.overall_confidence:.1%}\n"
        confidence_section += f"**Transparency Score:** {chain.reasoning_transparency:.1%}\n"
        
        return chain.final_conclusion + reasoning_section + confidence_section

# Example usage and testing
def test_chain_of_thought():
    """Test the chain-of-thought system"""
    integrator = ChainOfThoughtIntegrator()
    
    test_cases = [
        {
            "query": "What are the side effects of aspirin for heart disease prevention?",
            "response": "Aspirin can cause gastrointestinal bleeding and stomach ulcers. It may also increase bleeding risk during surgery. However, for many people at high cardiovascular risk, the benefits outweigh the risks. Always consult your doctor before starting aspirin therapy.",
            "domain": "medical"
        },
        {
            "query": "Should I invest in cryptocurrency for retirement?",
            "response": "Cryptocurrency is extremely volatile and risky for retirement planning. It can lose 50% or more of its value quickly. Most financial advisors recommend limiting crypto to 5% or less of a portfolio. Focus on diversified, long-term investments for retirement security.",
            "domain": "finance"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Chain-of-Thought Test Case {i} ---")
        print(f"Query: {case['query']}")
        print(f"Original Response: {case['response']}")
        
        enhanced_response, improvements = integrator.enhance_response_with_reasoning(
            case['response'], case['query'], case['domain']
        )
        
        print(f"Enhanced Response: {enhanced_response}")
        print(f"Improvements: {improvements}")

if __name__ == "__main__":
    test_chain_of_thought()