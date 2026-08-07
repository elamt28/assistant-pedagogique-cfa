import streamlit as st
import google.generativeai as genai
import time
import os

st.set_page_config(
    page_title="Assistant Pédagogique IA",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    /* Le fond bleu de l'application */
    .stApp {
        background-color: #e3f2fd; /* Bleu clair doux et professionnel */
    }
    .main-header {
        text-align: center;
        color: #0d47a1; /* Bleu foncé pour le titre */
        margin-bottom: 20px;
    }
    /* Style du bouton d'action */
    .stButton>button {
        width: 100%;
        background-color: #1e88e5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565c0;
        transform: scale(1.02);
    }
    /* Style de la boîte où s'affiche le cours pour qu'il soit bien lisible sur le fond bleu */
    .success-box {
        padding: 25px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

try:
    # On vérifie si l'image existe avant d'essayer de l'afficher
    if os.path.exists("edited-image.png"):
        st.image("edited-image.png", use_container_width=True)
except Exception as e:
    pass # Si l'image n'est pas là, on continue silencieusement

st.markdown("<h1 class='main-header'>🎓 Assistant Pédagogique IA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em; color: #333;'>Générez des fiches de cours sur mesure et des QCM pour la formation professionnelle.</p>", unsafe_allow_html=True)

api_key = ""
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    pass

if not api_key:
    st.info("Le moteur est en veille. Veuillez insérer votre propre clé API Google.")
    api_key = st.text_input("🔑 Clé API Gemini :", type="password")
else:
    st.success("✅ Moteur configuré par l'administrateur.")

st.markdown("### ⚙️ Configuration de la séance")

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
        pays_autre = st.text_input("Veuillez préciser le pays :")
        
    public_cible = st.text_input("👥 Public (ex: BTS MCO, CAP Cuisine) :")
    duree_seance = st.selectbox("⏱️ Durée", ["1 heure", "2 heures", "Demi-journée", "Journée entière"])

with col2:
    theme_cours = st.text_input("📚 Thème (ex: Traiter un client difficile) :")
    type_commerce = st.text_input("🏪 Type de commerce (ex: Boutique de sport, Restaurant, Bricolage) :")
    ton_cours = st.selectbox("🎭 Ton de l'animation", [
        "Dynamique et ludique",
        "Neutre et académique", 
        "Bienveillant et encourageant", 
        "Strict et directif"
    ])
    lieu_cours = st.text_input("📍 Lieu / Ville (Optionnel, ex: Paris, Montréal) :")

if st.button("🚀 Générer le cours sur mesure"):
    # Vérifications de sécurité avant de lancer l'IA
    if not api_key:
        st.error("⚠️ Impossible de démarrer : Clé API manquante.")
    elif not public_cible or not theme_cours or not type_commerce:
        st.warning("⚠️ Veuillez remplir au minimum les champs 'Public', 'Thème' et 'Type de commerce'.")
    else:
        # ZONE DE TEXTE PROTEGÉE : Créée avant le spinner pour ne pas disparaître !
        zone_affichage_cours = st.empty() 
        texte_complet = ""
        
        # Le spinner fait patienter l'utilisateur pendant que le moteur se connecte
        with st.spinner(f"🔄 Préparation d'une séance de {duree_seance} en cours..."):
            try:
                genai.configure(api_key=api_key)
                # Utilisation du moteur 2.5-flash validé
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                contexte_pays = pays_autre if systeme_educatif == "Autre pays francophone..." else systeme_educatif
                
                # Le Prompt intègre désormais le type de commerce demandé
                prompt_pedagogique = f"""
                Agis comme un ingénieur pédagogique expert pour la formation professionnelle.
                Rédige une fiche pédagogique complète pour la séance suivante :
                
                - Système éducatif ciblé : {contexte_pays}
                - Public visé : {public_cible}
                - Thème de la séance : {theme_cours}
                - Type de commerce / Secteur : {type_commerce}
                - Durée : {duree_seance}
                - Ton de l'animation : {ton_cours}
                - Contexte / Mise en situation : {lieu_cours if lieu_cours else "À définir localement"}
                
                IMPORTANT : Tout le scénario, les exemples et la mise en situation doivent impérativement se dérouler dans un contexte de "{type_commerce}".
                Utilise le vocabulaire officiel adapté au système éducatif ciblé.
                
                Structure obligatoire de la réponse (en Markdown) :
                ## 📋 Fiche Pédagogique de la Séance
                [Prérequis, Compétences visées, Savoirs associés]
                
                ## 🎯 Objectif de la séance
                [Objectif clair et minuté]
                
                ## 🔧 Déroulé et Mise en situation professionnelle ({type_commerce})
                [Explication de l'activité]
                
                ## ❓ QCM d'évaluation - 10 questions
                [10 questions à choix multiples. FORMAT OBLIGATOIRE POUR CHAQUE QUESTION :
                **Question X : [Texte]**
                
                A) [Réponse A]
                B) [Réponse B]
                C) [Réponse C]
                D) [Réponse D]
                ]

                ## 🗝️ Corrigé du QCM
                [Les 10 réponses avec courte justification]
                """
                
                response = model.generate_content(prompt_pedagogique, stream=True)
                
                for morceau in response:
                    try:
                        texte_complet += morceau.text
                        # Affichage du texte dans une boîte blanche stylisée par-dessus le fond bleu
                        zone_affichage_cours.markdown(f"<div class='success-box'>{texte_complet}</div>", unsafe_allow_html=True)
                        time.sleep(0.015) 
                    except ValueError:
                        continue
                        
            except Exception as e:
                st.error(f"❌ Une erreur de connexion au moteur de Google est survenue : {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 0.85em;'>Développé pour les acteurs de la formation professionnelle.</p>", unsafe_allow_html=True)
