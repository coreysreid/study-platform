"""Graph generation utilities for flashcards using matplotlib"""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import signal
import json
import logging
from contextlib import contextmanager
from RestrictedPython import compile_restricted_exec, safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safe_builtins, safer_getattr

logger = logging.getLogger(__name__)


def safe_getitem(obj, index):
    """
    Safe version of obj[index] for RestrictedPython.
    Only allows indexing on safe container types.
    """
    # Define allowed types for indexing
    allowed_types = (list, tuple, dict, str, np.ndarray)
    
    if not isinstance(obj, allowed_types):
        raise TypeError(f"Indexing not allowed on type {type(obj).__name__}")
    
    return obj[index]


class TimeoutException(Exception):
    """Exception raised when code execution times out"""
    pass


@contextmanager
def timeout(seconds):
    """Context manager for timing out code execution"""
    def signal_handler(signum, frame):
        raise TimeoutException("Graph generation timed out")
    
    # Set the signal handler and alarm
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # Disable the alarm
        signal.alarm(0)


def safe_execute_graph_code(code, variables=None):
    """
    Execute matplotlib code safely with restricted builtins.
    
    Args:
        code: Python code string to execute
        variables: Dictionary of variables to substitute in code
        
    Returns:
        matplotlib figure object
        
    Raises:
        ValueError: If code contains forbidden operations
        TimeoutException: If code takes too long to execute
    """
    if variables is None:
        variables = {}
    
    # Forbidden keywords that could be used for malicious purposes
    forbidden_keywords = [
        'import', 'exec', 'eval', 'open', 'file', 
        '__import__', 'compile', 'globals', 'locals',
        'input', 'raw_input', 'reload', 'execfile'
    ]
    
    # Check for forbidden keywords
    for keyword in forbidden_keywords:
        if keyword in code:
            raise ValueError(f"Forbidden keyword '{keyword}' found in code")
    
    # Substitute variables in the code (for parameterized graphs)
    for var_name, var_value in variables.items():
        placeholder = f"{{{var_name}}}"
        if placeholder in code:
            code = code.replace(placeholder, str(var_value))
    
    # Create a safe namespace with whitelisted imports and RestrictedPython guards
    restricted_globals = {
        '__builtins__': safe_builtins,
        '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
        '_getiter_': iter,
        '_getitem_': safe_getitem,
        '_getattr_': safer_getattr,
        'np': np,
        'plt': plt,
        'numpy': np,
    }
    
    # Create a new figure
    fig = plt.figure(figsize=(8, 6))
    
    try:
        # Compile code with RestrictedPython for safety
        byte_code = compile_restricted_exec(code, '<graph>')
        if byte_code.errors:
            plt.close(fig)
            raise ValueError(f"Code compilation errors: {byte_code.errors}")
        
        # Execute the code with timeout
        timeout_seconds = getattr(settings, 'GRAPH_TIMEOUT', 3)
        with timeout(timeout_seconds):
            exec(byte_code.code, restricted_globals, {})
    except TimeoutException:
        plt.close(fig)
        raise
    except Exception as e:
        plt.close(fig)
        raise ValueError(f"Error executing graph code: {str(e)}")
    
    return fig


def generate_graph(flashcard):
    """
    Generate graph from code and save to flashcard.
    
    Args:
        flashcard: Flashcard model instance with graph_code
        
    Returns:
        True if graph was generated successfully, False otherwise
    """
    if flashcard.graph_type == 'none' or not flashcard.graph_code:
        return False
    
    # Check if graph generation is enabled
    if not getattr(settings, 'ENABLE_GRAPH_GENERATION', True):
        return False
    
    try:
        # Extract variables if this is a parameterized card
        variables = {}
        if flashcard.parameter_spec:
            from .parameterization import ParameterGenerator
            generator = ParameterGenerator(flashcard.parameter_spec)
            variables = generator.generate()
        
        # Execute the graph code
        fig = safe_execute_graph_code(flashcard.graph_code, variables)
        
        # Apply graph configuration if provided
        if flashcard.graph_config:
            config = flashcard.graph_config
            if 'title' in config:
                plt.title(config['title'])
            if 'xlabel' in config:
                plt.xlabel(config['xlabel'])
            if 'ylabel' in config:
                plt.ylabel(config['ylabel'])
            if 'xlim' in config:
                plt.xlim(config['xlim'])
            if 'ylim' in config:
                plt.ylim(config['ylim'])
            if 'grid' in config and config['grid']:
                plt.grid(True)
        
        # Save figure to BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        
        # Create ContentFile and save to ImageField
        image_content = ContentFile(buffer.read())
        filename = f'graph_{flashcard.id}_{flashcard.graph_type}.png'
        flashcard.generated_graph_image.save(filename, image_content, save=True)
        
        # Close the figure to free memory
        plt.close(fig)
        
        return True
        
    except Exception as e:
        # Log the error using proper logging
        logger.error(f"Error generating graph for flashcard {flashcard.id}: {str(e)}")
        return False
    finally:
        # Always close any open figures
        plt.close('all')


def get_graph_template(graph_type):
    """
    Get a pre-built graph template for common graph types.
    
    Args:
        graph_type: Type of graph (function, parametric, 3d, vector)
        
    Returns:
        Dictionary with code template and default config
    """
    templates = {
        'function': {
            'code': """x = np.linspace(-10, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)""",
            'config': {
                'title': 'Function Plot',
                'xlabel': 'x',
                'ylabel': 'y',
                'grid': True
            }
        },
        'parametric': {
            'code': """t = np.linspace(0, 2*np.pi, 100)
x = np.cos(t)
y = np.sin(t)
plt.plot(x, y)
plt.grid(True)
plt.axis('equal')""",
            'config': {
                'title': 'Parametric Plot',
                'xlabel': 'x',
                'ylabel': 'y',
                'grid': True
            }
        },
        'vector': {
            'code': """x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
X, Y = np.meshgrid(x, y)
U = -Y
V = X
plt.quiver(X, Y, U, V)
plt.grid(True)""",
            'config': {
                'title': 'Vector Field',
                'xlabel': 'x',
                'ylabel': 'y',
                'grid': True
            }
        }
    }
    
    return templates.get(graph_type, templates['function'])
