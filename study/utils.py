"""Utilities for parameterized flashcard generation"""
import random
import math
import re
from typing import Dict, Any, List


class ParameterGenerator:
    """Generates random parameters according to specification"""
    
    def __init__(self, parameter_spec: Dict[str, Any]):
        """
        Initialize generator with parameter specification.
        
        Args:
            parameter_spec: Dictionary with 'variables' and optional 'constraints' and 'precision'
        """
        self.spec = parameter_spec
        self.variables = parameter_spec.get('variables', {})
        self.constraints = parameter_spec.get('constraints', [])
        self.precision = parameter_spec.get('precision', 2)
        self.max_retries = 100
        
    def generate(self) -> Dict[str, Any]:
        """
        Generate a set of parameter values.
        
        Returns:
            Dictionary mapping variable names to generated values
            
        Raises:
            ValueError: If constraints cannot be satisfied after max_retries
        """
        for attempt in range(self.max_retries):
            try:
                values = self._generate_once()
                if self._check_constraints(values):
                    return values
            except Exception:
                continue
                
        raise ValueError(f"Could not generate valid parameters after {self.max_retries} attempts")
    
    def _generate_once(self) -> Dict[str, Any]:
        """Generate one set of parameter values"""
        values = {}
        
        # First pass: generate random values
        for var_name, var_spec in self.variables.items():
            var_type = var_spec.get('type')
            
            if var_type == 'random_int':
                values[var_name] = self._generate_random_int(var_spec)
            elif var_type == 'random_float':
                values[var_name] = self._generate_random_float(var_spec)
            elif var_type == 'random_choice':
                values[var_name] = self._generate_random_choice(var_spec)
            elif var_type == 'computed':
                # Computed values are handled in second pass
                pass
            else:
                raise ValueError(f"Unknown variable type: {var_type}")
        
        # Second pass: compute derived values
        for var_name, var_spec in self.variables.items():
            if var_spec.get('type') == 'computed':
                values[var_name] = self._compute_value(var_spec, values)
                
        return values
    
    def _generate_random_int(self, spec: Dict[str, Any]) -> int:
        """Generate random integer"""
        min_val = spec.get('min', 0)
        max_val = spec.get('max', 100)
        return random.randint(min_val, max_val)
    
    def _generate_random_float(self, spec: Dict[str, Any]) -> float:
        """Generate random float"""
        min_val = spec.get('min', 0.0)
        max_val = spec.get('max', 100.0)
        precision = spec.get('precision', self.precision)
        value = random.uniform(min_val, max_val)
        return round(value, precision)
    
    def _generate_random_choice(self, spec: Dict[str, Any]) -> Any:
        """Pick random value from choices"""
        choices = spec.get('choices', [])
        if not choices:
            raise ValueError("random_choice requires 'choices' list")
        return random.choice(choices)
    
    def _compute_value(self, spec: Dict[str, Any], values: Dict[str, Any]) -> Any:
        """Compute value from formula"""
        formula = spec.get('formula', '')
        if not formula:
            raise ValueError("computed type requires 'formula'")
        
        # Create safe namespace with math functions and generated values
        namespace = {
            'sqrt': math.sqrt,
            'pow': math.pow,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            **values
        }
        
        # Safely evaluate the formula
        try:
            result = eval(formula, {"__builtins__": {}}, namespace)  # nosec B307 - Restricted namespace, no builtins
            
            # Apply precision if it's a float
            if isinstance(result, float):
                precision = spec.get('precision', self.precision)
                result = round(result, precision)
                
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating formula '{formula}': {e}")
    
    def _check_constraints(self, values: Dict[str, Any]) -> bool:
        """Check if generated values satisfy all constraints"""
        if not self.constraints:
            return True
            
        namespace = {
            'abs': abs,
            **values
        }
        
        for constraint in self.constraints:
            try:
                if not eval(constraint, {"__builtins__": {}}, namespace):  # nosec B307 - Restricted namespace, no builtins
                    return False
            except Exception:
                return False
                
        return True


class TemplateRenderer:
    """Renders templates with generated parameter values"""
    
    def render(self, template: str, values: Dict[str, Any]) -> str:
        """
        Render template by replacing {variable} placeholders.
        
        Args:
            template: String with {variable} placeholders
            values: Dictionary of variable values
            
        Returns:
            Rendered string with placeholders replaced
        """
        if not template:
            return ""
            
        result = template
        
        # Replace each variable placeholder
        for var_name, var_value in values.items():
            placeholder = f"{{{var_name}}}"
            
            # Format the value appropriately
            formatted_value = self._format_value(var_value)
            result = result.replace(placeholder, formatted_value)
            
        return result
    
    def _format_value(self, value: Any) -> str:
        """Format a value for display"""
        if isinstance(value, float):
            # Remove unnecessary trailing zeros
            formatted = f"{value:.10f}".rstrip('0').rstrip('.')
            return formatted
        else:
            return str(value)


def generate_parameterized_card(parameter_spec: Dict[str, Any], 
                                 question_template: str,
                                 answer_template: str) -> tuple:
    """
    Generate a parameterized card with random values.
    
    Args:
        parameter_spec: Parameter specification dictionary
        question_template: Template for question
        answer_template: Template for answer
        
    Returns:
        Tuple of (rendered_question, rendered_answer, generated_values)
    """
    generator = ParameterGenerator(parameter_spec)
    values = generator.generate()
    
    renderer = TemplateRenderer()
    question = renderer.render(question_template, values)
    answer = renderer.render(answer_template, values)
    
    return question, answer, values
