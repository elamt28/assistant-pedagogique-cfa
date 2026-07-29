import pytest
from streamlit.testing.v1 import AppTest

def test_app_rendering():
    """Test that the application UI renders correctly."""
    at = AppTest.from_file("app.py").run()

    assert not at.exception
    assert at.title[0].value == "⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT"

    # Check warning when API key is missing (Streamlit markdown rendering strips some characters when accessing .value, so check in string)
    assert "**Le moteur est en veille.** Pour l'activer, collez votre clé API ci-dessous :" in at.warning[0].value

    # Check buttons
    assert at.button[0].label == "🛠️ GÉNÉRER LE COURS SUR MESURE"
    assert at.button[1].label == "🔄 RÉINITIALISER"

def test_input_validation_missing_key():
    """Test clicking generate without API key shows an error."""
    at = AppTest.from_file("app.py").run()

    # Fill inputs but leave API key empty
    at.text_input[1].input("CAP") # Public
    at.text_input[2].input("Maths") # Theme

    # Click generate
    at.button[0].click().run()

    # Verify error message
    assert "Clé API manquante. Veuillez l'insérer dans la zone prévue à cet effet." in at.error[0].value

def test_input_validation_missing_fields():
    """Test clicking generate with API key but missing fields shows a warning."""
    at = AppTest.from_file("app.py").run()

    # Provide API key
    at.text_input[0].input("fake-api-key").run()

    # Click generate without filling Public and Theme
    at.button[0].click().run()

    # Verify warning message (need to check warning[1] because warning[0] is the API key warning)
    # Actually, if we provide the API key, warning[0] should be the missing fields warning, but Streamlit testing might not clear the first warning if not re-run properly or due to state.
    # Let's just check that the warning exists in any of the warnings.
    warnings = [w.value for w in at.warning]
    assert any("Veuillez remplir au minimum les champs 'Public' et 'Thème'." in w for w in warnings)

def test_reset_button_clears_session():
    """Test that the reset button clears the session state."""
    at = AppTest.from_file("app.py").run()

    # Manually set session state as if a course was generated
    at.session_state["cours_genere"] = "This is a fake course."
    at.session_state["theme_memoire"] = "Fake Theme"

    # The success message and download button should be visible now
    # Re-run to update UI based on session state change
    at.run()
    assert at.session_state["cours_genere"] == "This is a fake course."

    # Click reset
    at.button[1].click().run()

    # Session state should be cleared
    assert at.session_state["cours_genere"] == ""
    assert at.session_state["theme_memoire"] == ""
