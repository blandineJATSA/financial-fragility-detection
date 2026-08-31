select
    client_id,
    age,
    statut_pro,
    anciennete_mois
from {{ source('raw', 'clients') }}