import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch, MagicMock

def test_app_loads_successfully():
    """Test that the application loads without errors."""
    at = AppTest.from_file("app.py").run(timeout=10)
    assert not at.exception

def test_ui_elements_presence():
    """Test the presence of main UI elements using label matching."""
    at = AppTest.from_file("app.py").run(timeout=10)

    # Asserting titles and texts (using 'in' operator for markdown content)
    assert any("Assistant Pédagogique IA" in md.value for md in at.markdown)

    # Asserting input elements using next() to find them by label
    assert next((ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :"), None) is not None
    assert next((sb for sb in at.selectbox if sb.label == "🌍 Système Éducatif"), None) is not None
    assert next((ti for ti in at.text_input if ti.label == "👥 Public (ex: BTS MCO, CAP Cuisine) :"), None) is not None
    assert next((sb for sb in at.selectbox if sb.label == "⏱️ Durée"), None) is not None
    assert next((ti for ti in at.text_input if ti.label == "📚 Thème (ex: Traiter un client difficile) :"), None) is not None
    assert next((ti for ti in at.text_input if ti.label == "🏪 Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :"), None) is not None
    assert next((sb for sb in at.selectbox if sb.label == "🎭 Ton de l'animation"), None) is not None
    assert next((ti for ti in at.text_input if ti.label == "📍 Lieu / Ville (Optionnel, ex: Paris, Montréal) :"), None) is not None

    # Asserting button
    assert next((btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure"), None) is not None

def test_missing_api_key_error():
    """Test error message when API key is missing."""
    at = AppTest.from_file("app.py").run(timeout=10)

    # Empty API key by default in tests without secrets
    generate_btn = next((btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure"), None)
    generate_btn.click().run(timeout=10)

    # Verify error message is shown
    assert any("Impossible de démarrer : Clé API manquante." in err.value for err in at.error)

@patch("streamlit.secrets", {"GEMINI_API_KEY": "fake_key"})
def test_missing_fields_warning():
    """Test warning message when required fields are missing."""
    at = AppTest.from_file("app.py").run(timeout=10)

    generate_btn = next((btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure"), None)
    generate_btn.click().run(timeout=10)

    # Verify warning message is shown since fields are empty
    assert any("Veuillez remplir au minimum les champs" in warn.value for warn in at.warning)

def test_download_button_appears_when_content_generated():
    """Test that the download button appears when session state contains generated course."""
    at = AppTest.from_file("app.py")

    # Simulate content in session state
    at.session_state['cours_genere'] = "## Contenu du cours généré\nCeci est un test."
    at.run(timeout=10)

    # Verify the download button appears
    assert next((dl for dl in at.download_button if dl.label == "📥 Télécharger le cours (Markdown)"), None) is not None
