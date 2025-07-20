from dotenv import load_dotenv, find_dotenv
import os

# Locate .env in project root
dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv(dotenv_path)

def get_openai_key() -> str:
    """
    Return the OPENAI_API_KEY from .env, or raise if missing/placeholder.
    """
    key = os.getenv('OPENAI_API_KEY')
    if not key or key == 'your_api_key_here':
        raise RuntimeError('OPENAI_API_KEY environment variable is not set or is still the placeholder')
    return key 