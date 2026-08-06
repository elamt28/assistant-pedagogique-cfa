import streamlit as st
import google.generativeai as genai
import os
import time

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
if "cours_genere" not in st.session_state:
    st.session_state.cours_genere = ""
if "theme_memoire" not in st.session_state:
    st.session_state.theme_memoire = ""

# Fonction pour réinitialiser le cours
def reinitialiser_cours():
    st.session_state.cours_genere = ""
    st.session_state.theme_memoire = ""

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

st.write("Saisissez librement vos paramètres ci-dessous. Le système analysera sémantiquement votre demande pour générer un scénario conforme.")

# --- FORMULAIRE DE SAISIE ---
systeme_choix = st.selectbox(
    "🌍 Système Éducatif (Pays cible)",
    options=[
        "🇫🇷 France (CFA, Lycée Pro, Titre Pro...)", 
        "🇧🇪 Belgique (IFAPME, Enseignement qualifiant...)", 
        "🇨🇭 Suisse (CFC, AFP, Formation Duale...)", 
        "🇨🇦 Québec (DEP, DEC, Formation Professionnelle...)",
        "🌐 Autre pays francophone..."
    ]
)

# Gestion de l'option "Autre pays"
if systeme_choix == "🌐 Autre pays francophone...":
    systeme_educatif = st.text_input(
        "✍️ Veuillez préciser le pays (et le système si connu) :",
        placeholder="Ex: Maroc (OFPPT), Sénégal (BTS), Luxembourg...",
        help="L'IA s'adaptera automatiquement à ce pays."
    )
else:
    systeme_educatif = systeme_choix

col1, col2 = st.columns(2)

