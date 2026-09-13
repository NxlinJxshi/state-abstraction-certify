import concurrent.futures
import time

from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
MODEL = "Qwen/Qwen3-1.7B"
PROMPT = "Explain the plan-then-execute pattern for LLM agents in two sentences."

def one_call(_):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        max_tokens=256,
    )
    return resp.usage.completion_tokens

def run(concurrency: int, n_requests: int = 20):
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        token_counts = list(ex.map(one_call, range(n_requests)))
    elapsed = time.perf_counter() - start
    total_tokens = sum(token_counts)
    tput = total_tokens / elapsed
    print(f"concurrency={concurrency:>3}  tokens/sec={tput:>8.1f}  wall_clock={elapsed:.2f}s")
    return tput

if __name__ == "__main__":
    results = {c: run(c) for c in [1, 5, 10, 20]}
    print(results)
