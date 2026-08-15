from streamlit.testing.v1 import AppTest

def test_app_initialization():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)
    assert not at.exception