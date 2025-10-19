import os
from dotenv import load_dotenv

def test_env_secret_key_present():
    """
    Ensures that .env is set up and contains a SECRET_KEY.
    """
    loaded = load_dotenv()
    assert loaded, ".env could not be loaded"

    secret_key = os.getenv("SECRET_KEY")
    assert secret_key, "SECRET_KEY is missing in .env"