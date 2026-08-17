from streamlit.testing.v1 import AppTest

def test_app():
    at = AppTest.from_file('app.py')
    at.run(timeout=10)

    assert "🎓 Assistant Pédagogique IA" in at.markdown[1].value or any("🎓 Assistant Pédagogique IA" in md.value for md in at.markdown)

    # Vérifier la présence des champs textuels spécifiques
    assert next((ti for ti in at.text_input if ti.label == '🔑 Clé API Gemini :'), None) is not None
    assert next((ti for ti in at.text_input if ti.label == '👥 Public (ex: BTS MCO, CAP Cuisine) :'), None) is not None
    assert next((ti for ti in at.text_input if ti.label == '📚 Thème (ex: Traiter un client difficile) :'), None) is not None
    assert next((ti for ti in at.text_input if ti.label == '🏪 Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :'), None) is not None
    assert next((ti for ti in at.text_input if ti.label == '📍 Lieu / Ville (Optionnel, ex: Paris, Montréal) :'), None) is not None
