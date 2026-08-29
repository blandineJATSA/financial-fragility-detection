# Éthique et limites

## Vocabulaire à tenir

Ne jamais présenter le modèle comme décidant qu'un client "est fragile" —
parler de score de vigilance, signal précoce, risque d'apparition
d'incidents. Le score est une aide à la décision humaine, jamais un verdict
automatisé.

## Données synthétiques

Ce projet utilise exclusivement des données synthétiques, générées pour
simuler des trajectoires réalistes de clients (stable, dégradation
progressive, fragile dès le départ). Ce n'est pas un dispositif réglementaire
bancaire réel et ne doit pas être présenté comme tel.

## Proxys à éviter dans les features

Ne jamais inclure de variable pouvant servir de proxy à une caractéristique
protégée (origine, genre, situation de handicap...). Le code postal ou la
région, par exemple, doivent être utilisés avec prudence s'ils sont ajoutés
plus tard.

## Fuite d'information

`profil_trajectoire` (colonne de génération) ne doit jamais être utilisée
comme feature — voir `01_data_dictionary.md`.

## Trade-off faux positifs / faux négatifs

Rater un client réellement fragile a un coût humain et réglementaire plus
élevé qu'une fausse alerte. Ce déséquilibre doit se refléter dans le choix du
seuil de décision du modèle, pas seulement dans l'accuracy globale.

## Objectif du modèle

Le score doit déclencher un accompagnement ou une offre protectrice, jamais
une exclusion ou un refus de service.