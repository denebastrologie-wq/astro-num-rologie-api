"""
API Flask pour Calculs Astrologiques et Numérologiques
Nécessite: pip install flask flask-cors swisseph skyfield pytz
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
from datetime import datetime, timedelta
import pytz
from skyfield.api import load, wgs84
import math

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis Squarespace
# Route d'accueil
@app.route('/')
def home():
    return jsonify({
        'status': 'OK',
        'message': 'API Astrologie & Numérologie',
        'version': '1.0',
        'endpoints': {
            'test': '/api/test',
            'calcul_complet': '/api/calcul-complet (POST)'
        }
    })

# ==================== NUMÉROLOGIE ====================

TABLE_NUMEROLOGIE = {
    'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2,
    'C': 3, 'L': 3, 'U': 3, 'D': 4, 'M': 4, 'V': 4,
    'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8,
    'I': 9, 'R': 9
}

def reduire_a_22(nombre):
    """Réduit un nombre jusqu'à 22 maximum"""
    chiffre_reduit = nombre
    while chiffre_reduit > 22:
        somme = sum(int(c) for c in str(chiffre_reduit))
        chiffre_reduit = somme
    return chiffre_reduit

def calculer_somme_texte(texte):
    """Calcule la somme numérologique d'un texte"""
    texte = texte.upper().replace(' ', '')
    return sum(TABLE_NUMEROLOGIE.get(lettre, 0) for lettre in texte)

def calculer_chemin_vie(jour, mois, annee):
    """Calcule le chemin de vie"""
    chiffre_jour = reduire_a_22(jour)
    chiffre_mois = reduire_a_22(mois)
    somme_annee = sum(int(c) for c in str(annee))
    chiffre_annee = reduire_a_22(somme_annee)
    return reduire_a_22(chiffre_jour + chiffre_mois + chiffre_annee)

def calculer_cvh(prenom, nom, date_naissance, lieu):
    """Calcule les 3 CVH"""
    jour, mois, annee = date_naissance
    
    # CVH 1 (Nom + Prénom)
    somme_prenom = calculer_somme_texte(prenom)
    somme_nom = calculer_somme_texte(nom)
    cvh1 = reduire_a_22(somme_prenom + somme_nom)
    
    # Chemin de vie
    chemin_vie = calculer_chemin_vie(jour, mois, annee)
    
    # CVH 3 (Date + Lieu)
    somme_lieu = calculer_somme_texte(lieu)
    chiffre_lieu = reduire_a_22(somme_lieu)
    cvh3 = reduire_a_22(chemin_vie + chiffre_lieu)
    
    # CVH 2 (CVH1 + CVH3)
    cvh2 = reduire_a_22(cvh1 + cvh3)
    
    return cvh1, cvh2, cvh3, chemin_vie

