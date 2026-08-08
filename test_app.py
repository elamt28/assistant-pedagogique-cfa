import pytest
from streamlit.testing.v1 import AppTest
import os

def test_app_title_and_basic_ui():
    """Test that the application loads and displays the main components."""
    # Initialize the AppTest for our app.py
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Check if the title is displayed in markdown
    assert any("🎓 Assistant Pédagogique IA" in md.value for md in at.markdown)
    assert any("Générez des fiches de cours sur mesure" in md.value for md in at.markdown)

def test_form_inputs_exist():
    """Test that the required form inputs exist on the page."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Text input checks based on label text matching app.py implementation
    # We look through all text inputs to find the ones with specific labels
    labels = [ti.label for ti in at.text_input]
    assert "👥 Public (ex: BTS MCO, CAP Cuisine) :" in labels
    assert "📚 Thème (ex: Traiter un client difficile) :" in labels
    assert "🏪 Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :" in labels

    # Selectbox checks
    select_labels = [sb.label for sb in at.selectbox]
    assert "🌍 Système Éducatif" in select_labels
    assert "⏱️ Durée" in select_labels
    assert "🎭 Ton de l'animation" in select_labels

def test_button_exists():
    """Test that the submit button exists."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Verify the button exists
    assert any(btn.label == "🚀 Générer le cours sur mesure" for btn in at.button)

def test_missing_input_warning():
    """Test that clicking generate without inputs triggers a warning."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Give a dummy API key to bypass the first check
    try:
        api_input = next(ti for ti in at.text_input if "Clé API Gemini" in ti.label)
        api_input.input("dummy_key").run()
    except StopIteration:
        pass # API key input might be hidden if st.secrets works

    # Find and click the generate button
    gen_btn = next((btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure"), None)
    if gen_btn:
        gen_btn.click().run()

        # Check if warning exists
        assert any("Veuillez remplir au minimum les champs" in w.value for w in at.warning)
