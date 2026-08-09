import pytest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest

class MockChunk:
    def __init__(self, text):
        self.text = text

class MockGenerateContentStream:
    def __init__(self, chunks):
        self.chunks = chunks

    def __iter__(self):
        return iter(self.chunks)

@pytest.fixture
def mock_genai_client():
    with patch("app.genai.Client") as MockClient:
        mock_instance = MagicMock()
        mock_client_models = MagicMock()
        mock_client_models.generate_content_stream.return_value = MockGenerateContentStream([MockChunk("Ceci est un "), MockChunk("test généré par l'IA.")])
        mock_instance.models = mock_client_models
        MockClient.return_value = mock_instance
        yield MockClient

def test_app_title_and_layout():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    assert not at.exception

    # On vérifie la présence du titre principal
    title_present = any("Assistant Pédagogique IA" in md.value for md in at.markdown)
    assert title_present

def test_missing_api_key_shows_warning():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    # On clique sur le bouton sans avoir rempli les champs
    generate_btn = next(btn for btn in at.button if "Générer le cours sur mesure" in btn.label)
    generate_btn.click().run(timeout=10)

    # Une erreur doit s'afficher à propos de la clé API
    error_present = any("Impossible de démarrer : Clé API manquante." in err.value for err in at.error)
    assert error_present

def test_missing_fields_shows_warning():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    # On simule une clé API présente
    api_key_input = next(ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :")
    api_key_input.input("TEST_KEY").run(timeout=10)

    # On clique sur le bouton sans avoir rempli les autres champs obligatoires
    generate_btn = next(btn for btn in at.button if "Générer le cours sur mesure" in btn.label)
    generate_btn.click().run(timeout=10)

    # Un warning doit s'afficher
    warning_present = any("Veuillez remplir au minimum les champs" in warn.value for warn in at.warning)
    assert warning_present

def test_successful_generation(mock_genai_client):
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    # On remplit la clé API
    api_key_input = next(ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :")
    api_key_input.input("TEST_KEY").run(timeout=10)

    # On remplit le public, le thème et le type de commerce
    public_input = next(ti for ti in at.text_input if "Public" in ti.label)
    public_input.input("BTS MCO").run(timeout=10)

    theme_input = next(ti for ti in at.text_input if "Thème" in ti.label)
    theme_input.input("Management").run(timeout=10)

    commerce_input = next(ti for ti in at.text_input if "Type de commerce" in ti.label)
    commerce_input.input("Supermarché").run(timeout=10)

    # On clique sur générer
    generate_btn = next(btn for btn in at.button if "Générer le cours sur mesure" in btn.label)
    generate_btn.click().run(timeout=10)

    # On vérifie que la boîte de succès apparaît avec le texte de l'IA (en enlevant les balises html pour la vérification)
    success_box_present = any("Ceci est un test généré par l'IA." in md.value for md in at.markdown)
    assert success_box_present
