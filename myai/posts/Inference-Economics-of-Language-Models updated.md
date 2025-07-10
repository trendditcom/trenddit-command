## Three Key Insights

1. **Network latency, not bandwidth, is the critical bottleneck for fast LLM inference.** While network bandwidth limits are commonly discussed, they only become dominant with very large tensors (>10 MB) requiring per-GPU batch sizes of 500+. For practical fast inference scenarios, network communication time is dominated by latency constraints rather than bandwidth limitations.

2. **Token generation speed follows predictable scaling laws based on model size and hardware.** Dense Transformer inference speed scales roughly with the inverse square root of parameter count and the cube root of GPU memory bandwidth. These scaling relationships provide useful "order of magnitude" comparisons for inference performance planning.

3. **Speculative decoding can double inference speed without increasing costs or reducing performance.** This technique amortizes memory bandwidth and network latency costs over multiple tokens by generating many tokens in a single forward pass, making it particularly effective for large model inference where these factors are the primary bottlenecks.