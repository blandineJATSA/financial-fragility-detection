# Dashboard — spécification

Livrable final : application Streamlit à **2 pages**, pas plus (voir
justification dans le document d'architecture du dépôt).

## Page 1 — Vue globale

- 4 KPI : clients suivis, signaux détectés ce mois, délai moyen d'avance de
  détection, taux de couverture
- Graphe : signaux précoces vs incidents réglementaires (18 mois)
- Graphe : répartition des clients par niveau de vigilance
- Table filtrable des clients à vigilance élevée/critique
- Filtres sidebar : période, segment

## Page 2 — Profil client

- Sélecteur de client_id
- Badge de score (niveau de vigilance + valeur /100)
- Courbe de solde sur 18 mois, seuil réglementaire en pointillé
- Barres SHAP : 5 facteurs expliquant le score
- Encart recommandation, avec rappel que c'est une aide à l'analyse

## Statut

TODO — non codé à ce stade.