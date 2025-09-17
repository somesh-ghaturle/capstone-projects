#!/usr/bin/env python3
"""
Main Pipeline Script for FAIR-Agent System

This script runs the complete FAIR-Agent pipeline including:
- Agent initialization
- Query processing through orchestrator
- Response evaluation
- Logging and monitoring

Usage:
    python scripts/run_pipeline.py [--query "Your question"] [--interactive]
"""

import os
import sys
import yaml
import logging
import argparse
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents import FinanceAgent, MedicalAgent, Orchestrator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FAIRAgentPipeline:
    """Main pipeline for FAIR-Agent system"""
    
    def __init__(self, config_path: str = "./config/config.yaml"):
        """Initialize the pipeline with configuration"""
        self.config = self._load_config(config_path)
        self.orchestrator = None
        self._initialize_system()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'models': {
                'finance': {'name': 'gpt2', 'device': 'cpu'},
                'medical': {'name': 'gpt2', 'device': 'cpu'}
            },
            'orchestrator': {'enable_cross_domain': True}
        }
    
    def _initialize_system(self):
        """Initialize the FAIR-Agent system"""
        try:
            logger.info("Initializing FAIR-Agent system...")
            
            # Extract configurations
            finance_config = self.config.get('models', {}).get('finance', {})
            medical_config = self.config.get('models', {}).get('medical', {})
            
            # Initialize orchestrator
            self.orchestrator = Orchestrator(
                finance_config=finance_config,
                medical_config=medical_config,
                enable_cross_domain=self.config.get('orchestrator', {}).get('enable_cross_domain', True)
            )
            
            logger.info("FAIR-Agent system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize system: {e}")
            raise
    
    def process_query(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Process a single query through the system"""
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # Process through orchestrator
            response = self.orchestrator.process_query(query, context)
            
            # Evaluate response quality
            quality_metrics = self.orchestrator.evaluate_response_quality(response)
            
            # Prepare output
            output = {
                'query': query,
                'domain': response.domain.value,
                'primary_answer': response.primary_answer,
                'confidence_score': response.confidence_score,
                'routing_explanation': response.routing_explanation,
                'quality_metrics': quality_metrics
            }
            
            # Add domain-specific details
            if response.finance_response:
                output['finance_details'] = {
                    'reasoning_steps': response.finance_response.reasoning_steps,
                    'risk_assessment': response.finance_response.risk_assessment,
                    'numerical_outputs': response.finance_response.numerical_outputs
                }
            
            if response.medical_response:
                output['medical_details'] = {
                    'reasoning_steps': response.medical_response.reasoning_steps,
                    'safety_assessment': response.medical_response.safety_assessment,
                    'medical_evidence': response.medical_response.medical_evidence,
                    'uncertainty_indicators': response.medical_response.uncertainty_indicators
                }
            
            if response.cross_domain_analysis:
                output['cross_domain_analysis'] = response.cross_domain_analysis
            
            logger.info(f"Query processed successfully. Domain: {response.domain.value}")
            return output
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'query': query,
                'error': str(e),
                'domain': 'error',
                'primary_answer': 'Error processing query'
            }
    
    def run_interactive_mode(self):
        """Run the system in interactive mode"""
        print("=== FAIR-Agent Interactive Mode ===")
        print("Ask financial or medical questions. Type 'quit' to exit.\n")
        
        while True:
            try:
                # Get user input
                query = input("Your question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not query:
                    print("Please enter a question.\n")
                    continue
                
                # Process query
                print("\nProcessing...")
                result = self.process_query(query)
                
                # Display results
                self._display_result(result)
                print("\n" + "="*50 + "\n")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}\n")
    
    def _display_result(self, result: Dict):
        """Display query result in a formatted way"""
        print(f"\nDomain: {result['domain'].upper()}")
        print(f"Answer: {result['primary_answer']}")
        
        if 'confidence_score' in result:
            print(f"Confidence: {result['confidence_score']:.2f}")
        
        if 'routing_explanation' in result:
            print(f"Routing: {result['routing_explanation']}")
        
        # Display domain-specific details
        if 'finance_details' in result:
            finance = result['finance_details']
            print(f"\nFinancial Analysis:")
            print(f"  Risk: {finance.get('risk_assessment', 'N/A')}")
            if finance.get('numerical_outputs'):
                print(f"  Numbers: {finance['numerical_outputs']}")
        
        if 'medical_details' in result:
            medical = result['medical_details']
            print(f"\nMedical Analysis:")
            print(f"  Safety: {medical.get('safety_assessment', 'N/A')}")
            if medical.get('uncertainty_indicators'):
                print(f"  Uncertainties: {medical['uncertainty_indicators'][:2]}")
        
        if 'cross_domain_analysis' in result:
            print(f"\nCross-Domain Analysis:")
            # Display first few lines of cross-domain analysis
            lines = result['cross_domain_analysis'].split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  {line.strip()}")
        
        if 'quality_metrics' in result:
            quality = result['quality_metrics']
            print(f"\nQuality Score: {quality.get('overall_quality', 0):.2f}")
    
    def run_batch_queries(self, queries: List[str]) -> List[Dict]:
        """Run multiple queries in batch"""
        results = []
        
        for i, query in enumerate(queries, 1):
            logger.info(f"Processing query {i}/{len(queries)}")
            result = self.process_query(query)
            results.append(result)
        
        return results

def main():
    """Main function for script execution"""
    parser = argparse.ArgumentParser(description='Run FAIR-Agent pipeline')
    parser.add_argument(
        '--query',
        type=str,
        help='Single query to process'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--config',
        default='./config/config.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize pipeline
        pipeline = FAIRAgentPipeline(args.config)
        
        if args.query:
            # Process single query
            result = pipeline.process_query(args.query)
            pipeline._display_result(result)
        
        elif args.interactive:
            # Run interactive mode
            pipeline.run_interactive_mode()
        
        else:
            # Run demo queries
            demo_queries = [
                "What is the return on investment for Apple stock?",
                "What are the side effects of aspirin?",
                "How does healthcare spending affect pharmaceutical company profits?"
            ]
            
            print("=== FAIR-Agent Demo ===\n")
            
            for query in demo_queries:
                print(f"Query: {query}")
                result = pipeline.process_query(query)
                pipeline._display_result(result)
                print("\n" + "="*50 + "\n")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()