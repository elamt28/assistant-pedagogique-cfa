# ... existing code ...
    elif not public_cible or not theme_cours:
        st.warning("⚠️ Veuillez remplir au minimum les champs 'Public' et 'Thème'.")
    else:
        st.session_state.cours_genere = ""
        
        # 🛡️ CORRECTION : On crée la zone d'affichage AVANT la roue de chargement !
        zone_affichage_cours = st.empty() 
        texte_complet = ""
        
        with st.spinner(f"🔄 Calibrage d'une séance de {duree_seance} en cours... (Connexion au moteur Gemini)"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                consigne_referentiel = ""
# ... existing code ...
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
                
                response = model.generate_content(prompt_pedagogique, stream=True)
                
                for morceau in response:
                    try:
                        texte_complet += morceau.text
# ... existing code ...
```

Applique cette petite rustine magique et dis-moi si ton texte reste bien affiché jusqu'au bout cette fois-ci !