def generer_semaines_numerologiques(cvh1, cvh2, cvh3, annee_rs):
    """
    Génère le tableau numérologique sur 6 lignes avec périodes de 4 mois
    
    SYSTÈME DE TRANSITION ANNUELLE :
    - Ligne 1 est une séquence continue qui traverse les années
    - Chaque période = 4 mois
    - Les transitions se calculent entre fin année N-1 et début année N
    """
    
    def reduire_avec_maitres(nombre):
        """Réduit un nombre en conservant 11 et 22"""
        if nombre == 11 or nombre == 22:
            return nombre
        while nombre > 22:
            somme = sum(int(c) for c in str(nombre))
            if somme == 11 or somme == 22:
                return somme
            nombre = somme
        return nombre
    
    # Année actuelle et précédente réduites
    annee_actuelle = reduire_a_22(sum(int(c) for c in str(annee_rs)))
    annee_precedente = reduire_a_22(sum(int(c) for c in str(annee_rs - 1)))
    
    # ===== LIGNE 1 - Séquence continue =====
    # Année précédente (N-1)
    l1_n1_p1 = reduire_avec_maitres(cvh1 + annee_precedente)
    l1_n1_p3 = reduire_avec_maitres(cvh3 + annee_precedente)
    l1_n1_p2 = reduire_avec_maitres(l1_n1_p1 + l1_n1_p3)
    
    # Année actuelle (N)
    l1_n_p1 = reduire_avec_maitres(cvh1 + annee_actuelle)
    l1_n_p3 = reduire_avec_maitres(cvh3 + annee_actuelle)
    l1_n_p2 = reduire_avec_maitres(l1_n_p1 + l1_n_p3)
    
    # La Ligne 1 complète traverse les années : [N-1_p3, N_p1, N_p2, N_p3]
    # Exemple 2024→2025 : [20, 22, 7, 21]
    ligne1 = [l1_n1_p3, l1_n_p1, l1_n_p2, l1_n_p3]
    
    # ===== LIGNE 2 - Additions consécutives =====
    # Chaque nombre = somme de 2 nombres adjacents de Ligne 1
    ligne2 = []
    for i in range(len(ligne1) - 1):
        ligne2.append(reduire_avec_maitres(ligne1[i] + ligne1[i+1]))
    # ligne2 = [20+22, 22+7, 7+21] = [6, 11, 10]
    
    # ===== LIGNE 3 - Additions consécutives =====
    ligne3 = []
    for i in range(len(ligne2) - 1):
        ligne3.append(reduire_avec_maitres(ligne2[i] + ligne2[i+1]))
    # ligne3 = [6+11, 11+10] = [17, 21]
    
    # ===== LIGNE 4 - Additions consécutives =====
    ligne4 = []
    for i in range(len(ligne3) - 1):
        ligne4.append(reduire_avec_maitres(ligne3[i] + ligne3[i+1]))
    # ligne4 = [17+21] = [11]
    
    # ===== LIGNE 5 - Si possible =====
    ligne5 = []
    if len(ligne4) > 1:
        for i in range(len(ligne4) - 1):
            ligne5.append(reduire_avec_maitres(ligne4[i] + ligne4[i+1]))
    
    # ===== LIGNE 6 - Si possible =====
    ligne6 = []
    if len(ligne5) > 1:
        for i in range(len(ligne5) - 1):
            ligne6.append(reduire_avec_maitres(ligne5[i] + ligne5[i+1]))
    
    # Construction du résultat avec toutes les lignes
    lignes = [
        {
            "ligne": 1,
            "nom": "Ligne 1 - Base année",
            "periodes": ligne1,
            "description": f"Transition {annee_rs-1}→{annee_rs}"
        },
        {
            "ligne": 2,
            "nom": "Ligne 2",
            "periodes": ligne2,
            "description": "Additions consécutives"
        },
        {
            "ligne": 3,
            "nom": "Ligne 3",
            "periodes": ligne3,
            "description": "Niveau intermédiaire"
        },
        {
            "ligne": 4,
            "nom": "Ligne 4",
            "periodes": ligne4,
            "description": "Synthèse"
        }
    ]
    
    if ligne5:
        lignes.append({
            "ligne": 5,
            "nom": "Ligne 5",
            "periodes": ligne5,
            "description": "Convergence"
        })
    
    if ligne6:
        lignes.append({
            "ligne": 6,
            "nom": "Ligne 6",
            "periodes": ligne6,
            "description": "Point final"
        })
    
    return lignes

# ==================== ASTROLOGIE ====================

# Initialiser Swiss Ephemeris
swe.set_ephe_path(None)  # Utilise les éphémérides par défaut

PLANETES = {
    'Soleil': swe.SUN,
    'Lune': swe.MOON,
    'Mercure': swe.MERCURY,
    'Vénus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturne': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluton': swe.PLUTO
}

SIGNES = [
    "Bélier", "Taureau", "Gémeaux", "Cancer",
    "Lion", "Vierge", "Balance", "Scorpion",
    "Sagittaire", "Capricorne", "Verseau", "Poissons"
]

def coords_to_lat_lon(lieu_str):
    """Convertit un lieu en coordonnées (simplifié - à améliorer avec geocoding)"""
    # Base de données simplifiée
    lieux = {
        'paris': (48.8566, 2.3522),
        'orsay': (48.6981, 2.1878),
        'lyon': (45.7640, 4.8357),
        'marseille': (43.2965, 5.3698),
        'toulouse': (43.6047, 1.4442),
    }
    lieu_lower = lieu_str.lower().strip()
    return lieux.get(lieu_lower, (48.8566, 2.3522))  # Paris par défaut

def calcul_date_julienne(dt):
    """Convertit une date en jour julien"""
    return swe.julday(dt.year, dt.month, dt.day, 
                      dt.hour + dt.minute/60.0 + dt.second/3600.0)

def calculer_theme_natal(dt, lat, lon):
    """Calcule le thème natal complet"""
    jd = calcul_date_julienne(dt)
    
    # Positions planétaires
    positions = {}
    for nom, code in PLANETES.items():
        pos = swe.calc_ut(jd, code)[0]
        longitude = pos[0]
        signe_idx = int(longitude / 30)
        degre_dans_signe = longitude % 30
        
        positions[nom] = {
            'longitude': round(longitude, 2),
            'signe': SIGNES[signe_idx],
            'degre': round(degre_dans_signe, 2),
            'notation': f"{round(degre_dans_signe)}°{SIGNES[signe_idx]}"
        }
    
    # Maisons (système Placidus)
    maisons_data = swe.houses(jd, lat, lon, b'P')
    maisons = {}
    
    for i, cuspide in enumerate(maisons_data[0][:12], 1):
        signe_idx = int(cuspide / 30)
        degre = cuspide % 30
        maisons[f"Maison {i}"] = {
            'longitude': round(cuspide, 2),
            'signe': SIGNES[signe_idx],
            'degre': round(degre, 2)
        }
    
    # Points spéciaux
    asc = maisons_data[0][0]
    mc = maisons_data[0][9]
    
    return {
        'planetes': positions,
        'maisons': maisons,
        'ascendant': {
            'longitude': round(asc, 2),
            'signe': SIGNES[int(asc / 30)],
            'degre': round(asc % 30, 2)
        },
        'milieu_ciel': {
            'longitude': round(mc, 2),
            'signe': SIGNES[int(mc / 30)],
            'degre': round(mc % 30, 2)
        }
    }

