import pytest
from streamlit.testing.v1 import AppTest

def test_app_loads_and_has_elements():
    at = AppTest.from_file("app.py")
    at.run(timeout=15)

    # Verify no exceptions occurred during execution
    assert not at.exception

    # Assert main title is present (it's an st.title, which AppTest represents as title elements)
    assert any("⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT" in t.value for t in at.title)

    # Check for sidebar elements by label
    assert any(ti.label == "🔑 Clé API Google Gemini :" for ti in at.text_input)
    assert any(btn.label == "🗑️ Réinitialiser" for btn in at.button)

    # Check for main form elements by label
    assert any(ti.label == "👥 Quel est le public ?" for ti in at.text_input)
    assert any(ti.label == "📚 Quel est le thème ?" for ti in at.text_input)

    # Check for advanced scenario options
    assert any(ti.label == "Ville ou Région :" for ti in at.text_input)
    assert any(ti.label == "Type d'entreprise :" for ti in at.text_input)

    # Check for pedagogical checkboxes
    assert any(cb.label == "Inclure un glossaire" for cb in at.checkbox)
    assert any(cb.label == "Travail en groupe" for cb in at.checkbox)
    assert any(cb.label == "Critères d'évaluation" for cb in at.checkbox)

    # Check for the generate button
    assert any(btn.label == "🛠️ GÉNÉRER LE COURS SUR MESURE" for btn in at.button)

def test_reset_button():
    at = AppTest.from_file("app.py")
    at.run(timeout=15)

    # Set a dummy value to session state
    at.session_state["cours_genere"] = "dummy_course"
    at.session_state["theme_memoire"] = "dummy_theme"

    # Find the reset button
    reset_btn = next((btn for btn in at.button if btn.label == "🗑️ Réinitialiser"), None)
    assert reset_btn is not None

    # Click reset
    reset_btn.click().run(timeout=15)

    # Verify session state is cleared
    assert at.session_state["cours_genere"] == ""
    assert at.session_state["theme_memoire"] == ""