with col1:
    public_cible = st.text_input(
        "👥 Quel est le public ?",
        placeholder="Ex: CAP, CFC, DEP...",
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
    
    ton_cours = st.selectbox(
        "🎭 Ton du formateur ?",
        options=["Dynamique et ludique (avec jeux de mots)", "Strict et académique (très formel)", "Bienveillant et encourageant"]
    )

# --- OPTIONS AVANCÉES (Lieu & Entreprise) ---
with st.expander("📍 Options du Scénario (Lieu & Entreprise)"):
    st.write("Personnalisez le contexte pour ancrer le cours dans la réalité des apprenants.")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        lieu_scenario = st.text_input(
            "Ville ou Région :",
            placeholder="Ex: Strasbourg, Liège, Genève, Montréal, Dakar...",
            help="Laissez vide pour utiliser une ville par défaut selon le pays."
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
if st.button("🛠️ GÉNÉRER LE COURS SUR MESURE", type="primary", use_container_width=True):
    if not api_key:
        st.error("⛔ Clé API manquante. Veuillez l'insérer dans la zone prévue à cet effet.")
    elif not systeme_educatif:
        st.warning("⚠️ Veuillez préciser le pays ciblé.")
    elif not public_cible or not theme_cours:
        st.warning("⚠️ Veuillez remplir au minimum les champs 'Public' et 'Thème'.")
    else:
        st.session_state.cours_genere = ""
        
        with st.spinner(f"🔄 Calibrage d'une séance de {duree_seance} en cours... (Connexion au moteur Gemini)"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                consigne_referentiel = ""
                if competence_ref:
                    consigne_referentiel = f"""
                    5. CONFORMITÉ AU RÉFÉRENTIEL (OBLIGATION) : Tu dois impérativement construire TOUT le cours autour de cette compétence/module : "{competence_ref}".
                    """
                
                lieu_final = lieu_scenario if lieu_scenario else f"Une ville pertinente du pays suivant : {systeme_educatif}"
                entreprise_finale = type_entreprise if type_entreprise else "Au choix, selon le thème et le pays"

                prompt_pedagogique = f"""
                Tu es un expert international en ingénierie pédagogique.
                Tu dois concevoir un plan de cours approfondi, conforme et minuté, spécifiquement adapté au système éducatif ciblé.

                === DONNÉES D'ENTRÉE ===
                SYSTÈME ÉDUCATIF (PAYS) : "{systeme_educatif}"
                PUBLIC CIBLE : "{public_cible}"
                THÈME DU COURS : "{theme_cours}"
                DURÉE TOTALE : "{duree_seance}"
                TON DU COURS : "{ton_cours}"
                COMPÉTENCE RÉFÉRENTIEL : "{competence_ref if competence_ref else 'Non spécifiée'}"
                LIEU DU SCÉNARIO : "{lieu_final}"
                TYPE D'ENTREPRISE : "{entreprise_finale}"
                ========================

                CONSIGNES CRITIQUES DE CALIBRAGE :
                1. ADAPTATION AU PAYS : Utilise le vocabulaire officiel du système éducatif et du pays demandé ({systeme_educatif}). Adapte la monnaie, le nom des institutions et les normes locales. Les exigences doivent correspondre au standard de ce pays.
                2. ANALYSE SÉMANTIQUE : Déduis le niveau exact et la filière métier.
                3. ADAPTATION DU TON : Adopte impérativement le style d'écriture suivant : "{ton_cours}".
                4. CONTEXTUALISATION : Situe le scénario dans le lieu : {lieu_final}. L'entreprise ciblée est de type : {entreprise_finale}.
                {consigne_referentiel}
                6. GESTION DU TEMPS : Indique une durée estimée cohérente pour que le total fasse exactement {duree_seance}.
                7. DIRECTIVES DE MANU : Tu es le formateur/prescripteur, Manu est l'acteur (ne le nomme jamais directement).
                8. IMAGES RÉELLES : Intègre 2 images via Markdown (Ne fais aucune description textuelle).
                   ![Titre](https://image.pollinations.ai/prompt/ta_description_en_anglais_sans_espace?width=800&height=400&nologo=true)
                   - Image 1 (Photo) : ajoute "realistic_photo_of_" dans l'URL.
                   - Image 2 (Cartoon) : ajoute "funny_cartoon_style_of_" dans l'URL.
                   - Remplace les espaces par des tirets du bas (_) dans l'URL.
                9. PROFONDEUR ET RÉFÉRENTIEL : Le cours ne doit absolument pas être superficiel. Déduis du diplôme cible les prérequis logiques, ainsi que l'intitulé des compétences et savoirs/modules associés.

                STRUCTURE DE SORTIE ATTENDUE (EN MARKDOWN) :
                
                ## 📋 Fiche Pédagogique de la Séance ({systeme_educatif})
                * **Prérequis :** [Ce que l'apprenant doit impérativement maîtriser]
                * **Compétences / Modules visés :** [Liste des compétences mobilisées]
                * **Savoirs associés :** [Liste des savoirs technologiques et généraux]

                ## 🎯 Objectif de la séance (Temps estimé : X min)
                [Objectif calibré et lié au référentiel]

                ## 🔧 Mission Professionnelle à {lieu_final} (Temps estimé : X min)
                [Scénario engageant adapté au contexte local]
                [Image 1 : Photo]

                ## 📖 Apport de connaissances (Temps estimé : X min)
                [Explication technique approfondie des concepts]

                ## 📝 Exercice d'application (Temps estimé : X min)
                [Exercice pratique/étude de cas avec données chiffrées adaptées au pays]

                ## ✅ Corrigé de l'exercice (Pour le formateur)
                [Réponses détaillées et justifiées]
                [Image 2 : Cartoon]

                ## 💡 Synthèse : Ce qu'il faut retenir (Temps estimé : X min)
                [3 points clés]

                ## ❓ QCM d'évaluation - 10 questions (Temps estimé : X min)
                [10 questions à choix multiples. FORMAT OBLIGATOIRE POUR CHAQUE QUESTION (Laisse un saut de ligne comme dans l'exemple) :
                **Question X : [Texte de la question]**
                
                A) [Réponse A]
                
                B) [Réponse B]
                
                C) [Réponse C]
                
                D) [Réponse D]
                ]

                ## 🗝️ Corrigé du QCM (Pour le formateur)
                [Les 10 réponses avec courte justification]
                """
                
                zone_affichage_cours = st.empty() 
                texte_complet = ""
                
                response = model.generate_content(prompt_pedagogique, stream=True)
                
                for morceau in response:
                    texte_complet += morceau.text
                    zone_affichage_cours.markdown(texte_complet + " ▌")
                    time.sleep(0.02)
                
                zone_affichage_cours.markdown(texte_complet)
                
                st.session_state.cours_genere = texte_complet
                st.session_state.theme_memoire = theme_cours
                
            except Exception as e:
                st.error(f"🚨 Une erreur technique est survenue : {e}")

# --- AFFICHAGE EN MÉMOIRE ET EXPORTATION ---
if st.session_state.cours_genere:
    st.success("✨ Scénario terminé et prêt à être utilisé !")
    
    col_boutons1, col_boutons2 = st.columns(2)
    with col_boutons1:
        nom_fichier = f"Cours_{st.session_state.theme_memoire.replace(' ', '_')}.md"
        st.download_button(
            label="📥 TÉLÉCHARGER (Format Texte/Markdown)",
            data=st.session_state.cours_genere,
            file_name=nom_fichier,
            mime="text/markdown",
            use_container_width=True
        )
    with col_boutons2:
        st.button("🧹 CRÉER UN NOUVEAU COURS", on_click=reinitialiser_cours, use_container_width=True)
        
    st.markdown("---")
    
    if "zone_affichage_cours" not in locals():
        st.markdown(st.session_state.cours_genere)
