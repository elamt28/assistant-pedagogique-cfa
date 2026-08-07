import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
    page_title="Assistant Pédagogique IA",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1e3a8a;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #152c6a;
        border-color: #152c6a;
    }
    .success-box {
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🎓 Assistant Pédagogique IA</h1>", unsafe_allow_html=True)
st.markdown("Générez des fiches de cours sur mesure et des QCM pour la formation professionnelle en quelques secondes.")

api_key = ""
try:
    # Tente de récupérer la clé depuis les secrets de Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    pass

if not api_key:
    st.info("Le moteur est en veille. Veuillez insérer votre propre clé API Google.")
    api_key = st.text_input("🔑 Clé API Gemini :", type="password")
else:
    st.success("✅ Moteur configuré par l'administrateur.")

st.markdown("### ⚙️ Configuration du cours")

col1, col2 = st.columns(2)

with col1:
    systeme_educatif = st.selectbox("🌍 Système Éducatif", [
        "France (Éducation Nationale / Qualiopi)", 
        "Québec (DEP)", 
        "Suisse (CFC)", 
        "Belgique (IFAPME / Qualifiant)", 
        "Autre pays francophone..."
    ])
    
    pays_autre = ""
    if systeme_educatif == "Autre pays francophone...":
        pays_autre = st.text_input("Veuillez préciser le pays (ex: Maroc, Sénégal) :")
        
    public_cible = st.text_input("👥 Public (ex: BTS MCO, CAP Cuisine) :")
    duree_seance = st.selectbox("⏱️ Durée", ["1 heure", "2 heures", "Demi-journée", "Journée entière"])

with col2:
    theme_cours = st.text_input("📚 Thème (ex: Traiter un client difficile) :")
    ton_cours = st.selectbox("🎭 Ton de l'animation", [
        "Dynamique et ludique",
        "Neutre et académique", 
        "Bienveillant et encourageant", 
        "Strict et directif"
    ])
    lieu_cours = st.text_input("📍 Lieu / Contexte (Optionnel, ex: Paris) :")

if st.button("🚀 Générer le cours sur mesure"):
    if not api_key:
        st.error("⚠️ Impossible de démarrer : Clé API manquante.")
    elif not public_cible or not theme_cours:
        st.warning("⚠️ Veuillez remplir au minimum les champs 'Public' et 'Thème'.")
    else:
        # 🛡️ LA RUSTINE MAGIQUE : On crée la zone de texte AVANT le spinner !
        # Ainsi, quand le spinner disparaît, le texte reste à l'écran.
        zone_affichage_cours = st.empty() 
        texte_complet = ""
        
        # Le spinner fait patienter l'utilisateur pendant que le moteur se connecte
        with st.spinner(f"🔄 Calibrage d'une séance de {duree_seance} en cours..."):
            try:
                # Configuration du moteur
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Détermination du contexte pays
                contexte_pays = pays_autre if systeme_educatif == "Autre pays francophone..." else systeme_educatif
                
                # Création du super-prompt pour l'IA
                prompt_pedagogique = f"""
                Agis comme un ingénieur pédagogique expert pour la formation professionnelle.
                Rédige une fiche pédagogique complète pour la séance suivante :
                
                - Système éducatif ciblé : {contexte_pays}
                - Public visé : {public_cible}
                - Thème de la séance : {theme_cours}
                - Durée : {duree_seance}
                - Ton de l'animation : {ton_cours}
                - Contexte / Mise en situation : {lieu_cours if lieu_cours else "À définir de manière pertinente et locale"}
                
                Utilise le vocabulaire officiel adapté au système éducatif ciblé (ex: CFA, DEP, CFC, apprentis, élèves, etc.).
                
                Structure obligatoire de la réponse (en Markdown) :
                ## 📋 Fiche Pédagogique de la Séance
                [Prérequis, Compétences visées, Savoirs associés]
                
                ## 🎯 Objectif de la séance
                [Objectif clair et minuté]
                
                ## 🔧 Déroulé et Mise en situation professionnelle
                [Explication de l'activité]
                
                ## ❓ QCM d'évaluation - 10 questions
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
                
                # Appel à l'IA avec la fonction "stream=True" pour l'effet machine à écrire
                response = model.generate_content(prompt_pedagogique, stream=True)
                
                # Affichage en temps réel des morceaux de texte
                for morceau in response:
                    try:
                        texte_complet += morceau.text
                        zone_affichage_cours.markdown(f"<div class='success-box'>{texte_complet}</div>", unsafe_allow_html=True)
                        time.sleep(0.02) # Petit délai pour rendre l'effet de frappe fluide
                    except ValueError:
                        # Sécurité si l'IA envoie un morceau vide
                        continue
                        
            except Exception as e:
                st.error(f"❌ Une erreur de connexion est survenue : {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>Développé pour les acteurs de la formation professionnelle.</p>", unsafe_allow_html=True)
