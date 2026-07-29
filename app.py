import streamlit as st
import google.generativeai as genai
import os

def init_session_state():
    """Initializes session state variables."""
    if "cours_genere" not in st.session_state:
        st.session_state.cours_genere = ""
    if "theme_memoire" not in st.session_state:
        st.session_state.theme_memoire = ""

def reset_app():
    """Resets the application state."""
    st.session_state.cours_genere = ""
    st.session_state.theme_memoire = ""

def build_prompt(public_cible, theme_cours, duree_seance, competence_ref, lieu_final, entreprise_finale):
    """Builds the prompt for the generative AI model."""
    consigne_referentiel = ""
    if competence_ref:
        consigne_referentiel = f"""
        5. CONFORMITÉ AU RÉFÉRENTIEL (OBLIGATION) : Tu dois impérativement construire TOUT le cours autour de cette compétence : "{competence_ref}".
        """

    prompt_pedagogique = f"""
    Tu es un expert en ingénierie pédagogique pour l'apprentissage en CFA.
    Tu dois concevoir un plan de cours approfondi, conforme et minuté.

    === DONNÉES D'ENTRÉE ===
    PUBLIC CIBLE : "{public_cible}"
    THÈME DU COURS : "{theme_cours}"
    DURÉE TOTALE : "{duree_seance}"
    COMPÉTENCE RÉFÉRENTIEL : "{competence_ref if competence_ref else 'Non spécifiée'}"
    LIEU DU SCÉNARIO : "{lieu_final}"
    TYPE D'ENTREPRISE : "{entreprise_finale}"
    ========================

    CONSIGNES CRITIQUES DE CALIBRAGE :
    1. ANALYSE SÉMANTIQUE : Déduis le niveau exact et la filière métier.
    2. ADAPTATION : Vocabulaire concret et opérationnel pour CAP/BP ; analytique/stratégique pour BTS/BM.
    3. CONTEXTUALISATION : Situe le scénario dans le lieu : {lieu_final}. L'entreprise ciblée est de type : {entreprise_finale}.
    4. DIRECTIVES DE MANU : Tu es le prescripteur, Manu est l'acteur (ne le nomme jamais). Intègre de l'humour/jeux de mots.
    {consigne_referentiel}
    6. GESTION DU TEMPS : Pour chaque section (Apport de connaissances, Exercice, etc.), tu dois indiquer une durée estimée cohérente pour que le total fasse exactement {duree_seance}.
    7. IMAGES RÉELLES : Intègre 2 images via Markdown (Ne fais aucune description textuelle).
       ![Titre](https://image.pollinations.ai/prompt/ta_description_en_anglais_sans_espace?width=800&height=400&nologo=true)
       - Image 1 (Photo) : ajoute "realistic_photo_of_" dans l'URL.
       - Image 2 (Cartoon) : ajoute "funny_cartoon_style_of_" dans l'URL.
       - Remplace les espaces par des tirets du bas (_) dans l'URL.
    8. PROFONDEUR ET RÉFÉRENTIEL : Le cours ne doit absolument pas être superficiel. Tu dois impérativement déduire du diplôme cible les prérequis logiques, ainsi que l'intitulé des compétences et savoirs associés (savoirs technologiques/théoriques) issus du référentiel officiel.

    STRUCTURE DE SORTIE ATTENDUE (EN MARKDOWN) :

    ## 📋 Fiche Pédagogique de la Séance
    * **Prérequis :** [Ce que l'apprenti doit impérativement maîtriser avant de commencer cette séance]
    * **Compétences visées (Référentiel) :** [Liste des compétences mobilisées pour ce thème]
    * **Savoirs associés (Référentiel) :** [Liste des savoirs technologiques et généraux en lien avec la séance]

    ## 🎯 Objectif de la séance (Temps estimé : X min)
    [Objectif calibré et lié au référentiel]

    ## 🔧 Mission Professionnelle à {lieu_final} (Temps estimé : X min)
    [Scénario engageant avec jeu de mots]
    [Image 1 : Photo]

    ## 📖 Apport de connaissances (Temps estimé : X min)
    [Explication technique approfondie des concepts]

    ## 📝 Exercice d'application (Temps estimé : X min)
    [Exercice pratique/étude de cas avec données chiffrées]

    ## ✅ Corrigé de l'exercice (Pour le formateur)
    [Réponses détaillées et justifiées]
    [Image 2 : Cartoon]

    ## 💡 Synthèse : Ce qu'il faut retenir (Temps estimé : X min)
    [3 points clés]

    ## ❓ QCM d'évaluation - 10 questions (Temps estimé : X min)
    [10 questions à choix multiples. ⚠️ FORMAT DE SAUT DE LIGNE OBLIGATOIRE POUR CHAQUE QUESTION :
    **Question X : [Texte de la question]**

    A) [Réponse A]

    B) [Réponse B]

    C) [Réponse C]

    D) [Réponse D]
    ]

    ## 🗝️ Corrigé du QCM (Pour le formateur)
    [Les 10 réponses avec courte justification]
    """
    return prompt_pedagogique

