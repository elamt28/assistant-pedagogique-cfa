import pytest
from streamlit.testing.v1 import AppTest

def test_app_sidebar():
    at = AppTest.from_file("app.py")
    at.run()

    # Check if the title is present
    assert "⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT" in at.title[0].value

    # Check if the labels match what we expect for the main inputs
    labels = [ti.label for ti in at.text_input]
    assert "👥 Quel est le public ?" in labels
    assert "📚 Quel est le thème ?" in labels

    assert at.selectbox[0].label == "⏱️ Durée de la séance ?"

def test_app_reset_button():
    at = AppTest.from_file("app.py")
    at.run()

    # The reset button should be in the app
    button_labels = [btn.label for btn in at.button]
    assert "🔄 Réinitialiser" in button_labels