def calculer_revolution_solaire(dt_naissance, annee_rs, lat, lon):
    """Calcule la révolution solaire pour une année donnée"""
    # Position du Soleil natal
    jd_natal = calcul_date_julienne(dt_naissance)
    pos_soleil_natal = swe.calc_ut(jd_natal, swe.SUN)[0][0]
    
    # Chercher la date exacte de RS dans l'année donnée
    dt_approx = datetime(annee_rs, dt_naissance.month, dt_naissance.day, 12, 0)
    
    # Affiner la recherche (à +/- 2 jours)
    for delta_heures in range(-48, 49):
        dt_test = dt_approx + timedelta(hours=delta_heures)
        jd_test = calcul_date_julienne(dt_test)
        pos_soleil = swe.calc_ut(jd_test, swe.SUN)[0][0]
        
        # Si on est à moins de 0.1° de la position natale
        if abs(pos_soleil - pos_soleil_natal) < 0.1:
            return calculer_theme_natal(dt_test, lat, lon)
    
    # Fallback: utiliser la date approximative
    return calculer_theme_natal(dt_approx, lat, lon)

def calculer_theme_progresse(dt_naissance, date_actuelle, lat, lon):
    """
    Calcule le thème progressé (1 jour = 1 an)
    Progression secondaire
    """
    jours_ecoules = (date_actuelle - dt_naissance).days
    annees_ecoulees = jours_ecoules / 365.25
    
    # Date progressée = naissance + nombre d'années en jours
    dt_progresse = dt_naissance + timedelta(days=annees_ecoulees)
    
    return calculer_theme_natal(dt_progresse, lat, lon)

# ==================== API ROUTES ====================

@app.route('/api/calcul-complet', methods=['POST'])
def calcul_complet():
    """
    Endpoint principal pour tous les calculs
    
    Body JSON:
    {
        "prenom": "Robert",
        "nom": "Martinez",
        "date": "24/08/1963",
        "heure": "14:30",
        "lieu": "Orsay",
        "annee_rs": 2025
    }
    """
    try:
        data = request.json
        
        # Extraction des données
        prenom = data['prenom']
        nom = data['nom']
        date_str = data['date']  # format: DD/MM/YYYY
        heure_str = data.get('heure', '12:00')  # format: HH:MM
        lieu = data['lieu']
        annee_rs = data.get('annee_rs', datetime.now().year)
        
        # Parser la date et l'heure
        jour, mois, annee = map(int, date_str.split('/'))
        heure, minute = map(int, heure_str.split(':'))
        
        dt_naissance = datetime(annee, mois, jour, heure, minute)
        lat, lon = coords_to_lat_lon(lieu)
        
        # === CALCULS NUMÉROLOGIQUES ===
        cvh1, cvh2, cvh3, chemin_vie = calculer_cvh(
            prenom, nom, (jour, mois, annee), lieu
        )
        
        semaines = generer_semaines_numerologiques(cvh1, cvh2, cvh3, annee_rs)
        
        # === CALCULS ASTROLOGIQUES ===
        theme_natal = calculer_theme_natal(dt_naissance, lat, lon)
        revolution_solaire = calculer_revolution_solaire(dt_naissance, annee_rs, lat, lon)
        theme_progresse = calculer_theme_progresse(dt_naissance, datetime.now(), lat, lon)
        
        # === RÉSULTAT COMPLET ===
        resultat = {
            'numerologie': {
                'cvh1': cvh1,
                'cvh2': cvh2,
                'cvh3': cvh3,
                'chemin_vie': chemin_vie,
                'lignes': semaines  # Changé de 'semaines' à 'lignes'
            },
            'astrologie': {
                'theme_natal': theme_natal,
                'revolution_solaire': revolution_solaire,
                'theme_progresse': theme_progresse
            },
            'informations': {
                'nom_complet': f"{prenom} {nom}",
                'date_naissance': dt_naissance.strftime('%d/%m/%Y %H:%M'),
                'lieu': lieu,
                'coordonnees': {'latitude': lat, 'longitude': lon},
                'annee_rs': annee_rs
            }
        }
        
        return jsonify(resultat), 200
        
    except Exception as e:
        return jsonify({'erreur': str(e)}), 400

@app.route('/api/test', methods=['GET'])
def test():
    """Route de test pour vérifier que l'API fonctionne"""
    return jsonify({
        'status': 'OK',
        'message': 'API Astrologie/Numérologie fonctionnelle',
        'version': '1.0'
    })

# ==================== LANCEMENT ====================

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
