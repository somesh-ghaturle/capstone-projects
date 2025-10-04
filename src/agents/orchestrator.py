"""
Orchestrator Module for FAIR-Agent System

This module implements the central orchestrator that coordinates between
finance and medical agents, handles query routing, response aggregation,
and cross-domain reasoning tasks.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from enum import Enum
from dataclasses import dataclass
import re

from .finance_agent import FinanceAgent, FinanceResponse
from .medical_agent import MedicalAgent, MedicalResponse

class QueryDomain(Enum):
    """Enumeration of supported query domains"""
    FINANCE = "finance"
    MEDICAL = "medical"
    CROSS_DOMAIN = "cross_domain"
    UNKNOWN = "unknown"

@dataclass
class OrchestratedResponse:
    """Combined response from orchestrator"""
    primary_answer: str
    domain: QueryDomain
    confidence_score: float
    finance_response: Optional[FinanceResponse] = None
    medical_response: Optional[MedicalResponse] = None
    cross_domain_analysis: Optional[str] = None
    routing_explanation: str = ""

class Orchestrator:
    """
    Central orchestrator for FAIR-Agent system
    
    Responsibilities:
    - Query domain classification and routing
    - Agent coordination and response aggregation
    - Cross-domain reasoning and synthesis
    - Quality assessment and risk evaluation
    """
    
    def __init__(
        self,
        finance_config: Optional[Dict] = None,
        medical_config: Optional[Dict] = None,
        enable_cross_domain: bool = True
    ):
        """
        Initialize the Orchestrator
        
        Args:
            finance_config: Configuration for finance agent
            medical_config: Configuration for medical agent
            enable_cross_domain: Whether to enable cross-domain reasoning
        """
        self.logger = logging.getLogger(__name__)
        self.enable_cross_domain = enable_cross_domain
        
        # Initialize agents with provided configurations
        finance_config = finance_config or {}
        medical_config = medical_config or {}
        
        try:
            self.finance_agent = FinanceAgent(**finance_config)
            self.medical_agent = MedicalAgent(**medical_config)
            self.logger.info("Orchestrator initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize orchestrator: {e}")
            raise
    
    def process_query(
        self,
        query: str,
        context: Optional[Dict] = None,
        force_domain: Optional[QueryDomain] = None
    ) -> OrchestratedResponse:
        """
        Process a query through the appropriate agent(s)
        
        Args:
            query: The user query to process
            context: Additional context for the query
            force_domain: Force routing to specific domain (for testing)
            
        Returns:
            OrchestratedResponse with processed results
        """
        try:
            # Classify query domain
            domain = force_domain or self._classify_query_domain(query)
            
            # Route and process based on domain
            if domain == QueryDomain.FINANCE:
                return self._handle_finance_query(query, context)
            elif domain == QueryDomain.MEDICAL:
                return self._handle_medical_query(query, context)
            elif domain == QueryDomain.CROSS_DOMAIN:
                return self._handle_cross_domain_query(query, context)
            else:
                return self._handle_unknown_query(query, context)
                
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return OrchestratedResponse(
                primary_answer="Error processing query",
                domain=QueryDomain.UNKNOWN,
                confidence_score=0.0,
                routing_explanation=f"Error: {str(e)}"
            )
    
    def _classify_query_domain(self, query: str) -> QueryDomain:
        """
        Classify the domain of a query
        
        Args:
            query: The query text to classify
            
        Returns:
            QueryDomain classification
        """
        query_lower = query.lower()
        
        # Define domain keywords
        finance_keywords = [
            'financial', 'finance', 'money', 'investment', 'portfolio', 'stock',
            'market', 'revenue', 'profit', 'loss', 'budget', 'cost', 'price',
            'earnings', 'dividend', 'bond', 'asset', 'liability', 'cash flow',
            'roi', 'return on investment', 'valuation', 'financial statement'
        ]
        
        medical_keywords = [
            'medical', 'health', 'disease', 'symptom', 'treatment', 'diagnosis',
            'patient', 'clinical', 'drug', 'medication', 'therapy', 'hospital',
            'doctor', 'physician', 'nurse', 'surgery', 'cancer', 'diabetes', 'diabetic', 'diabetics',
            'blood', 'heart', 'brain', 'infection', 'virus', 'bacteria',
            'pharmaceutical', 'biomedical', 'pathology', 'anatomy', 'condition',
            'illness', 'syndrome', 'disorder', 'chronic', 'acute', 'pain',
            'fever', 'headache', 'medicine', 'vaccine', 'immunization',
            'hypertension', 'cholesterol', 'obesity', 'depression', 'anxiety',
            'asthma', 'arthritis', 'allergies', 'pneumonia', 'flu', 'covid'
        ]
        
        # Special case: single word "medicine" should strongly indicate medical domain
        if query_lower.strip() == 'medicine':
            return QueryDomain.MEDICAL
        
        # Count keyword matches
        finance_score = sum(1 for keyword in finance_keywords if keyword in query_lower)
        medical_score = sum(1 for keyword in medical_keywords if keyword in query_lower)
        
        # Determine domain based on scores with adaptive thresholds
        strong_threshold = 2  # For clear domain assignment
        weak_threshold = 1    # For single strong medical/finance terms
        
        # Strong domain classification with multiple matches
        if finance_score >= strong_threshold and finance_score > medical_score:
            return QueryDomain.FINANCE
        elif medical_score >= strong_threshold and medical_score > finance_score:
            return QueryDomain.MEDICAL
        elif finance_score >= strong_threshold and medical_score >= strong_threshold:
            return QueryDomain.CROSS_DOMAIN if self.enable_cross_domain else QueryDomain.FINANCE
        
        # Weak domain classification with single clear matches
        elif finance_score >= weak_threshold and finance_score > medical_score:
            # Always route clear finance terms directly
            return QueryDomain.FINANCE
        elif medical_score >= weak_threshold and medical_score > finance_score:
            # Always route clear medical terms directly  
            return QueryDomain.MEDICAL
        
        # Use heuristics for any remaining weak signals
        elif finance_score > 0 or medical_score > 0:
            return self._heuristic_classification(query)
        else:
            # No domain keywords found - treat as general query
            return QueryDomain.UNKNOWN
    
    def _heuristic_classification(self, query: str) -> QueryDomain:
        """Apply heuristic rules for edge case classification"""
        query_lower = query.lower()
        
        # Patterns that suggest finance
        finance_patterns = [
            r'\$[\d,]+', r'[\d,]+\s*dollars?', r'[\d.]+%', r'cost of',
            r'price of', r'revenue', r'profit', r'budget'
        ]
        
        # Patterns that suggest medical
        medical_patterns = [
            r'symptoms?', r'diagnos[ie]s', r'treatment', r'patient',
            r'mg\b', r'ml\b', r'dose', r'side effects?'
        ]
        
        finance_matches = sum(1 for pattern in finance_patterns if re.search(pattern, query_lower))
        medical_matches = sum(1 for pattern in medical_patterns if re.search(pattern, query_lower))
        
        # Only assign domain if there are clear pattern matches
        if finance_matches > 0 and finance_matches > medical_matches:
            return QueryDomain.FINANCE
        elif medical_matches > 0 and medical_matches > finance_matches:
            return QueryDomain.MEDICAL
        else:
            # No clear domain patterns - treat as general query
            return QueryDomain.UNKNOWN
    
    def _handle_finance_query(self, query: str, context: Optional[Dict]) -> OrchestratedResponse:
        """Handle finance-specific queries"""
        finance_response = self.finance_agent.query(query, context)
        
        return OrchestratedResponse(
            primary_answer=finance_response.answer,
            domain=QueryDomain.FINANCE,
            confidence_score=finance_response.confidence_score,
            finance_response=finance_response,
            routing_explanation="Query routed to Finance Agent based on financial keywords and patterns"
        )
    
    def _handle_medical_query(self, query: str, context: Optional[Dict]) -> OrchestratedResponse:
        """Handle medical-specific queries"""
        medical_response = self.medical_agent.query(query, context)
        
        return OrchestratedResponse(
            primary_answer=medical_response.answer,
            domain=QueryDomain.MEDICAL,
            confidence_score=medical_response.confidence_score,
            medical_response=medical_response,
            routing_explanation="Query routed to Medical Agent based on medical keywords and patterns"
        )
    
    def _handle_cross_domain_query(self, query: str, context: Optional[Dict]) -> OrchestratedResponse:
        """Handle queries that span both domains"""
        # Get responses from both agents
        finance_response = self.finance_agent.query(query, context)
        medical_response = self.medical_agent.query(query, context)
        
        # Synthesize cross-domain analysis
        cross_domain_analysis = self._synthesize_cross_domain_response(
            query, finance_response, medical_response
        )
        
        # Determine primary answer based on confidence scores
        if finance_response.confidence_score > medical_response.confidence_score:
            primary_answer = finance_response.answer
            confidence = finance_response.confidence_score
        else:
            primary_answer = medical_response.answer
            confidence = medical_response.confidence_score
        
        return OrchestratedResponse(
            primary_answer=primary_answer,
            domain=QueryDomain.CROSS_DOMAIN,
            confidence_score=confidence,
            finance_response=finance_response,
            medical_response=medical_response,
            cross_domain_analysis=cross_domain_analysis,
            routing_explanation="Query contains both financial and medical elements, processed by both agents"
        )
    
    def _handle_unknown_query(self, query: str, context: Optional[Dict]) -> OrchestratedResponse:
        """Handle queries that don't clearly fit any domain"""
        # For general queries, provide a general response without forcing domain-specific analysis
        general_response = self._generate_general_response(query)
        
        return OrchestratedResponse(
            primary_answer=general_response,
            domain=QueryDomain.UNKNOWN,
            confidence_score=0.7,  # Moderate confidence for general responses
            routing_explanation="Query identified as general topic, providing general knowledge response"
        )
    
    def _generate_general_response(self, query: str) -> str:
        """Generate a general response for non-domain-specific queries"""
        query_lower = query.lower()
        
        # Handle common general topics
        if "machine learning" in query_lower or "ml" in query_lower:
            return """Machine Learning is a subset of artificial intelligence (AI) that focuses on algorithms and statistical models that enable computers to improve their performance on tasks through experience without being explicitly programmed.

Key concepts include:
- **Supervised Learning**: Learning from labeled training data
- **Unsupervised Learning**: Finding patterns in data without labels  
- **Reinforcement Learning**: Learning through interaction with an environment
- **Deep Learning**: Using neural networks with multiple layers

Common applications include image recognition, natural language processing, recommendation systems, and predictive analytics. Machine learning is widely used across industries including finance, healthcare, technology, and research."""

        elif "artificial intelligence" in query_lower or "ai" in query_lower:
            return """Artificial Intelligence (AI) refers to computer systems that can perform tasks typically requiring human intelligence, such as learning, reasoning, problem-solving, and decision-making.

AI encompasses various approaches:
- **Machine Learning**: Systems that learn from data
- **Natural Language Processing**: Understanding and generating human language
- **Computer Vision**: Interpreting visual information
- **Robotics**: AI-powered physical systems
- **Expert Systems**: Knowledge-based decision support

AI applications are transforming industries by automating processes, enhancing decision-making, and enabling new capabilities in areas like healthcare diagnosis, financial analysis, autonomous vehicles, and personalized recommendations."""

        elif any(term in query_lower for term in ["diabetes", "diabetic", "cancer", "heart", "blood", "disease", "medical", "health"]):
            return f"""I notice your query appears to be medical in nature. While I can provide some general information, for detailed medical analysis, please rephrase your query to be more specific about the medical context.

For example, instead of "{query}", try:
- "What are the symptoms and treatment options for diabetes?"
- "How does diabetes affect blood sugar levels and what treatments are available?"
- "What are the medical complications associated with diabetes?"

This will route your query to our specialized Medical Agent for comprehensive, trustworthy medical analysis with proper safety assessments and evidence-based information.

**Important**: This system provides educational information only and should not replace professional medical advice. Always consult healthcare professionals for medical decisions."""

        elif "explain" in query_lower and any(word in query_lower for word in ["concept", "theory", "principle"]):
            return f"""I'd be happy to help explain this topic. However, for the most comprehensive and accurate information about '{query}', I recommend:

1. **Domain-Specific Analysis**: If this relates to finance or healthcare, please rephrase your query with domain-specific context for specialized insights.

2. **General Resources**: For broad topics, consider consulting academic sources, textbooks, or specialized educational platforms.

3. **Refined Query**: Try providing more specific context about what aspect you'd like explained.

The FAIR-Agent system is optimized for finance and medical domain queries, but I'm happy to provide general guidance where possible."""

        else:
            return f"""Thank you for your question about '{query}'. 

The FAIR-Agent system is specifically designed for finance and healthcare domain queries, where it can provide specialized, trustworthy analysis with comprehensive evaluation metrics.

For general topics like this, I recommend:
- **Finance-related queries**: Ask about investments, financial analysis, market trends, or economic topics
- **Medical queries**: Ask about health conditions, treatments, medical research, or healthcare topics
- **Cross-domain queries**: Ask about topics that intersect both domains

If your question relates to either domain, please rephrase it with that context for more detailed analysis. Otherwise, consider consulting general knowledge resources or educational platforms for comprehensive information on this topic."""
    
    def _synthesize_cross_domain_response(
        self,
        query: str,
        finance_response: FinanceResponse,
        medical_response: MedicalResponse
    ) -> str:
        """Synthesize insights from both finance and medical responses"""
        synthesis = f"""
Cross-Domain Analysis for: "{query}"

Financial Perspective:
- Answer: {finance_response.answer}
- Confidence: {finance_response.confidence_score:.2f}
- Risk Assessment: {finance_response.risk_assessment}

Medical Perspective:
- Answer: {medical_response.answer}
- Confidence: {medical_response.confidence_score:.2f}
- Safety Assessment: {medical_response.safety_assessment}

Integrated Insights:
"""
        
        # Add specific integration logic based on query type
        if "healthcare" in query.lower() and ("cost" in query.lower() or "budget" in query.lower()):
            synthesis += "This query involves healthcare economics, requiring both medical expertise and financial analysis."
        elif "pharmaceutical" in query.lower() and "investment" in query.lower():
            synthesis += "This query involves pharmaceutical investment analysis, combining medical knowledge with financial evaluation."
        else:
            synthesis += "This query requires interdisciplinary analysis combining medical and financial perspectives."
        
        return synthesis.strip()
    
    def evaluate_response_quality(self, response: OrchestratedResponse) -> Dict[str, float]:
        """
        Evaluate the quality of an orchestrated response
        
        Args:
            response: The orchestrated response to evaluate
            
        Returns:
            Dictionary of quality metrics
        """
        metrics = {
            'overall_confidence': response.confidence_score,
            'domain_clarity': 1.0 if response.domain != QueryDomain.UNKNOWN else 0.5,
            'response_completeness': self._assess_completeness(response),
            'safety_score': self._assess_safety(response)
        }
        
        # Calculate overall quality score
        metrics['overall_quality'] = sum(metrics.values()) / len(metrics)
        
        return metrics
    
    def _assess_completeness(self, response: OrchestratedResponse) -> float:
        """Assess completeness of the response"""
        completeness_score = 0.5  # Base score
        
        if response.primary_answer and len(response.primary_answer) > 20:
            completeness_score += 0.2
        
        if response.routing_explanation:
            completeness_score += 0.1
        
        if response.domain == QueryDomain.CROSS_DOMAIN and response.cross_domain_analysis:
            completeness_score += 0.2
        
        return min(1.0, completeness_score)
    
    def _assess_safety(self, response: OrchestratedResponse) -> float:
        """Assess safety of the response"""
        safety_score = 0.8  # Base safety score
        
        # Medical responses have additional safety considerations
        if response.medical_response:
            if "consult" in response.medical_response.safety_assessment.lower():
                safety_score += 0.2
            if "warning" in response.medical_response.safety_assessment.lower():
                safety_score -= 0.3
        
        # Financial responses with risk assessment
        if response.finance_response:
            if "high risk" in response.finance_response.risk_assessment.lower():
                safety_score -= 0.1
        
        return max(0.0, min(1.0, safety_score))