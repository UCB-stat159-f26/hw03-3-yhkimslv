import matplotlib.pyplot as plt

from tenniscareer import get_career_data, plot_career


serena = get_career_data("serena williams")

print("Serena Williams")
print(serena.head())

ax = plot_career(serena)
ax.figure.savefig("serena_career.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)

rafael = get_career_data("Rafael Nadal")

print("Rafael Nadal")
print(rafael.head())

ax = plot_career(rafael)
ax.figure.savefig("rafael_career.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)

print("Saved: serena_career.png and rafael_career.png")