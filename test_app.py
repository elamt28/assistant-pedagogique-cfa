from streamlit.testing.v1 import AppTest

def test_app_loads_and_has_inputs():
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Vérification que l'application s'est lancée sans erreur critique
    assert not at.exception

    # Vérifier la présence du champ Clé API et Système Éducatif
    api_key_input = next((ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :"), None)
    assert api_key_input is not None

    systeme_educatif_select = next((sb for sb in at.selectbox if sb.label == "🌍 Système Éducatif"), None)
    assert systeme_educatif_select is not None

    # On vérifie aussi la présence d'autres éléments
    public_input = next((ti for ti in at.text_input if ti.label == "👥 Public (ex: BTS MCO, CAP Cuisine) :"), None)
    assert public_input is not None

def test_missing_fields_warning():
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # On définit la clé API pour passer la première erreur
    api_key_input = next((ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :"), None)
    api_key_input.set_value("fake_api_key")

    # On laisse les champs vides et on clique sur générer
    gen_button = at.button[0]
    assert gen_button.label == "🚀 Générer le cours sur mesure"
    gen_button.click().run()

    # On s'attend à avoir un warning
    warning = next((w for w in at.warning if "Veuillez remplir au minimum les champs" in w.value), None)
    assert warning is not None

def test_missing_api_key_error():
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # On remplit les champs mais pas la clé
    public_input = next((ti for ti in at.text_input if ti.label == "👥 Public (ex: BTS MCO, CAP Cuisine) :"), None)
    public_input.set_value("BTS MCO")

    theme_input = next((ti for ti in at.text_input if ti.label == "📚 Thème (ex: Traiter un client difficile) :"), None)
    theme_input.set_value("Vente")

    commerce_input = next((ti for ti in at.text_input if ti.label == "🏪 Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :"), None)
    commerce_input.set_value("Boutique de sport")

    # on clique sur générer
    gen_button = at.button[0]
    gen_button.click().run()

    # On s'attend à avoir une erreur
    error = next((e for e in at.error if "Clé API manquante" in e.value), None)
    assert error is not None
