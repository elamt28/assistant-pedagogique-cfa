from streamlit.testing.v1 import AppTest

def test_app_layout():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    assert "ASSISTANT PÉDAGOGIQUE INTELLIGENT" in at.title[0].value

def test_missing_api_key_warning():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    assert "Le moteur est en veille" in at.warning[0].value
