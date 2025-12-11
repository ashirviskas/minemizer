# Minemizer Benchmark Report

Compare [minemizer](https://github.com/ashirviskas/minemizer) to other encoding formats for LLM token efficiency.

## Summary

*Efficiency = Accuracy × (JSON tokens ÷ Format tokens)*

### nested_1000

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| minemizer | 1.18 | 47.8% | 33.5k | 6.9 |
| minemizer_compact | 1.14 | 44.2% | 32.1k | 7.2 |
| minemizer_compact_no_repeat | 1.06 | 40.8% | 31.9k | 7.2 |
| minemizer_no_repeat | 1.02 | 41.0% | 33.3k | 6.9 |
| tson | 0.84 | 30.0% | 29.7k | 7.7 |
| yaml | 0.69 | 49.0% | 58.5k | 3.9 |
| json_min | 0.67 | 39.2% | 48.9k | 4.7 |
| toon | 0.62 | 44.8% | 59.6k | 3.9 |
| json_pretty | 0.42 | 42.5% | 82.9k | 2.8 |

## Compression Benchmarks

### simple_flat

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 763 | 384 | 334 | 264 | 270 |
| json_min | 522 | 152 | 165 | 137 | 150 |
| csv | 234 | 95 | 101 | 77 | 91 |
| tsv | 234 | 95 | 101 | 77 | 92 |
| yaml | 489 | 163 | 180 | 169 | 172 |
| toon | 246 | 98 | 103 | 96 | 93 |
| tson | 229 | 90 | 95 | 80 | 86 |
| minemizer | 251 | 74 | 83 | 72 | 75 |
| minemizer_compact | 224 | 85 | 91 | 77 | 83 |

### nested_objects

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 1,039 | 590 | 435 | 348 | 349 |
| json_min | 618 | 188 | 211 | 174 | 187 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 629 | 264 | 246 | 229 | 228 |
| toon | 675 | 315 | 238 | 223 | 224 |
| tson | 306 | 136 | 141 | 110 | 124 |
| minemizer | 325 | 126 | 132 | 121 | 120 |
| minemizer_compact | 290 | 132 | 139 | 117 | 119 |

### lists_of_primitives

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 610 | 382 | 280 | 217 | 223 |
| json_min | 330 | 115 | 125 | 103 | 115 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 341 | 153 | 157 | 149 | 152 |
| toon | 339 | 161 | 141 | 137 | 142 |
| tson | 168 | 80 | 79 | 65 | 78 |
| minemizer | 188 | 81 | 79 | 71 | 68 |
| minemizer_compact | 165 | 83 | 83 | 70 | 71 |

### sparse_data

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 611 | 323 | 285 | 227 | 229 |
| json_min | 400 | 131 | 146 | 121 | 126 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 384 | 145 | 158 | 149 | 150 |
| toon | 438 | 190 | 167 | 159 | 160 |
| tson | 328 | 146 | 145 | 113 | 117 |
| minemizer | 200 | 72 | 79 | 72 | 73 |
| minemizer_compact | 180 | 82 | 88 | 74 | 76 |

### complex_mixed

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 1,320 | 768 | 560 | 455 | 428 |
| json_min | 760 | 224 | 284 | 246 | 239 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 818 | 374 | 338 | 306 | 279 |
| toon | 881 | 434 | 329 | 304 | 279 |
| tson | 453 | 207 | 237 | 203 | 194 |
| minemizer | 403 | 157 | 203 | 193 | 161 |
| minemizer_compact | 361 | 173 | 214 | 190 | 159 |

### books

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 27,902 | 12,188 | 11,626 | 9,434 | 8,955 |
| json_min | 22,501 | 7,103 | 8,035 | 6,637 | 6,166 |
| csv | 14,071 | 5,354 | 6,151 | 4,799 | 4,463 |
| tsv | 14,057 | 5,564 | 6,360 | 4,883 | 4,680 |
| yaml | 22,400 | 8,081 | 8,859 | 7,605 | 7,159 |
| toon | 14,277 | 5,388 | 6,172 | 4,866 | 4,435 |
| tson | 14,448 | 5,433 | 6,229 | 4,845 | 4,484 |
| minemizer | 14,458 | 5,152 | 6,042 | 4,976 | 4,520 |
| minemizer_compact | 13,753 | 5,260 | 6,056 | 4,847 | 4,387 |

### countries

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 1,133,948 | 677,260 | 565,880 | 474,014 | 402,626 |
| json_min | 787,962 | 339,487 | 425,660 | 365,037 | 304,093 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 641,939 | 345,580 | 251,610 | 219,269 | 206,631 |
| toon | 691,140 | 397,301 | 246,360 | 215,450 | 202,875 |
| tson | 423,383 | 210,056 | 196,499 | 158,349 | 158,554 |
| minemizer | 324,916 | 167,101 | 152,897 | 134,184 | 120,629 |
| minemizer_compact | 301,053 | 171,367 | 156,942 | 134,101 | 124,714 |

### large_non_uniform_nested_mixed

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 2,402 | 1,292 | 1,003 | 816 | 802 |
| json_min | 1,500 | 446 | 522 | 449 | 457 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 1,573 | 661 | 617 | 559 | 533 |
| toon | 1,766 | 841 | 625 | 572 | 545 |
| tson | 1,275 | 525 | 560 | 462 | 489 |
| minemizer | 1,203 | 383 | 452 | 400 | 389 |
| minemizer_compact | 1,072 | 409 | 462 | 382 | 385 |

### large_non_uniform_nested_numerical

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 2,947 | 1,718 | 1,542 | 1,332 | 1,170 |
| json_min | 1,873 | 755 | 976 | 884 | 749 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 2,085 | 1,033 | 1,171 | 1,077 | 894 |
| toon | 2,318 | 1,249 | 1,178 | 1,090 | 906 |
| tson | 1,642 | 823 | 993 | 907 | 747 |
| minemizer | 1,534 | 632 | 940 | 883 | 699 |
| minemizer_compact | 1,361 | 676 | 875 | 809 | 642 |

### large_non_uniform_nested_text

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 4,214 | 1,498 | 1,268 | 997 | 986 |
| json_min | 3,359 | 658 | 792 | 634 | 647 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 3,387 | 818 | 843 | 716 | 703 |
| toon | 3,534 | 974 | 846 | 718 | 705 |
| tson | 3,173 | 721 | 831 | 644 | 689 |
| minemizer | 2,809 | 522 | 619 | 510 | 500 |
| minemizer_compact | 2,694 | 565 | 672 | 534 | 527 |

### mcp_tools_list

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek |
|--------|-------|------|------|------|------|
| json_pretty | 51,663 | 27,574 | 13,539 | 11,210 | 11,303 |
| json_min | 30,724 | 6,840 | 7,315 | 6,368 | 6,977 |
| csv | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A |
| yaml | 38,139 | 16,770 | 8,915 | 7,927 | 7,997 |
| toon | 38,376 | 17,296 | 8,649 | 7,670 | 7,767 |
| tson | 25,878 | 7,318 | 7,045 | 5,889 | 6,731 |
| minemizer | 23,383 | 5,559 | 5,767 | 5,319 | 5,342 |
| minemizer_compact | 21,912 | 5,672 | 5,726 | 5,112 | 5,216 |

## LLM Accuracy Benchmarks

### Phi-4-mini-instruct-Q8_0 on nested_1000

*50 queries, 2025-12-02*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| minemizer_compact | 38.0% | 29.0k | 1615ms |
| minemizer_compact_no_repeat | 38.0% | 28.9k | 1428ms |
| json_pretty | 36.0% | 79.8k | 6448ms |
| minemizer | 36.0% | 30.5k | 1998ms |
| tson | 32.0% | 27.3k | 1708ms |
| minemizer_no_repeat | 30.0% | 30.4k | 1687ms |
| toon | 18.0% | 56.6k | 4035ms |
| yaml | 12.0% | 55.6k | 4110ms |
| json_min | 4.0% | 45.8k | 3493ms |

### Qwen3-VL-30B-A3B-Instruct-Q4_K_M.gguf on nested_1000

*20 queries, 2025-12-01*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| yaml | 80.0% | 61.4k | 18577ms |
| json_min | 65.0% | 51.9k | 11098ms |
| toon | 65.0% | 62.4k | 19448ms |
| minemizer | 65.0% | 36.3k | 8367ms |
| minemizer_compact | 65.0% | 35.1k | 8172ms |
| minemizer_compact_no_repeat | 55.0% | 34.9k | 7569ms |
| json_pretty | 50.0% | 85.9k | 2795ms |
| minemizer_no_repeat | 50.0% | 36.2k | 7958ms |
| tson | 30.0% | 32.1k | 7133ms |

### Qwen3-VL-8B-Instruct-Q8_0 on nested_1000

*50 queries, 2025-12-02*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| minemizer | 58.0% | 36.3k | 3175ms |
| yaml | 56.0% | 61.4k | 6600ms |
| minemizer_compact | 56.0% | 35.1k | 3202ms |
| minemizer_no_repeat | 54.0% | 36.2k | 3166ms |
| tson | 50.0% | 32.1k | 2883ms |
| minemizer_compact_no_repeat | 50.0% | 34.9k | 3080ms |
| toon | 46.0% | 62.4k | 6255ms |
| json_min | 44.0% | 51.9k | 4151ms |
| json_pretty | 40.0% | 85.9k | 10601ms |

### gpt-oss-20b-Q8_0-low on nested_1000

*50 queries, 2025-12-02*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| toon | 50.0% | 56.7k | 3788ms |
| yaml | 48.0% | 55.7k | 3689ms |
| json_pretty | 44.0% | 79.9k | 5081ms |
| json_min | 44.0% | 45.9k | 3073ms |
| minemizer | 32.0% | 30.6k | 2818ms |
| minemizer_no_repeat | 30.0% | 30.4k | 2691ms |
| minemizer_compact_no_repeat | 20.0% | 28.9k | 2672ms |
| minemizer_compact | 18.0% | 29.1k | 2918ms |
| tson | 8.0% | 27.4k | 2804ms |
