<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .astro-container {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            padding: 40px 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            position: relative;
        }
        
        .astro-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url('TON_LOGO_URL_ICI');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.05;
            pointer-events: none;
        }
        
        .astro-wrapper {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 3rem;
            color: white;
            font-weight: 300;
            margin-bottom: 10px;
            text-shadow: 0 2px 30px rgba(139, 92, 246, 0.5);
            letter-spacing: 2px;
        }
        
        .header p {
            color: rgba(255, 255, 255, 0.7);
            font-size: 1.1rem;
            font-weight: 300;
        }
        
        .form-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .form-group label {
            display: block;
            color: white;
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 15px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            font-size: 1rem;
            transition: all 0.3s;
        }
        
        .form-group input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #a78bfa;
            box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.3);
            background: rgba(255, 255, 255, 0.2);
        }
        
        .calculate-btn {
            width: 100%;
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
            font-weight: bold;
            padding: 20px;
            border: none;
            border-radius: 15px;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 10px 40px rgba(139, 92, 246, 0.5);
        }
        
        .calculate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(139, 92, 246, 0.7);
        }
        
        .calculate-btn:disabled {
            background: gray;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: white;
            font-size: 1.2rem;
            padding: 20px;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results {
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .section-title {
            color: white;
            font-size: 2rem;
            font-weight: bold;
            margin: 40px 0 20px 0;
            text-align: center;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }
        
        /* Numérologie */
        .numero-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .numero-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .numero-card h3 {
            color: white;
            font-size: 1.2rem;
            margin-bottom: 15px;
        }
        
        .numero-card .big-number {
            font-size: 4rem;
            color: white;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .cvh-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .cvh-card {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }
        
        .cvh-card h4 {
            color: white;
            font-size: 1.1rem;
            margin-bottom: 10px;
        }
        
        .cvh-card .number {
            font-size: 3rem;
            color: white;
            font-weight: bold;
        }
        
        /* Semaines */
        .semaines-table {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            overflow-x: auto;
            margin-bottom: 30px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            color: white;
        }
        
        th {
            background: rgba(139, 92, 246, 0.5);
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* Astrologie */
        .astro-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .astro-section h3 {
            color: #a78bfa;
            font-size: 1.8rem;
            margin-bottom: 20px;
        }
        
        .planetes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .planete-item {
            background: rgba(167, 139, 250, 0.2);
            padding: 15px;
            border-radius: 12px;
            border-left: 4px solid #a78bfa;
        }
        
        .planete-item .nom {
            color: #c4b5fd;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .planete-item .position {
            color: white;
            font-size: 1.1rem;
        }
        
        .maisons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
        }
        
        .maison-item {
            background: rgba(99, 102, 241, 0.2);
            padding: 12px;
            border-radius: 10px;
            text-align: center;
        }
        
        .maison-item .nom {
            color: #93c5fd;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }
        
        .maison-item .signe {
            color: white;
            font-weight: 600;
        }
        
        .error-message {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid #ef4444;
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            display: none;
        }
        
        .error-message.show {
            display: block;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .form-card {
                padding: 25px;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="astro-container">
        <div class="astro-wrapper">
            <!-- Header -->
            <div class="header">
                <h1>ASTROLOGIE & NUMÉROLOGIE</h1>
                <p>Analyse complète de votre thème</p>
            </div>

            <!-- Formulaire -->
            <div class="form-card">
                <div class="form-grid">
                    <div class="form-group">
                        <label>👤 Prénom</label>
                        <input type="text" id="prenom" placeholder="Ex: Robert">
                    </div>
                    <div class="form-group">
                        <label>👤 Nom</label>
                        <input type="text" id="nom" placeholder="Ex: Martinez">
                    </div>
                    <div class="form-group">
                        <label>📅 Date de naissance</label>
                        <input type="text" id="date" placeholder="JJ/MM/AAAA (ex: 24/08/1963)">
                    </div>
                    <div class="form-group">
                        <label>🕐 Heure de naissance</label>
                        <input type="text" id="heure" placeholder="HH:MM (ex: 14:30)">
                    </div>
                    <div class="form-group">
                        <label>📍 Lieu de naissance</label>
                        <input type="text" id="lieu" placeholder="Ex: Paris, Orsay">
                    </div>
                    <div class="form-group">
                        <label>📆 Année de révolution solaire</label>
                        <input type="number" id="annee_rs" placeholder="2025" value="2025">
                    </div>
                </div>
                <button class="calculate-btn" id="calculateBtn" onclick="calculerTheme()">
                    🔮 Calculer le Thème Complet
                </button>
            </div>

            <!-- Loading -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Calcul en cours des positions planétaires...</p>
            </div>

            <!-- Message d'erreur -->
            <div class="error-message" id="errorMessage"></div>

            <!-- Résultats -->
            <div class="results" id="results">
                <!-- Numérologie -->
                <h2 class="section-title">🔢 Numérologie</h2>
                
                <div class="numero-grid">
                    <div class="numero-card">
                        <h3>Chemin de Vie</h3>
                        <div class="big-number" id="cheminVie">-</div>
                    </div>
                </div>

                <div class="cvh-grid">
                    <div class="cvh-card">
                        <h4>CVH 1 - Départ</h4>
                        <div class="number" id="cvh1">-</div>
                    </div>
                    <div class="cvh-card">
                        <h4>CVH 2 - Action</h4>
                        <div class="number" id="cvh2">-</div>
                    </div>
                    <div class="cvh-card">
                        <h4>CVH 3 - Finalité</h4>
                        <div class="number" id="cvh3">-</div>
                    </div>
                </div>

                <div class="semaines-table">
                    <h3 style="color: white; margin-bottom: 20px;">📅 Triangle Numérologique (Périodes de 4 mois)</h3>
                    <div id="triangleDisplay" style="color: white;"></div>
                </div>

                <!-- Astrologie -->
                <h2 class="section-title">🌟 Thème Natal</h2>
                <div class="astro-section" id="themeNatal"></div>

                <h2 class="section-title">☀️ Révolution Solaire <span id="anneeRS"></span></h2>
                <div class="astro-section" id="revolutionSolaire"></div>

                <h2 class="section-title">🔄 Thème Progressé</h2>
                <div class="astro-section" id="themeProgresse"></div>
            </div>
        </div>
    </div>

    <script>
        // URL de ton API sur Render
        const API_URL = 'https://astro-num-rologie-api-6.onrender.com/api/calcul-complet';

        async function calculerTheme() {
            // Récupérer les valeurs
            const prenom = document.getElementById('prenom').value.trim();
            const nom = document.getElementById('nom').value.trim();
            const date = document.getElementById('date').value.trim();
            const heure = document.getElementById('heure').value.trim() || '12:00';
            const lieu = document.getElementById('lieu').value.trim();
            const annee_rs = parseInt(document.getElementById('annee_rs').value) || 2025;

            // Validation
            if (!prenom || !nom || !date || !lieu) {
                afficherErreur('Merci de remplir tous les champs obligatoires !');
                return;
            }

            // Afficher le loading
            document.getElementById('loading').classList.add('show');
            document.getElementById('calculateBtn').disabled = true;
            document.getElementById('results').classList.remove('show');
            document.getElementById('errorMessage').classList.remove('show');

            try {
                // Appel à l'API
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prenom,
                        nom,
                        date,
                        heure,
                        lieu,
                        annee_rs
                    })
                });

                if (!response.ok) {
                    throw new Error('Erreur de communication avec le serveur');
                }

                const data = await response.json();
                
                // Afficher les résultats
                afficherResultats(data);

            } catch (error) {
                console.error('Erreur:', error);
                afficherErreur('Impossible de calculer le thème. Vérifiez que l\'API est en ligne. ' + error.message);
            } finally {
                document.getElementById('loading').classList.remove('show');
                document.getElementById('calculateBtn').disabled = false;
            }
        }

        function afficherResultats(data) {
            const { numerologie, astrologie } = data;

            // Numérologie
            document.getElementById('cheminVie').textContent = numerologie.chemin_vie;
            document.getElementById('cvh1').textContent = numerologie.cvh1;
            document.getElementById('cvh2').textContent = numerologie.cvh2;
            document.getElementById('cvh3').textContent = numerologie.cvh3;

            // Triangle numérologique
            const triangleDiv = document.getElementById('triangleDisplay');
            let triangleHTML = '';
            
            numerologie.lignes.forEach(ligne => {
                triangleHTML += `
                    <div style="margin: 20px 0; padding: 20px; background: rgba(139, 92, 246, 0.2); border-radius: 15px; border-left: 4px solid #8b5cf6;">
                        <h4 style="color: #a78bfa; margin-bottom: 10px;">${ligne.nom}</h4>
                        <div style="display: flex; gap: 15px; justify-content: center; align-items: center; flex-wrap: wrap;">
                `;
                
                ligne.periodes.forEach((periode, index) => {
                    triangleHTML += `
                        <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 20px 30px; border-radius: 12px; min-width: 60px; text-align: center;">
                            <div style="font-size: 2rem; font-weight: bold;">${periode}</div>
                            <div style="font-size: 0.85rem; opacity: 0.8; margin-top: 5px;">4 mois</div>
                        </div>
                    `;
                });
                
                triangleHTML += `
                        </div>
                        <div style="margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">${ligne.description}</div>
                    </div>
                `;
            });
            
            triangleDiv.innerHTML = triangleHTML;

            // Thèmes astrologiques
            afficherTheme('themeNatal', astrologie.theme_natal);
            afficherTheme('revolutionSolaire', astrologie.revolution_solaire);
            afficherTheme('themeProgresse', astrologie.theme_progresse);
            
            document.getElementById('anneeRS').textContent = data.informations.annee_rs;

            // Afficher les résultats
            document.getElementById('results').classList.add('show');
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        }

        function afficherTheme(elementId, theme) {
            const container = document.getElementById(elementId);
            
            let html = '<h3>🪐 Planètes</h3><div class="planetes-grid">';
            
            for (const [nom, data] of Object.entries(theme.planetes)) {
                html += `
                    <div class="planete-item">
                        <div class="nom">${nom}</div>
                        <div class="position">${data.notation}</div>
                    </div>
                `;
            }
            
            html += '</div>';
            
            html += `
                <h3 style="color: #a78bfa; margin-top: 30px; margin-bottom: 15px;">🏠 Maisons</h3>
                <div class="maisons-grid">
            `;
            
            for (const [nom, data] of Object.entries(theme.maisons)) {
                html += `
                    <div class="maison-item">
                        <div class="nom">${nom}</div>
                        <div class="signe">${Math.round(data.degre)}° ${data.signe}</div>
                    </div>
                `;
            }
            
            html += '</div>';
            
            html += `
                <div style="margin-top: 30px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div class="planete-item">
                        <div class="nom">⬆️ Ascendant</div>
                        <div class="position">${Math.round(theme.ascendant.degre)}° ${theme.ascendant.signe}</div>
                    </div>
                    <div class="planete-item">
                        <div class="nom">⬆️ Milieu du Ciel</div>
                        <div class="position">${Math.round(theme.milieu_ciel.degre)}° ${theme.milieu_ciel.signe}</div>
                    </div>
                </div>
            `;
            
            container.innerHTML = html;
        }

        function afficherErreur(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = '❌ ' + message;
            errorDiv.classList.add('show');
            setTimeout(() => errorDiv.classList.remove('show'), 5000);
        }
    </script>
</body>
</html>
