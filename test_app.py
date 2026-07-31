import pytest
from streamlit.testing.v1 import AppTest
import os
from unittest.mock import patch, MagicMock

# Create an empty file to test image logic if needed
if not os.path.exists("edited-image.png"):
    with open("edited-image.png", "w") as f:
        f.write("mock")

def test_initial_load():
    """Test que l'application se charge correctement avec les bons éléments d'interface."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Vérifie le titre
    assert at.title[0].value == "⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT"

    # Vérifie la présence de la barre latérale pour la clé API
    labels = [ti.label for ti in at.text_input]
    assert any("Votre clé API Google Gemini :" in l for l in labels)

    # Vérifie la présence des champs principaux
    labels = [ti.label for ti in at.text_input]
    assert "👥 Quel est le public ?" in labels
    assert "📚 Quel est le thème ?" in labels

    # Vérifie le bouton de génération
    assert at.button[0].label == "🛠️ GÉNÉRER LE COURS SUR MESURE"

def test_missing_api_key_warning():
    """Test qu'un avertissement est affiché si la clé API n'est pas fournie et qu'on clique sur Générer."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # On clique sans rien remplir
    next(b for b in at.button if "GÉNÉRER" in b.label).click().run()

    # Vérifie l'erreur de clé API manquante
    assert any("Clé API manquante" in e for e in [err.value for err in at.error])

def test_missing_fields_warning():
    """Test qu'un avertissement est affiché si la clé est là mais les champs sont vides."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Simuler l'entrée de la clé API
    next(ti for ti in at.text_input if "clé API" in ti.label).input("fake_api_key").run()

    # Clique sur le bouton générer
    next(b for b in at.button if "GÉNÉRER" in b.label).click().run()

    # On s'attend à un warning pour les champs manquants
    assert any("Veuillez remplir au minimum" in w for w in [warn.value for warn in at.warning])


def test_reset_button():
    """Test que le bouton de réinitialisation fonctionne."""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.run()

    # Simulate a generated course in session state
    at.session_state.cours_genere = "Test content"
    at.session_state.theme_memoire = "Test Theme"

    # Rerun to show the reset button
    at.run()

    # Find the reset button
    reset_btn = None
    for btn in at.button:
        if "NOUVELLE GÉNÉRATION" in btn.label:
            reset_btn = btn
            break

    assert reset_btn is not None

    # Click reset
    reset_btn.click().run()

    # Verify session state is cleared
    assert "cours_genere" not in at.session_state or at.session_state.cours_genere == ""
