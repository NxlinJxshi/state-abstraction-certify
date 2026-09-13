# scripts/plot_throughput.py
import matplotlib.pyplot as plt

# {concurrency: tokens/sec} dict printed by bench_throughput.py
results = {1: 173.03068813835486, 5: 766.3855558949398, 10: 1002.5507884927626, 20: 3000.908018187167}

plt.plot(list(results.keys()), list(results.values()), marker="o")
plt.xlabel("Concurrent requests (rollouts in flight)")
plt.ylabel("Output tokens/sec")
plt.title("vLLM throughput — Qwen3-1.7B on RTX PRO 4500 SE (Blackwell)")
plt.grid(True, alpha=0.3)
plt.savefig("scripts/throughput_plot.png", dpi=150)
print("saved scripts/throughput_plot.png")
