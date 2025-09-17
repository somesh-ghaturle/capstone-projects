"""
Calibration Evaluation Module

This module implements metrics to evaluate how well agent confidence
scores align with actual performance (calibration).
"""

import logging
from typing import Dict, List, Tuple, Optional, Union
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class CalibrationScore:
    """Container for calibration evaluation results"""
    ece: float  # Expected Calibration Error
    mce: float  # Maximum Calibration Error
    ace: float  # Average Calibration Error
    brier_score: float
    reliability_diagram_data: Dict
    details: Dict

class CalibrationEvaluator:
    """
    Evaluator for calibration metrics
    
    Assesses how well agent confidence scores align with actual correctness.
    A well-calibrated agent should be correct X% of the time when it claims
    X% confidence.
    """
    
    def __init__(self, n_bins: int = 10):
        """
        Initialize calibration evaluator
        
        Args:
            n_bins: Number of bins for calibration analysis
        """
        self.logger = logging.getLogger(__name__)
        self.n_bins = n_bins
    
    def evaluate_calibration(
        self,
        predictions: List[str],
        ground_truths: List[str],
        confidence_scores: List[float],
        binary_correctness: Optional[List[bool]] = None
    ) -> CalibrationScore:
        """
        Evaluate calibration of predictions with confidence scores
        
        Args:
            predictions: List of agent predictions
            ground_truths: List of correct answers
            confidence_scores: List of confidence scores (0-1)
            binary_correctness: Optional pre-computed correctness scores
            
        Returns:
            CalibrationScore with detailed metrics
        """
        try:
            # Compute correctness if not provided
            if binary_correctness is None:
                binary_correctness = self._compute_correctness(predictions, ground_truths)
            
            # Validate inputs
            assert len(predictions) == len(ground_truths) == len(confidence_scores) == len(binary_correctness)
            
            # Compute calibration metrics
            ece = self._compute_ece(confidence_scores, binary_correctness)
            mce = self._compute_mce(confidence_scores, binary_correctness)
            ace = self._compute_ace(confidence_scores, binary_correctness)
            brier_score = self._compute_brier_score(confidence_scores, binary_correctness)
            
            # Generate reliability diagram data
            reliability_data = self._generate_reliability_diagram_data(
                confidence_scores, binary_correctness
            )
            
            # Compile details
            details = {
                'n_samples': len(predictions),
                'n_bins': self.n_bins,
                'mean_confidence': np.mean(confidence_scores),
                'mean_accuracy': np.mean(binary_correctness),
                'confidence_std': np.std(confidence_scores),
                'accuracy_by_confidence_bin': reliability_data['bin_accuracies']
            }
            
            return CalibrationScore(
                ece=ece,
                mce=mce,
                ace=ace,
                brier_score=brier_score,
                reliability_diagram_data=reliability_data,
                details=details
            )
            
        except Exception as e:
            self.logger.error(f"Error evaluating calibration: {e}")
            return self._default_score()
    
    def _compute_correctness(self, predictions: List[str], ground_truths: List[str]) -> List[bool]:
        """Compute binary correctness scores"""
        correctness = []
        
        for pred, truth in zip(predictions, ground_truths):
            # Simple exact match (can be enhanced with fuzzy matching)
            is_correct = self._is_prediction_correct(pred, truth)
            correctness.append(is_correct)
        
        return correctness
    
    def _is_prediction_correct(self, prediction: str, ground_truth: str) -> bool:
        """Determine if a prediction is correct"""
        # Normalize both strings
        pred_norm = prediction.strip().lower()
        truth_norm = ground_truth.strip().lower()
        
        # Exact match
        if pred_norm == truth_norm:
            return True
        
        # Check if prediction contains the ground truth
        if truth_norm in pred_norm or pred_norm in truth_norm:
            return True
        
        # For numerical answers, check approximate equality
        if self._is_numerical_match(pred_norm, truth_norm):
            return True
        
        return False
    
    def _is_numerical_match(self, pred: str, truth: str) -> bool:
        """Check if numerical predictions match within tolerance"""
        try:
            # Extract numbers from strings
            pred_numbers = self._extract_numbers(pred)
            truth_numbers = self._extract_numbers(truth)
            
            if not pred_numbers or not truth_numbers:
                return False
            
            # Check if any numbers match within 5% tolerance
            for p_num in pred_numbers:
                for t_num in truth_numbers:
                    if abs(p_num - t_num) / max(abs(t_num), 1e-6) < 0.05:
                        return True
            
            return False
            
        except:
            return False
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numerical values from text"""
        import re
        
        # Pattern to match numbers (including decimals and percentages)
        number_pattern = r'-?\d+\.?\d*'
        matches = re.findall(number_pattern, text)
        
        numbers = []
        for match in matches:
            try:
                numbers.append(float(match))
            except ValueError:
                continue
        
        return numbers
    
    def _compute_ece(self, confidence_scores: List[float], correctness: List[bool]) -> float:
        """Compute Expected Calibration Error"""
        bin_boundaries = np.linspace(0, 1, self.n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        ece = 0
        total_samples = len(confidence_scores)
        
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            # Find samples in this bin
            in_bin = [
                i for i, conf in enumerate(confidence_scores)
                if bin_lower < conf <= bin_upper
            ]
            
            if not in_bin:
                continue
            
            # Calculate bin accuracy and average confidence
            bin_accuracy = np.mean([correctness[i] for i in in_bin])
            bin_confidence = np.mean([confidence_scores[i] for i in in_bin])
            bin_weight = len(in_bin) / total_samples
            
            # Add to ECE
            ece += bin_weight * abs(bin_accuracy - bin_confidence)
        
        return ece
    
    def _compute_mce(self, confidence_scores: List[float], correctness: List[bool]) -> float:
        """Compute Maximum Calibration Error"""
        bin_boundaries = np.linspace(0, 1, self.n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        max_error = 0
        
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            # Find samples in this bin
            in_bin = [
                i for i, conf in enumerate(confidence_scores)
                if bin_lower < conf <= bin_upper
            ]
            
            if not in_bin:
                continue
            
            # Calculate bin accuracy and average confidence
            bin_accuracy = np.mean([correctness[i] for i in in_bin])
            bin_confidence = np.mean([confidence_scores[i] for i in in_bin])
            
            # Update maximum error
            bin_error = abs(bin_accuracy - bin_confidence)
            max_error = max(max_error, bin_error)
        
        return max_error
    
    def _compute_ace(self, confidence_scores: List[float], correctness: List[bool]) -> float:
        """Compute Average Calibration Error"""
        bin_boundaries = np.linspace(0, 1, self.n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        errors = []
        
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            # Find samples in this bin
            in_bin = [
                i for i, conf in enumerate(confidence_scores)
                if bin_lower < conf <= bin_upper
            ]
            
            if not in_bin:
                continue
            
            # Calculate bin accuracy and average confidence
            bin_accuracy = np.mean([correctness[i] for i in in_bin])
            bin_confidence = np.mean([confidence_scores[i] for i in in_bin])
            
            errors.append(abs(bin_accuracy - bin_confidence))
        
        return np.mean(errors) if errors else 0.0
    
    def _compute_brier_score(self, confidence_scores: List[float], correctness: List[bool]) -> float:
        """Compute Brier Score"""
        brier_score = np.mean([
            (conf - int(correct))**2
            for conf, correct in zip(confidence_scores, correctness)
        ])
        
        return brier_score
    
    def _generate_reliability_diagram_data(
        self, 
        confidence_scores: List[float], 
        correctness: List[bool]
    ) -> Dict:
        """Generate data for reliability diagram"""
        bin_boundaries = np.linspace(0, 1, self.n_bins + 1)
        bin_lowers = bin_boundaries[:-1]
        bin_uppers = bin_boundaries[1:]
        
        bin_confidences = []
        bin_accuracies = []
        bin_counts = []
        
        for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
            # Find samples in this bin
            in_bin = [
                i for i, conf in enumerate(confidence_scores)
                if bin_lower < conf <= bin_upper
            ]
            
            if in_bin:
                bin_confidence = np.mean([confidence_scores[i] for i in in_bin])
                bin_accuracy = np.mean([correctness[i] for i in in_bin])
                bin_count = len(in_bin)
            else:
                bin_confidence = (bin_lower + bin_upper) / 2
                bin_accuracy = 0.0
                bin_count = 0
            
            bin_confidences.append(bin_confidence)
            bin_accuracies.append(bin_accuracy)
            bin_counts.append(bin_count)
        
        return {
            'bin_confidences': bin_confidences,
            'bin_accuracies': bin_accuracies,
            'bin_counts': bin_counts,
            'bin_boundaries': bin_boundaries.tolist()
        }
    
    def plot_reliability_diagram(
        self, 
        calibration_score: CalibrationScore, 
        save_path: Optional[str] = None
    ):
        """Plot reliability diagram"""
        try:
            data = calibration_score.reliability_diagram_data
            
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Plot perfect calibration line
            ax.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
            
            # Plot actual calibration
            bin_confidences = data['bin_confidences']
            bin_accuracies = data['bin_accuracies']
            bin_counts = data['bin_counts']
            
            # Create scatter plot with size proportional to bin count
            sizes = [max(10, count * 100 / max(bin_counts)) for count in bin_counts]
            
            scatter = ax.scatter(
                bin_confidences, 
                bin_accuracies, 
                s=sizes, 
                alpha=0.7,
                label='Actual Calibration'
            )
            
            # Connect points with lines
            ax.plot(bin_confidences, bin_accuracies, 'o-', alpha=0.5)
            
            # Formatting
            ax.set_xlabel('Confidence')
            ax.set_ylabel('Accuracy')
            ax.set_title(f'Reliability Diagram (ECE: {calibration_score.ece:.3f})')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            
            # Add text with metrics
            metrics_text = f'ECE: {calibration_score.ece:.3f}\nMCE: {calibration_score.mce:.3f}\nBrier: {calibration_score.brier_score:.3f}'
            ax.text(0.05, 0.95, metrics_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Reliability diagram saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting reliability diagram: {e}")
    
    def _default_score(self) -> CalibrationScore:
        """Return default score for error cases"""
        return CalibrationScore(
            ece=1.0,
            mce=1.0,
            ace=1.0,
            brier_score=1.0,
            reliability_diagram_data={},
            details={'error': 'Evaluation failed'}
        )
    
    def evaluate_batch_calibration(
        self,
        batch_predictions: List[List[str]],
        batch_ground_truths: List[List[str]],
        batch_confidence_scores: List[List[float]]
    ) -> List[CalibrationScore]:
        """Evaluate calibration for multiple batches"""
        results = []
        
        for preds, truths, confs in zip(batch_predictions, batch_ground_truths, batch_confidence_scores):
            score = self.evaluate_calibration(preds, truths, confs)
            results.append(score)
        
        return results
    
    def get_aggregate_metrics(self, scores: List[CalibrationScore]) -> Dict[str, float]:
        """Calculate aggregate metrics across multiple calibration evaluations"""
        if not scores:
            return {}
        
        return {
            'mean_ece': np.mean([s.ece for s in scores]),
            'mean_mce': np.mean([s.mce for s in scores]),
            'mean_ace': np.mean([s.ace for s in scores]),
            'mean_brier_score': np.mean([s.brier_score for s in scores]),
            'std_ece': np.std([s.ece for s in scores]),
            'min_ece': np.min([s.ece for s in scores]),
            'max_ece': np.max([s.ece for s in scores])
        }