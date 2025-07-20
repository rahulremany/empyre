from empyre_backend.utils.helpers import get_openai_key
from openai import OpenAI

def main():
    # Load API key and create client
    client = OpenAI(api_key=get_openai_key())
    # Fetch list of models to verify connectivity
    models = client.models.list()
    print(f"Models fetched: {len(models.data)}")

if __name__ == "__main__":
    main() 