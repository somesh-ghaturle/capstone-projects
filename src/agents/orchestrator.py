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
            'doctor', 'physician', 'nurse', 'surgery', 'cancer', 'diabetes',
            'blood', 'heart', 'brain', 'infection', 'virus', 'bacteria',
            'pharmaceutical', 'biomedical', 'pathology', 'anatomy'
        ]
        
        # Count keyword matches
        finance_score = sum(1 for keyword in finance_keywords if keyword in query_lower)
        medical_score = sum(1 for keyword in medical_keywords if keyword in query_lower)
        
        # Determine domain based on scores
        if finance_score > medical_score and finance_score > 0:
            return QueryDomain.FINANCE
        elif medical_score > finance_score and medical_score > 0:
            return QueryDomain.MEDICAL
        elif finance_score > 0 and medical_score > 0:
            return QueryDomain.CROSS_DOMAIN if self.enable_cross_domain else QueryDomain.FINANCE
        else:
            # Use heuristics for edge cases
            return self._heuristic_classification(query)
    
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
        
        if finance_matches > medical_matches:
            return QueryDomain.FINANCE
        elif medical_matches > finance_matches:
            return QueryDomain.MEDICAL
        else:
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
        # Default to finance agent with low confidence
        finance_response = self.finance_agent.query(query, context)
        
        return OrchestratedResponse(
            primary_answer=f"Domain unclear. Attempted finance analysis: {finance_response.answer}",
            domain=QueryDomain.UNKNOWN,
            confidence_score=0.3,  # Low confidence for unknown domain
            finance_response=finance_response,
            routing_explanation="Query domain unclear, defaulted to Finance Agent with reduced confidence"
        )
    
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