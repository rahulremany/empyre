from empyre_backend.utils.helpers import get_openai_key

def main():
    print('Loaded key:', get_openai_key()[:4] + '…')  # only show first 4 chars

if __name__ == '__main__':
    main() 