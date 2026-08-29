"""Point d'entree : orchestre la generation complete des donnees synthetiques."""

import os

from data_generation.config import N_CLIENTS, N_MONTHS, RANDOM_SEED
from data_generation.generate_clients import generate_clients
from data_generation.generate_transactions import generate_transactions


def main() -> None:
    os.makedirs("data/raw", exist_ok=True)

    clients = generate_clients(N_CLIENTS, RANDOM_SEED)
    transactions = generate_transactions(clients, N_MONTHS, RANDOM_SEED)

    clients.to_parquet("data/raw/clients.parquet", index=False)
    transactions.to_parquet("data/raw/transactions.parquet", index=False)

    print(f"Genere : {len(clients)} clients, {len(transactions)} lignes de transactions.")
    print(f"Repartition des profils :")
    print(clients["profil_trajectoire"].value_counts(normalize=True))


if __name__ == "__main__":
    main()