def main():
    # --- CONFIGURATION DE LA PAGE ---
    st.set_page_config(
        page_title="Assistant Pédagogique Intelligent",
        page_icon="⚡",
        layout="centered"
    )

    # --- INJECTION CSS (Le "Tuning" visuel à haut contraste) ---
    st.markdown("""
    <style>
    /* Mode Sombre global avec Haut Contraste (Bleu nuit élégant) */
    .stApp {
        background-color: #1a1a2e !important;
    }

    /* Forcer le texte en blanc pur pour une lisibilité maximale */
    .stApp p, .stApp span, .stApp div, .stApp label, .stApp h2, .stApp h3, .stApp li {
        color: #ffffff !important;
    }

    /* Style du titre principal (Effet Neon Bleu clair) */
    h1 {
        color: #00f0ff !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Champs de saisie (Lisibilité améliorée et Néon Vert au focus) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, div[data-baseweb="textarea"] > div {
        background-color: #16213e !important;
        border: 2px solid #0f3460 !important;
        border-radius: 8px;
    }
    div[data-baseweb="input"] > div > input, div[data-baseweb="textarea"] > div > textarea {
        color: #ffffff !important;
        font-weight: bold;
    }
    div[data-baseweb="input"]:focus-within > div, div[data-baseweb="select"]:focus-within > div, div[data-baseweb="textarea"]:focus-within > div {
        border-color: #00ffcc !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.6) !important;
    }

    /* Style du Bouton de génération (Le Bouton Glowing Haut Contraste) */
    div.stButton > button:first-child {
        background-color: #0f3460 !important;
        color: #00f0ff !important;
        border: 2px solid #00f0ff !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        border-radius: 12px;
        font-weight: bold;
        letter-spacing: 1px;
        padding: 10px 24px;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #00f0ff !important;
        color: #1a1a2e !important;
        box-shadow: 0 0 20px #00f0ff, 0 0 40px #00f0ff;
    }

    /* Style de l'expander (Menu déroulant Options) */
    div[data-testid="stExpander"] {
        background-color: #16213e !important;
        border: 1px solid #0f3460 !important;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- MÉMOIRE DE L'APPLICATION (SESSION STATE) ---
    init_session_state()

    # --- RÉCUPÉRATION DE LA CLÉ API ---
    api_key = ""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # --- INTERFACE PRINCIPALE ---
    st.title("⚡ ASSISTANT PÉDAGOGIQUE INTELLIGENT")
    st.markdown("---")

    if not api_key:
        st.warning("⚠️ **Le moteur est en veille.** Pour l'activer, collez votre clé API ci-dessous :")
        api_key = st.text_input(
            "🔑 Votre clé API Google Gemini :",
            type="password",
            help="Cette clé est nécessaire pour que l'application puisse dialoguer avec les serveurs d'IA."
        )
        st.markdown("---")
    else:
        st.success("✅ Moteur connecté (Clé sécurisée par l'administrateur).")

    if os.path.exists("edited-image.png"):
        st.image("edited-image.png", use_container_width=True)
    else:
        st.info("🖼️ Astuce Système : Le logo principal est introuvable. Assurez-vous que le fichier 'edited-image.png' est présent dans le même dossier que l'application.")

    st.write("Saisissez librement vos paramètres ci-dessous. Le système analysera sémantiquement votre demande pour générer un scénario conforme.")

    # --- FORMULAIRE DE SAISIE ---
    col1, col2 = st.columns(2)

    with col1:
        public_cible = st.text_input(
            "👥 Quel est le public ?",
            placeholder="Ex: CAP Équipier Polyvalent du Commerce",
            autocomplete="off"
        )

        duree_seance = st.selectbox(
            "⏱️ Durée de la séance ?",
            options=["1 heure", "2 heures", "3 heures", "4 heures", "Journée complète (7h)"]
        )

    with col2:
        theme_cours = st.text_input(
            "📚 Quel est le thème ?",
            placeholder="Ex: La gestion des stocks",
            autocomplete="off"
        )

    # --- OPTIONS AVANCÉES (Lieu & Entreprise) ---
    with st.expander("📍 Options du Scénario (Lieu & Entreprise)"):
        st.write("Personnalisez le contexte pour ancrer le cours dans la réalité des apprentis.")
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            lieu_scenario = st.text_input(
                "Ville ou Région :",
                placeholder="Ex: Strasbourg, Bretagne...",
                help="Laissez vide pour utiliser Chartres par défaut."
            )
        with col_opt2:
            type_entreprise = st.text_input(
                "Type d'entreprise :",
                placeholder="Ex: Grande surface, Salon de coiffure...",
                help="Laissez vide pour laisser l'IA choisir selon le thème."
            )

    # --- COMPÉTENCE RÉFÉRENTIEL ---
    competence_ref = st.text_area(
        "📜 Compétence du référentiel visée (Optionnel)",
        placeholder="Ex: C2.1 - Participer au suivi des stocks\n(Vous pouvez coller plusieurs lignes ou puces ici)",
        help="Copiez-collez ici les lignes exactes du référentiel pour forcer la conformité."
    )

    st.markdown("###")

    # --- LOGIQUE DE GÉNÉRATION ---
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        generer_btn = st.button("🛠️ GÉNÉRER LE COURS SUR MESURE", type="primary", use_container_width=True)
    with col_btn2:
        st.button("🔄 RÉINITIALISER", on_click=reset_app, use_container_width=True)

    if generer_btn:
        if not api_key:
            st.error("⛔ Clé API manquante. Veuillez l'insérer dans la zone prévue à cet effet.")
        elif not public_cible or not theme_cours:
            st.warning("⚠️ Veuillez remplir au minimum les champs 'Public' et 'Thème'.")
        else:
            with st.spinner(f"🔄 Calibrage d'une séance de {duree_seance} en cours..."):
                try:
                    genai.configure(api_key=api_key)
                    # Le moteur validé et fonctionnel
                    model = genai.GenerativeModel('gemini-2.5-flash')

                    # Validation des choix de scénario (remplissage par défaut si vide)
                    lieu_final = lieu_scenario if lieu_scenario else "Chartres (Eure-et-Loir)"
                    entreprise_finale = type_entreprise if type_entreprise else "Au choix, selon le thème"

                    # Création du prompt ultra-détaillé pour l'IA
                    prompt_pedagogique = build_prompt(
                        public_cible=public_cible,
                        theme_cours=theme_cours,
                        duree_seance=duree_seance,
                        competence_ref=competence_ref,
                        lieu_final=lieu_final,
                        entreprise_finale=entreprise_finale
                    )

                    response = model.generate_content(prompt_pedagogique)

                    st.session_state.cours_genere = response.text
                    st.session_state.theme_memoire = theme_cours

                except Exception as e:
                    st.error(f"🚨 Une erreur technique est survenue : {e}")

    # --- AFFICHAGE ET EXPORTATION ---
    if st.session_state.cours_genere:
        st.success("✨ Scénario généré et sauvegardé en mémoire !")

        nom_fichier = f"Cours_{st.session_state.theme_memoire.replace(' ', '_')}.md"
        st.download_button(
            label="📥 TÉLÉCHARGER LE COURS (Format Texte/Markdown)",
            data=st.session_state.cours_genere,
            file_name=nom_fichier,
            mime="text/markdown",
            help="Téléchargez le cours pour l'ouvrir dans Word, Notepad ou l'imprimer."
        )

        st.markdown("---")
        st.markdown(st.session_state.cours_genere)

if __name__ == "__main__":
    main()
