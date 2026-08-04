from streamlit.testing.v1 import AppTest

def test_api_key_input():
    # Instanciate the AppTest
    at = AppTest.from_file("app.py", default_timeout=10)

    # Run the application initially
    at.run(timeout=10)

    # Check if the warning is displayed when api key is not set
    assert any("**Le moteur est en veille.** Pour l'activer, collez votre clé API ci-dessous :" in str(w.value) for w in at.warning)

    # Check if the warning is still displayed when the user inputs the key manually
    # (as the success message is reserved for the admin key in st.secrets)
    api_key_input = next(ti for ti in at.text_input if ti.label == "🔑 Votre clé API Google Gemini :")
    api_key_input.set_value("dummy_api_key").run(timeout=10)
    assert any("**Le moteur est en veille.** Pour l'activer, collez votre clé API ci-dessous :" in str(w.value) for w in at.warning)

    # Check that the input value is correctly updated
    api_key_input_updated = next(ti for ti in at.text_input if ti.label == "🔑 Votre clé API Google Gemini :")
    assert api_key_input_updated.value == "dummy_api_key"

def test_session_state_initialization():
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run(timeout=10)

    # Check that session state variables are correctly initialized
    assert 'cours_genere' in at.session_state
    assert at.session_state['cours_genere'] == ""
    assert 'theme_memoire' in at.session_state
    assert at.session_state['theme_memoire'] == ""
