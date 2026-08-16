from streamlit.testing.v1 import AppTest
from unittest.mock import patch

def test_app_initialization():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    assert not at.exception

    # Check title
    assert any("Assistant Pédagogique IA" in md.value for md in at.markdown)

    # Check button
    assert at.button[0].label == "🚀 Générer le cours sur mesure"

@patch("google.genai.Client")
def test_app_generation_success(mock_client):
    # Mocking genai response
    class MockChunk:
        def __init__(self, text):
            self.text = text

    class MockModels:
        def generate_content_stream(self, model, contents):
            return [MockChunk("Ceci est un "), MockChunk("cours généré.")]

    mock_instance = mock_client.return_value
    mock_instance.models = MockModels()

    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    assert not at.exception

    # Fill mandatory fields
    # Using generator to find inputs by label
    api_key_input = next(ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :")
    api_key_input.set_value("fake_api_key").run(timeout=10)

    public_input = next(ti for ti in at.text_input if ti.label == "👥 Public (ex: BTS MCO, CAP Cuisine) :")
    public_input.set_value("BTS MCO").run(timeout=10)

    theme_input = next(ti for ti in at.text_input if ti.label == "📚 Thème (ex: Traiter un client difficile) :")
    theme_input.set_value("Management").run(timeout=10)

    commerce_input = next(ti for ti in at.text_input if ti.label == "🏪 Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :")
    commerce_input.set_value("Boutique de sport").run(timeout=10)

    # Click button
    at.button[0].click().run(timeout=10)

    # Assert no exceptions during generation
    assert not at.exception

    # Verify session state was populated correctly
    assert 'cours_genere' in at.session_state
    assert at.session_state['cours_genere'] == "Ceci est un cours généré."

    # Verify the generated text is rendered in the UI
    assert any("Ceci est un cours généré." in md.value for md in at.markdown)
