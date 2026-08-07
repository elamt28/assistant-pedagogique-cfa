import pytest
from streamlit.testing.v1 import AppTest

def test_app_initialization():
    """Test that the app initializes correctly and default session state values are set."""
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    assert not at.exception
    assert "⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT" in at.title[0].value
    assert at.session_state['cours_genere'] == ""
    assert at.session_state['theme_memoire'] == ""

def test_reinitialiser_cours():
    """Test that resetting the course works."""
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    # Simulate an active course
    at.session_state['cours_genere'] = "Test cours"
    at.session_state['theme_memoire'] = "Test theme"

    # Re-run the app with the new session state to show the button
    at.run(timeout=10)

    # Find and click the reset button
    reset_button = next(b for b in at.button if b.label == "🧹 CRÉER UN NOUVEAU COURS")
    reset_button.click().run(timeout=10)

    # Assert session state is cleared
    assert at.session_state['cours_genere'] == ""
    assert at.session_state['theme_memoire'] == ""
