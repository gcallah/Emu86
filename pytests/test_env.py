import os
import pytest

REQUIRED_ENV_VARS = [
    "SECRET_KEY",
]

@pytest.mark.parametrize("var", REQUIRED_ENV_VARS)
def test_required_environment_variables_exist(var):
    value = os.environ.get(var)
    assert value is not None and value != "", f"Environment variable {var} is missing or empty!"