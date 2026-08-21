from streamlit.testing.v1 import AppTest

def test_app_loads():
    at = AppTest.from_file('app.py')
    at.run(timeout=10)

    # Vérification que le titre principal est présent
    assert any("🎓 Assistant Pédagogique IA" in md.value for md in at.markdown)

    # Vérification qu'un des champs de saisie est présent par son étiquette
    theme_input = next((ti for ti in at.text_input if ti.label == "📚 Thème (ex: Traiter un client difficile) :"), None)
    assert theme_input is not None
