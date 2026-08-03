from streamlit.testing.v1 import AppTest
import pytest

def test_app_ui_and_warnings():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)

    # Vérification du titre principal (en utilisant 'in')
    assert "⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT" in at.title[0].value

    # Vérification de l'existence du champ de clé API via son label et simulation de saisie
    api_input_found = False
    for text_input in at.text_input:
        if "🔑 Votre clé API Google Gemini :" in text_input.label:
            api_input_found = True
            text_input.input("fake_api_key")
            break
    assert api_input_found, "Le champ de clé API n'a pas été trouvé"

    at.run(timeout=10)

    # Simulation du clic sur le bouton de génération pour déclencher l'avertissement de champs vides
    button_found = False
    for btn in at.button:
        if "🛠️ GÉNÉRER LE COURS SUR MESURE" in btn.label:
            button_found = True
            btn.click()
            break
    assert button_found, "Le bouton de génération n'a pas été trouvé"

    at.run(timeout=10)

    # Vérifier que l'avertissement apparaît car le formulaire est vide
    warning_found = False
    for warning in at.warning:
        if "Veuillez remplir au minimum les champs" in warning.value:
            warning_found = True
            break
    assert warning_found, "Le message d'avertissement pour les champs vides n'est pas apparu"
