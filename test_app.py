from streamlit.testing.v1 import AppTest

def test_app_loads():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)
    assert not at.exception, f"App generated exceptions: {at.exception}"
    assert "🎓 Assistant Pédagogique IA" in at.markdown[1].value

def test_missing_fields_shows_warning():
    at = AppTest.from_file("app.py")
    at.run(timeout=10)
    assert not at.exception

    # Find the API key input and set it so we pass the first check
    api_key_input = next(ti for ti in at.text_input if ti.label == "🔑 Clé API Gemini :")
    api_key_input.set_value("fake-api-key").run(timeout=10)

    # Click generate button without filling required fields
    generate_btn = next(btn for btn in at.button if btn.label == "🚀 Générer le cours sur mesure")
    generate_btn.click().run(timeout=10)

    # Check that a warning is displayed
    warning_msgs = [w.value for w in at.warning]
    assert any("Veuillez remplir au minimum les champs" in w for w in warning_msgs), "Warning about missing fields not found"
