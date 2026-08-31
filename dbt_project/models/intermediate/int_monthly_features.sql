with transactions as (
    select * from {{ ref('stg_transactions') }}
),

with_lags_and_deltas as (
    select
        client_id,
        mois,
        revenus_entrants,
        depenses_contraintes,
        depenses_variables,
        solde_fin_mois,
        nb_incidents_paiement,
        nb_decouverts,

        lag(revenus_entrants) over (partition by client_id order by mois) as revenus_entrants_lag1,
        revenus_entrants - lag(revenus_entrants) over (partition by client_id order by mois) as revenus_entrants_delta,

        avg(revenus_entrants) over (
            partition by client_id order by mois
            rows between 2 preceding and current row
        ) as revenus_entrants_roll3,

        avg(revenus_entrants) over (
            partition by client_id order by mois
            rows between 5 preceding and current row
        ) as revenus_entrants_roll6,

        avg(nb_incidents_paiement) over (
            partition by client_id order by mois
            rows between 2 preceding and current row
        ) as nb_incidents_roll3,

        avg(nb_decouverts) over (
            partition by client_id order by mois
            rows between 2 preceding and current row
        ) as nb_decouverts_roll3,

        -- Plafonne a 3.0 : au-dela, c'est deja une detresse financiere extreme,
        -- le plafond evite que quelques valeurs aberrantes (revenu quasi nul un mois)
        -- n'ecrasent l'echelle du ratio pour tous les autres clients
        least(safe_divide(depenses_contraintes, nullif(revenus_entrants, 0)), 3.0) as ratio_charges_revenu

    from transactions
)

select * from with_lags_and_deltas