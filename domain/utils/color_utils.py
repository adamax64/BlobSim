import random

def generate_random_color() -> str:
    """Generate a random hex color code."""
    # Generate random RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Convert to hex and format
    return f"#{r:02x}{g:02x}{b:02x}" 
