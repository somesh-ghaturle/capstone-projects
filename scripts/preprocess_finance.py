#!/usr/bin/env python3
"""
Finance Dataset Preprocessing Script for FAIR-Agent

This script downloads and preprocesses financial datasets including:
- FinQA: Financial Question Answering
- TAT-QA: Table and Text Question Answering  
- ConvFinQA: Conversational Financial QA

Usage:
    python scripts/preprocess_finance.py [--dataset all|finqa|tatqa|convfinqa]
"""

import os
import sys
import yaml
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from datasets import load_dataset, Dataset
import pandas as pd
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinanceDatasetPreprocessor:
    """Preprocessor for financial datasets"""
    
    def __init__(self, config_path: str = "./config/config.yaml"):
        """Initialize with configuration"""
        self.config = self._load_config(config_path)
        self.datasets_config = self.config['datasets']['finance']
        
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
                'finance': [
                    {
                        'name': 'finqa',
                        'source': 'ibm-research/finqa',
                        'local_path': './datasets/finance/finqa',
                        'preprocessing_required': True
                    }
                ]
            }
        }
    
    def preprocess_all(self):
        """Preprocess all configured finance datasets"""
        logger.info("Starting preprocessing of all finance datasets")
        
        for dataset_config in self.datasets_config:
            if dataset_config.get('preprocessing_required', True):
                try:
                    self.preprocess_dataset(dataset_config)
                except Exception as e:
                    logger.error(f"Failed to preprocess {dataset_config['name']}: {e}")
                    continue
        
        logger.info("Completed preprocessing of all finance datasets")
    
    def preprocess_dataset(self, dataset_config: Dict):
        """Preprocess a specific dataset"""
        dataset_name = dataset_config['name']
        source = dataset_config['source']
        local_path = dataset_config['local_path']
        
        logger.info(f"Preprocessing {dataset_name} from {source}")
        
        # Create local directory
        Path(local_path).mkdir(parents=True, exist_ok=True)
        
        if dataset_name == 'finqa':
            self._preprocess_finqa(source, local_path)
        elif dataset_name == 'tatqa':
            self._preprocess_tatqa(source, local_path)
        elif dataset_name == 'convfinqa':
            self._preprocess_convfinqa(source, local_path)
        else:
            logger.warning(f"Unknown dataset: {dataset_name}")
    
    def _preprocess_finqa(self, source: str, local_path: str):
        """Preprocess FinQA dataset"""
        try:
            # Load FinQA dataset
            logger.info("Loading FinQA dataset...")
            dataset = load_dataset(source)
            
            # Process train split
            if 'train' in dataset:
                train_data = self._process_finqa_split(dataset['train'])
                self._save_processed_data(train_data, local_path, 'train')
            
            # Process validation split
            if 'validation' in dataset:
                val_data = self._process_finqa_split(dataset['validation'])
                self._save_processed_data(val_data, local_path, 'validation')
            
            # Process test split
            if 'test' in dataset:
                test_data = self._process_finqa_split(dataset['test'])
                self._save_processed_data(test_data, local_path, 'test')
            
            logger.info(f"FinQA preprocessing completed. Data saved to {local_path}")
            
        except Exception as e:
            logger.error(f"Error preprocessing FinQA: {e}")
            raise
    
    def _process_finqa_split(self, split_data) -> List[Dict]:
        """Process a single split of FinQA data"""
        processed_data = []
        
        for example in split_data:
            processed_example = {
                'id': example.get('id', ''),
                'question': example.get('question', ''),
                'context': {
                    'table': example.get('table', []),
                    'text': example.get('text', ''),
                },
                'answer': example.get('answer', ''),
                'program': example.get('program', []),
                'gold_inds': example.get('gold_inds', []),
                'domain': 'finance',
                'dataset': 'finqa'
            }
            processed_data.append(processed_example)
        
        return processed_data
    
    def _preprocess_tatqa(self, source: str, local_path: str):
        """Preprocess TAT-QA dataset"""
        try:
            logger.info("Loading TAT-QA dataset...")
            dataset = load_dataset(source)
            
            for split_name, split_data in dataset.items():
                processed_data = self._process_tatqa_split(split_data)
                self._save_processed_data(processed_data, local_path, split_name)
            
            logger.info(f"TAT-QA preprocessing completed. Data saved to {local_path}")
            
        except Exception as e:
            logger.error(f"Error preprocessing TAT-QA: {e}")
            raise
    
    def _process_tatqa_split(self, split_data) -> List[Dict]:
        """Process a single split of TAT-QA data"""
        processed_data = []
        
        for example in split_data:
            processed_example = {
                'id': example.get('id', ''),
                'question': example.get('question', ''),
                'context': {
                    'table': example.get('table', {}),
                    'text': example.get('paragraphs', []),
                },
                'answer': example.get('answer', ''),
                'answer_type': example.get('answer_type', ''),
                'domain': 'finance',
                'dataset': 'tatqa'
            }
            processed_data.append(processed_example)
        
        return processed_data
    
    def _preprocess_convfinqa(self, source: str, local_path: str):
        """Preprocess ConvFinQA dataset"""
        try:
            logger.info("Loading ConvFinQA dataset...")
            dataset = load_dataset(source)
            
            for split_name, split_data in dataset.items():
                processed_data = self._process_convfinqa_split(split_data)
                self._save_processed_data(processed_data, local_path, split_name)
            
            logger.info(f"ConvFinQA preprocessing completed. Data saved to {local_path}")
            
        except Exception as e:
            logger.error(f"Error preprocessing ConvFinQA: {e}")
            raise
    
    def _process_convfinqa_split(self, split_data) -> List[Dict]:
        """Process a single split of ConvFinQA data"""
        processed_data = []
        
        for example in split_data:
            # Handle conversational context
            conversation_history = []
            if 'conversation' in example:
                for turn in example['conversation']:
                    conversation_history.append({
                        'question': turn.get('question', ''),
                        'answer': turn.get('answer', '')
                    })
            
            processed_example = {
                'id': example.get('id', ''),
                'question': example.get('question', ''),
                'context': {
                    'table': example.get('table', {}),
                    'text': example.get('text', ''),
                    'conversation_history': conversation_history
                },
                'answer': example.get('answer', ''),
                'domain': 'finance',
                'dataset': 'convfinqa'
            }
            processed_data.append(processed_example)
        
        return processed_data
    
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
            'preprocessing_date': pd.Timestamp.now().isoformat()
        }
        
        metadata_file = os.path.join(local_path, f"{split_name}_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

def main():
    """Main function for script execution"""
    parser = argparse.ArgumentParser(description='Preprocess finance datasets for FAIR-Agent')
    parser.add_argument(
        '--dataset', 
        choices=['all', 'finqa', 'tatqa', 'convfinqa'],
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
        preprocessor = FinanceDatasetPreprocessor(args.config)
        
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
        
        logger.info("Finance dataset preprocessing completed successfully")
        
    except Exception as e:
        logger.error(f"Preprocessing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()