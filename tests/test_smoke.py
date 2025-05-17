from chatrepo.config import settings

def test_settings_load():
    assert settings.openai_api_key.startswith("sk-")
