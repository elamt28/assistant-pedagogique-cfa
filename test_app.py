from streamlit.testing.v1 import AppTest
import pytest
from unittest.mock import patch, MagicMock

def test_app_loads():
    at = AppTest.from_file("app.py").run(timeout=10)
    assert not at.exception

def test_missing_api_key_error():
    at = AppTest.from_file("app.py").run(timeout=10)

    # On simule le clic sur le bouton de génération sans clé API et sans champs remplis
    next(btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure").click().run(timeout=10)

    # On vérifie que l'erreur "Clé API manquante" s'affiche
    assert any("Impossible de démarrer : Clé API manquante." in err.value for err in at.error)

@patch("app.genai.Client")
def test_generation_success(mock_client_class):
    # Mocking the genai.Client
    mock_client = MagicMock()
    mock_models = MagicMock()

    # Simuler le comportement d'un flux de réponse (stream)
    mock_response_chunk1 = MagicMock()
    mock_response_chunk1.text = "## Fiche Pédagogique\n"
    mock_response_chunk2 = MagicMock()
    mock_response_chunk2.text = "Contenu du cours généré."

    mock_models.generate_content_stream.return_value = [mock_response_chunk1, mock_response_chunk2]
    mock_client.models = mock_models
    mock_client_class.return_value = mock_client

    at = AppTest.from_file("app.py").run(timeout=10)

    # On simule l'entrée d'une clé API
    next(ti for ti in at.text_input if "Clé API Gemini :" in ti.label).input("fake-api-key").run(timeout=10)

    # On remplit les champs obligatoires
    next(ti for ti in at.text_input if "Public (ex: BTS MCO, CAP Cuisine) :" in ti.label).input("BTS MCO").run(timeout=10)
    next(ti for ti in at.text_input if "Thème (ex: Traiter un client difficile) :" in ti.label).input("Vente").run(timeout=10)
    next(ti for ti in at.text_input if "Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :" in ti.label).input("Boutique").run(timeout=10)

    # On clique sur le bouton pour générer
    next(btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure").click().run(timeout=10)

    # On vérifie qu'il n'y a pas d'erreur ou d'avertissement
    assert not at.error
    assert not at.warning

    # On vérifie que le texte a bien été généré et stocké dans l'état de session
    assert "cours_genere" in at.session_state
    assert at.session_state["cours_genere"] == "## Fiche Pédagogique\nContenu du cours généré."

    # On vérifie que le bouton de téléchargement est présent
    assert any("📥 Télécharger le cours (Markdown)" in btn.label for btn in at.download_button)
