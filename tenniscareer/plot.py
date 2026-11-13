import matplotlib.pyplot as plt


def plot_career(data):
    required = {"player_age", "age_diff", "result"}
    if data.empty or not required.issubset(data.columns):
        raise ValueError("Use a nonempty DataFrame from get_career_data().")
    wins = data[data["result"] == "W"]
    losses = data[data["result"] == "L"]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(wins["player_age"], wins["age_diff"], color="teal", label="Win", s=15)
    ax.scatter(losses["player_age"], losses["age_diff"], color="salmon", label="Loss", s=15)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("Player age (years)")
    ax.set_ylabel("Player age - Opponent age (years)")
    ax.set_title(data.attrs.get("player_name", "Career matches"))
    ax.legend()
    fig.tight_layout()
    return ax