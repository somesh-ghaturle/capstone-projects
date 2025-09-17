#!/usr/bin/env python3
"""
Medical Dataset Preprocessing Script for FAIR-Agent

This script downloads and preprocesses medical datasets including:
- MIMIC-IV: Medical Information Mart for Intensive Care
- PubMedQA: Biomedical Question Answering
- MedMCQA: Medical Multiple Choice Question Answering

Usage:
    python scripts/preprocess_medical.py [--dataset all|mimiciv|pubmedqa|medmcqa]
"""

import os
import sys
import yaml
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import warnings

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from datasets import load_dataset, Dataset
import pandas as pd
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MedicalDatasetPreprocessor:
    """Preprocessor for medical datasets"""
    
    def __init__(self, config_path: str = "./config/config.yaml"):
        """Initialize with configuration"""
        self.config = self._load_config(config_path)
        self.datasets_config = self.config['datasets']['medical']
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration if config file is missing"""
        return {
            'datasets': {
                'medical': [
                    {
                        'name': 'pubmedqa',
                        'source': 'pubmedqa/pubmedqa',
                        'local_path': './datasets/medical/pubmedqa',
                        'preprocessing_required': True
                    }
                ]
            }
        }
    
    def preprocess_all(self):
        """Preprocess all configured medical datasets"""
        logger.info("Starting preprocessing of all medical datasets")
        
        for dataset_config in self.datasets_config:
            if dataset_config.get('preprocessing_required', True):
                try:
                    self.preprocess_dataset(dataset_config)
                except Exception as e:
                    logger.error(f"Failed to preprocess {dataset_config['name']}: {e}")
                    continue
        
        logger.info("Completed preprocessing of all medical datasets")
    
    def preprocess_dataset(self, dataset_config: Dict):
        """Preprocess a specific dataset"""
        dataset_name = dataset_config['name']
        source = dataset_config['source']
        local_path = dataset_config['local_path']
        
        logger.info(f"Preprocessing {dataset_name} from {source}")
        
        # Create local directory
        Path(local_path).mkdir(parents=True, exist_ok=True)
        
        if dataset_name == 'mimiciv':
            self._preprocess_mimiciv(source, local_path, dataset_config)
        elif dataset_name == 'pubmedqa':
            self._preprocess_pubmedqa(source, local_path)
        elif dataset_name == 'medmcqa':
            self._preprocess_medmcqa(source, local_path)
        else:
            logger.warning(f"Unknown dataset: {dataset_name}")
    
    def _preprocess_mimiciv(self, source: str, local_path: str, config: Dict):
        """Preprocess MIMIC-IV dataset"""
        try:
            # MIMIC-IV requires special access credentials
            if config.get('access_required', False):
                logger.warning("MIMIC-IV requires PhysioNet credentials. Skipping automated download.")
                logger.info("Please manually download MIMIC-IV from PhysioNet and place in the datasets directory.")
                
                # Create placeholder structure
                self._create_mimiciv_placeholder(local_path)
                return
            
            # If credentials are available, proceed with download
            logger.info("Loading MIMIC-IV dataset...")
            # This would require PhysioNet credentials
            # dataset = load_dataset(source, trust_remote_code=True)
            
            # For now, create sample structure
            self._create_mimiciv_sample(local_path)
            
        except Exception as e:
            logger.error(f"Error preprocessing MIMIC-IV: {e}")
            self._create_mimiciv_placeholder(local_path)
    
    def _create_mimiciv_placeholder(self, local_path: str):
        """Create placeholder structure for MIMIC-IV"""
        placeholder_data = {
            'note': 'MIMIC-IV requires PhysioNet credentials',
            'instructions': [
                '1. Register at https://physionet.org/',
                '2. Complete required training',
                '3. Request access to MIMIC-IV',
                '4. Download and place files in this directory'
            ],
            'expected_structure': {
                'admissions.csv': 'Patient admission data',
                'patients.csv': 'Patient demographic data',
                'noteevents.csv': 'Clinical notes',
                'diagnoses_icd.csv': 'ICD diagnosis codes'
            }
        }
        
        with open(os.path.join(local_path, 'README.json'), 'w') as f:
            json.dump(placeholder_data, f, indent=2)
        
        logger.info(f"MIMIC-IV placeholder created at {local_path}")
    
    def _create_mimiciv_sample(self, local_path: str):
        """Create sample MIMIC-IV data for testing"""
        # Sample synthetic data for development/testing
        sample_patients = [
            {
                'subject_id': 10000001,
                'gender': 'M',
                'anchor_age': 65,
                'domain': 'medical',
                'dataset': 'mimiciv_sample'
            },
            {
                'subject_id': 10000002,
                'gender': 'F',
                'anchor_age': 72,
                'domain': 'medical',
                'dataset': 'mimiciv_sample'
            }
        ]
        
        sample_notes = [
            {
                'note_id': 1,
                'subject_id': 10000001,
                'text': 'Patient presents with chest pain and shortness of breath...',
                'category': 'Discharge summary',
                'domain': 'medical',
                'dataset': 'mimiciv_sample'
            }
        ]
        
        # Save sample data
        with open(os.path.join(local_path, 'patients_sample.json'), 'w') as f:
            json.dump(sample_patients, f, indent=2)
        
        with open(os.path.join(local_path, 'notes_sample.json'), 'w') as f:
            json.dump(sample_notes, f, indent=2)
    
    def _preprocess_pubmedqa(self, source: str, local_path: str):
        """Preprocess PubMedQA dataset"""
        try:
            logger.info("Loading PubMedQA dataset...")
            dataset = load_dataset(source, 'pqa_labeled')
            
            for split_name, split_data in dataset.items():
                processed_data = self._process_pubmedqa_split(split_data)
                self._save_processed_data(processed_data, local_path, split_name)
            
            logger.info(f"PubMedQA preprocessing completed. Data saved to {local_path}")
            
        except Exception as e:
            logger.error(f"Error preprocessing PubMedQA: {e}")
            # Create sample data for testing
            self._create_pubmedqa_sample(local_path)
    
    def _process_pubmedqa_split(self, split_data) -> List[Dict]:
        """Process a single split of PubMedQA data"""
        processed_data = []
        
        for example in split_data:
            # Extract context from abstracts
            context_text = ""
            if 'context' in example and example['context']:
                contexts = example['context']['contexts']
                labels = example['context']['labels']
                
                for i, ctx in enumerate(contexts):
                    label = labels[i] if i < len(labels) else ""
                    context_text += f"{label}: {ctx}\n"
            
            processed_example = {
                'id': example.get('pubid', ''),
                'question': example.get('question', ''),
                'context': {
                    'text': context_text.strip(),
                    'abstracts': example.get('context', {}).get('contexts', []),
                    'mesh_terms': example.get('mesh_terms', [])
                },
                'answer': example.get('final_decision', ''),
                'long_answer': example.get('long_answer', ''),
                'domain': 'medical',
                'dataset': 'pubmedqa'
            }
            processed_data.append(processed_example)
        
        return processed_data
    
    def _create_pubmedqa_sample(self, local_path: str):
        """Create sample PubMedQA data for testing"""
        sample_data = [
            {
                'id': 'sample_001',
                'question': 'Does aspirin reduce cardiovascular risk?',
                'context': {
                    'text': 'Background: Aspirin has been shown to reduce cardiovascular events in multiple studies.',
                    'abstracts': ['Aspirin reduces cardiovascular events...'],
                    'mesh_terms': ['Aspirin', 'Cardiovascular Disease']
                },
                'answer': 'yes',
                'long_answer': 'Yes, aspirin has been demonstrated to reduce cardiovascular risk in multiple clinical trials.',
                'domain': 'medical',
                'dataset': 'pubmedqa_sample'
            }
        ]
        
        self._save_processed_data(sample_data, local_path, 'sample')
    
    def _preprocess_medmcqa(self, source: str, local_path: str):
        """Preprocess MedMCQA dataset"""
        try:
            logger.info("Loading MedMCQA dataset...")
            dataset = load_dataset(source)
            
            for split_name, split_data in dataset.items():
                processed_data = self._process_medmcqa_split(split_data)
                self._save_processed_data(processed_data, local_path, split_name)
            
            logger.info(f"MedMCQA preprocessing completed. Data saved to {local_path}")
            
        except Exception as e:
            logger.error(f"Error preprocessing MedMCQA: {e}")
            self._create_medmcqa_sample(local_path)
    
    def _process_medmcqa_split(self, split_data) -> List[Dict]:
        """Process a single split of MedMCQA data"""
        processed_data = []
        
        for example in split_data:
            # Format multiple choice options
            options = {
                'A': example.get('opa', ''),
                'B': example.get('opb', ''),
                'C': example.get('opc', ''),
                'D': example.get('opd', '')
            }
            
            processed_example = {
                'id': example.get('id', ''),
                'question': example.get('question', ''),
                'context': {
                    'options': options,
                    'subject': example.get('subject_name', ''),
                    'topic': example.get('topic_name', ''),
                    'explanation': example.get('exp', '')
                },
                'answer': example.get('cop', ''),  # Correct option
                'answer_text': options.get(example.get('cop', ''), ''),
                'domain': 'medical',
                'dataset': 'medmcqa'
            }
            processed_data.append(processed_example)
        
        return processed_data
    
    def _create_medmcqa_sample(self, local_path: str):
        """Create sample MedMCQA data for testing"""
        sample_data = [
            {
                'id': 'sample_001',
                'question': 'Which of the following is the most common cause of pneumonia?',
                'context': {
                    'options': {
                        'A': 'Streptococcus pneumoniae',
                        'B': 'Haemophilus influenzae',
                        'C': 'Staphylococcus aureus',
                        'D': 'Klebsiella pneumoniae'
                    },
                    'subject': 'Medicine',
                    'topic': 'Respiratory System',
                    'explanation': 'Streptococcus pneumoniae is the most common bacterial cause of pneumonia.'
                },
                'answer': 'A',
                'answer_text': 'Streptococcus pneumoniae',
                'domain': 'medical',
                'dataset': 'medmcqa_sample'
            }
        ]
        
        self._save_processed_data(sample_data, local_path, 'sample')
    
    def _save_processed_data(self, data: List[Dict], local_path: str, split_name: str):
        """Save processed data to JSON file"""
        output_file = os.path.join(local_path, f"{split_name}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(data)} examples to {output_file}")
        
        # Also save as CSV for easy inspection
        df = pd.json_normalize(data)
        csv_file = os.path.join(local_path, f"{split_name}.csv")
        df.to_csv(csv_file, index=False)
        
        # Save metadata
        metadata = {
            'split': split_name,
            'total_examples': len(data),
            'columns': list(df.columns),
            'preprocessing_date': pd.Timestamp.now().isoformat(),
            'data_privacy_note': 'Medical data requires appropriate privacy protections'
        }
        
        metadata_file = os.path.join(local_path, f"{split_name}_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

def main():
    """Main function for script execution"""
    parser = argparse.ArgumentParser(description='Preprocess medical datasets for FAIR-Agent')
    parser.add_argument(
        '--dataset', 
        choices=['all', 'mimiciv', 'pubmedqa', 'medmcqa'],
        default='all',
        help='Which dataset to preprocess'
    )
    parser.add_argument(
        '--config',
        default='./config/config.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    
    try:
        preprocessor = MedicalDatasetPreprocessor(args.config)
        
        if args.dataset == 'all':
            preprocessor.preprocess_all()
        else:
            # Find specific dataset config
            dataset_config = None
            for config in preprocessor.datasets_config:
                if config['name'] == args.dataset:
                    dataset_config = config
                    break
            
            if dataset_config:
                preprocessor.preprocess_dataset(dataset_config)
            else:
                logger.error(f"Dataset {args.dataset} not found in configuration")
                sys.exit(1)
        
        logger.info("Medical dataset preprocessing completed successfully")
        
    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()