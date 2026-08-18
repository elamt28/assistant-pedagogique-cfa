from streamlit.testing.v1 import AppTest

def test_app_title_and_loading():
    """
    Test que l'application Streamlit charge correctement
    et affiche le titre principal sans exception.
    """
    at = AppTest.from_file('app.py')
    at.run(timeout=10)

    assert not at.exception, "L'application a levé une exception au chargement."

    # Vérification du titre via markdown (on utilise `in` car il peut y avoir du HTML autour)
    # Dans app.py: st.markdown("<h1 class='main-header'>🎓 Assistant Pédagogique IA</h1>", unsafe_allow_html=True)
    title_found = False
    for markdown_element in at.markdown:
        if "<h1 class='main-header'>🎓 Assistant Pédagogique IA</h1>" in markdown_element.value:
            title_found = True
            break

    assert title_found, "Le titre principal n'a pas été trouvé dans les éléments markdown."
