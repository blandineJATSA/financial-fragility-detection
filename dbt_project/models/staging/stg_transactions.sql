select
    client_id,
    mois,
    revenus_entrants,
    depenses_contraintes,
    depenses_variables,
    solde_fin_mois,
    nb_incidents_paiement,
    nb_decouverts
from {{ source('raw', 'transactions') }}