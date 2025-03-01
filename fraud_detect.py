import networkx as nx
import community
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from database import fetch_transactions


def detect_fraud_communities(transactions, min_amount=5000, time_window_days=30, visualize=False):
    """
    Detects fraud communities using graph-based analysis.

    Parameters:
    - transactions: List of transaction dictionaries with sender, receiver, amount, and date.
    - min_amount: Minimum transaction amount to consider (default: 5000).
    - time_window_days: Time window in days to detect rapid transactions (default: 30).
    - visualize: If True, plots the fraud network.

    Returns:
    - Dictionary mapping community IDs to lists of account numbers.
    """

    G = nx.Graph()
    recent_cutoff = datetime.now() - timedelta(days=time_window_days)

    # Add transactions as edges (filtering based on amount and date)
    for transaction in transactions:
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]
        date = transaction["date"]

        if amount >= min_amount and date >= recent_cutoff:
            if G.has_edge(sender, receiver):
                G[sender][receiver]["weight"] += amount  # Aggregate transactions
            else:
                G.add_edge(sender, receiver, weight=amount)

    # Detect fraud communities using the Louvain algorithm
    if len(G.nodes) == 0:
        print("No significant transactions detected for fraud analysis.")
        return {}

    partition = community.best_partition(G)

    # Group accounts by community
    community_accounts = defaultdict(list)
    for account, comm_id in partition.items():
        community_accounts[comm_id].append(account)

    # Visualization (optional)
    if visualize:
        visualize_fraud_network(G, partition)

    return community_accounts


def visualize_fraud_network(G, partition):
    """
    Plots the fraud transaction network with detected communities.

    Parameters:
    - G: The transaction graph.
    - partition: Community mapping from detect_fraud_communities().
    """

    pos = nx.spring_layout(G, seed=42)  # Consistent layout
    cmap = plt.get_cmap("viridis")
    unique_communities = set(partition.values())

    # Draw nodes with colors representing communities
    for community_id in unique_communities:
        nodes = [node for node in partition if partition[node] == community_id]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=[cmap(community_id / len(unique_communities))], node_size=500, alpha=0.8)

    # Draw edges with varying thickness based on transaction weight
    edges = [(u, v) for u, v in G.edges()]
    weights = [G[u][v]["weight"] / 1000 for u, v in G.edges()]  # Normalize weights
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, alpha=0.6)

    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    plt.title("Fraudulent Transaction Network")
    plt.show()


# Fetch transactions from database
transactions = fetch_transactions()
fraud_groups = detect_fraud_communities(transactions, visualize=True)

print("🚨 Detected Fraud Communities 🚨")
for group_id, accounts in fraud_groups.items():
    if len(accounts) > 3:  # Communities with >3 members might indicate fraud rings
        print(f"Community {group_id}: {accounts}")
