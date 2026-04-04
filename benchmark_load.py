import time
import psutil
import pandas as pd
import numpy as np
from ml.streaming_ml_engine import PipelineOrchestrator

def run_benchmark(duration_sec=30):
    print(f"Starting CommandX Performance Benchmark ({duration_sec}s)...")
    
    # Initialize the high-frequency pipeline
    # 100Hz is a high load for this simulation
    streamer = PipelineOrchestrator(frequency_hz=100, buffer_duration_sec=30)
    streamer.start()
    
    cpu_usage = []
    mem_usage = []
    latencies = []
    throughputs = []
    
    process = psutil.Process()
    
    start_time = time.time()
    while time.time() - start_time < duration_sec:
        # Measure system footprint
        cpu_usage.append(process.cpu_percent(interval=None))
        mem_usage.append(process.memory_info().rss / (1024 * 1024)) # MB
        
        # Get pipeline metrics
        metrics = streamer.get_metrics()
        latencies.append(metrics['latency_ms'])
        throughputs.append(metrics['throughput_hz'])
        
        time.sleep(0.5)
    
    streamer.stop()
    
    df = pd.DataFrame({
        'CPU (%)': cpu_usage,
        'Memory (MB)': mem_usage,
        'Latency (ms)': latencies,
        'Throughput (Hz)': throughputs
    })
    
    stats = df.describe().loc[['mean', 'max', 'std']]
    print("\nBenchmark Results:")
    print(stats)
    
    # Save to CSV for README reference
    df.to_csv('results/load_benchmark_results.csv', index=False)
    print("\nResults saved to results/load_benchmark_results.csv")

if __name__ == "__main__":
    run_benchmark()
