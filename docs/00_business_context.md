# Contexte métier

Depuis la loi de 2013, les banques françaises ont l'obligation légale de détecter
leurs clients en situation de fragilité financière et de leur proposer une offre
spécifique plafonnée. Les critères réglementaires (5 incidents/mois combinés à un
critère de ressources, inscription 3 mois au FCC, dossier de surendettement
recevable) détectent la fragilité une fois qu'elle est déjà installée.

## Problème métier

Détecter les signaux précoces de fragilité, avant que le client n'atteigne ces
seuils réglementaires, à partir de son comportement transactionnel — pour
permettre une action préventive plutôt que réactive.

## Définition de la cible

`target_fragile_j3m` : le client atteindra `fragile_legal = True` dans les 3
prochains mois, alors qu'il ne l'est pas encore au mois M. Le split
entraînement/test se fait par le temps, jamais aléatoirement.

## Vocabulaire à tenir

Ne jamais présenter le modèle comme décidant qu'un client "est fragile" — parler
de score de vigilance, signal précoce, risque d'apparition d'incidents. Le score
est une aide à la décision humaine, jamais un verdict automatisé.

## Ce que le projet n'est pas

- Pas un vrai dataset bancaire (données 100% synthétiques, à annoncer clairement)
- Pas un outil de scoring de crédit
- Pas une décision réglementaire automatisée