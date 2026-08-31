with transactions as (
    select * from {{ ref('stg_transactions') }}
),

fragility_flags as (
    select
        client_id,
        mois,
        case
            when nb_incidents_paiement >= 5 and revenus_entrants < 1500 then 1
            else 0
        end as critere_incidents_ressources,
        case when nb_incidents_paiement >= 1 then 1 else 0 end as a_incident_ce_mois
    from transactions
),

with_consecutive as (
    select
        *,
        sum(a_incident_ce_mois) over (
            partition by client_id order by mois
            rows between 2 preceding and current row
        ) as incidents_somme_3m
    from fragility_flags
),

fragile_legal_calc as (
    -- Voir docs/00_business_context.md pour la justification de ces 2 criteres
    select
        client_id,
        mois,
        case
            when critere_incidents_ressources = 1 then 1
            when incidents_somme_3m = 3 then 1
            else 0
        end as fragile_legal
    from with_consecutive
),

with_future_targets as (
    select
        client_id,
        mois,
        fragile_legal,
        lead(fragile_legal, 1) over (partition by client_id order by mois) as fragile_legal_lead1,
        lead(fragile_legal, 2) over (partition by client_id order by mois) as fragile_legal_lead2,
        lead(fragile_legal, 3) over (partition by client_id order by mois) as fragile_legal_lead3
    from fragile_legal_calc
),

target as (
    select
        client_id,
        mois,
        fragile_legal,
        case
            when fragile_legal = 0
                and (fragile_legal_lead1 = 1 or fragile_legal_lead2 = 1 or fragile_legal_lead3 = 1)
            then 1
            else 0
        end as target_fragile_j3m
    from with_future_targets
    -- On exclut les mois trop proches de la fin pour eviter un horizon tronque
    where mois <= (select max(mois) from transactions) - 3
),

features as (
    select * from {{ ref('int_monthly_features') }}
),

clients as (
    select * from {{ ref('stg_clients') }}
)

select
    f.client_id,
    f.mois,
    c.age,
    c.statut_pro,
    c.anciennete_mois,
    f.revenus_entrants,
    f.revenus_entrants_lag1,
    f.revenus_entrants_delta,
    f.revenus_entrants_roll3,
    f.revenus_entrants_roll6,
    f.nb_incidents_roll3,
    f.nb_decouverts_roll3,
    f.ratio_charges_revenu,
    t.fragile_legal,
    t.target_fragile_j3m
from features f
inner join target t
    on f.client_id = t.client_id and f.mois = t.mois
left join clients c
    on f.client_id = c.client_id