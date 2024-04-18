import random
import string

def generate_string(size):
    # Define the pool of characters to choose from
    characters = string.ascii_uppercase + string.digits
    
    # Generate a random string of the specified size
    random_string = ''.join(random.choice(characters) for _ in range(size))
    
    return random_string