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

## Définition opérationnelle de `fragile_legal` (données synthétiques)

Le vrai critère légal combine plusieurs éléments (dossier de surendettement,
inscription FCC de 3 mois, incidents répétés, 5 incidents/mois combinés à un
critère de ressources). Nos données synthétiques ne modélisent pas
explicitement l'inscription FCC ni le dossier de surendettement — on
approxime donc `fragile_legal` avec deux critères combinés (OU logique) :

1. **Au moins 5 incidents de paiement dans le mois, combinés à des revenus
   sous 1500€** (proxy du critère de ressources modestes — hypothèse
   assumée, pas une valeur réglementaire officielle)
2. **Au moins un incident de paiement pendant 3 mois consécutifs** (proxy
   de l'inscription FCC, qu'on ne génère pas explicitement)

Constat empirique sur les données générées : le critère 1 ne se déclenche
que dans 0.6% des cas (5 incidents simultanés reste un événement rare avec
notre paramétrage), tandis que le critère 2 (persistance) porte l'essentiel
de la détection à 11%. C'est cohérent avec l'esprit du texte réglementaire,
où la répétition d'incidents compte autant qu'un pic isolé.

Distribution finale : `fragile_legal` = 11.2% des mois observés,
`target_fragile_j3m` = 8.3% — une cible ni trop rare ni trop fréquente pour
être exploitable par un modèle.
## Vocabulaire à tenir

Ne jamais présenter le modèle comme décidant qu'un client "est fragile" — parler
de score de vigilance, signal précoce, risque d'apparition d'incidents. Le score
est une aide à la décision humaine, jamais un verdict automatisé.

## Ce que le projet n'est pas

- Pas un vrai dataset bancaire (données 100% synthétiques, à annoncer clairement)
- Pas un outil de scoring de crédit
- Pas une décision réglementaire automatisée