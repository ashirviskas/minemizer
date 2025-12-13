# Minemizer Benchmark Report

Compare [minemizer](https://github.com/ashirviskas/minemizer) to other encoding formats for LLM token efficiency.

## Summary

*Efficiency = Accuracy × (JSON tokens ÷ Format tokens)*

### flat_100

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| csv | 1.86 | 82.0% | 3.8k | 5.6 |
| tsv | 1.83 | 81.0% | 3.8k | 5.6 |
| minemizer_compact | 1.80 | 79.0% | 3.8k | 5.6 |
| minemizer_compact_no_repeat | 1.80 | 79.0% | 3.8k | 5.6 |
| toon | 1.80 | 80.0% | 3.8k | 5.6 |
| minemizer | 1.61 | 73.0% | 3.9k | 5.5 |
| minemizer_no_repeat | 1.61 | 73.0% | 3.9k | 5.5 |
| tson | 1.57 | 69.0% | 3.8k | 5.6 |
| yaml | 1.17 | 90.0% | 6.6k | 3.2 |
| json_min | 0.89 | 61.0% | 5.9k | 3.6 |
| json_pretty | 0.66 | 66.0% | 8.6k | 2.5 |

### flat_250

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| csv | 1.45 | 63.0% | 9.3k | 5.7 |
| minemizer_compact | 1.42 | 62.0% | 9.3k | 5.7 |
| toon | 1.41 | 62.0% | 9.4k | 5.7 |
| tsv | 1.37 | 60.0% | 9.4k | 5.7 |
| minemizer_compact_no_repeat | 1.36 | 59.0% | 9.3k | 5.7 |
| minemizer | 1.33 | 60.0% | 9.7k | 5.5 |
| minemizer_no_repeat | 1.27 | 57.0% | 9.6k | 5.5 |
| minemizer_compact_repeat10 | 1.24 | 57.0% | 9.8k | 5.4 |
| minemizer_repeat10 | 1.23 | 58.0% | 10.1k | 5.3 |
| tson | 1.12 | 49.0% | 9.3k | 5.7 |
| yaml | 0.96 | 74.0% | 16.4k | 3.2 |
| json_min | 0.60 | 41.0% | 14.6k | 3.6 |
| json_pretty | 0.55 | 55.0% | 21.4k | 2.5 |

### nested_100

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| minemizer_compact | 1.84 | 76.0% | 3.6k | 6.5 |
| minemizer_compact_no_repeat | 1.84 | 76.0% | 3.6k | 6.5 |
| minemizer | 1.83 | 78.0% | 3.7k | 6.2 |
| minemizer_no_repeat | 1.83 | 78.0% | 3.7k | 6.2 |
| json_min | 1.27 | 80.0% | 5.5k | 4.2 |
| yaml | 1.14 | 82.0% | 6.2k | 3.7 |
| toon | 1.03 | 75.0% | 6.3k | 3.6 |
| tson | 0.82 | 33.0% | 3.5k | 6.6 |
| json_pretty | 0.69 | 69.0% | 8.7k | 2.7 |

### nested_50

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| minemizer_compact | 2.08 | 87.5% | 1.8k | 6.3 |
| minemizer_compact_no_repeat | 2.08 | 87.5% | 1.8k | 6.3 |
| minemizer | 1.94 | 84.0% | 1.9k | 6.1 |
| minemizer_no_repeat | 1.94 | 84.0% | 1.9k | 6.1 |
| yaml | 1.22 | 87.5% | 3.1k | 3.7 |
| toon | 1.13 | 82.5% | 3.2k | 3.6 |
| json_pretty | 0.91 | 90.5% | 4.4k | 2.6 |
| tson | 0.88 | 36.5% | 1.8k | 6.4 |
| json_min | 0.73 | 46.5% | 2.8k | 4.2 |

### sparse_250

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| minemizer_no_repeat | 1.26 | 61.0% | 16.5k | 5.6 |
| minemizer_repeat10 | 1.24 | 62.0% | 17.0k | 5.4 |
| minemizer_compact_repeat10 | 1.19 | 60.0% | 17.2k | 5.4 |
| minemizer | 1.15 | 56.0% | 16.6k | 5.6 |
| minemizer_compact_no_repeat | 1.15 | 56.0% | 16.6k | 5.6 |
| minemizer_compact | 1.11 | 54.0% | 16.6k | 5.6 |
| tson | 0.84 | 55.0% | 22.3k | 4.2 |
| yaml | 0.83 | 60.0% | 24.8k | 3.7 |
| json_min | 0.70 | 46.0% | 22.3k | 4.2 |
| toon | 0.69 | 49.0% | 24.3k | 3.8 |
| json_pretty | 0.42 | 42.0% | 34.1k | 2.7 |

### nested_1000

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| minemizer | 1.08 | 44.2% | 34.1k | 6.8 |
| minemizer_compact | 1.08 | 42.2% | 32.7k | 7.0 |
| minemizer_compact_no_repeat | 1.02 | 39.8% | 32.5k | 7.1 |
| minemizer_no_repeat | 0.99 | 40.0% | 33.9k | 6.8 |
| tson | 0.78 | 28.8% | 30.6k | 7.5 |
| yaml | 0.66 | 46.4% | 59.1k | 3.9 |
| json_min | 0.62 | 37.0% | 49.9k | 4.6 |
| toon | 0.59 | 42.6% | 60.2k | 3.8 |
| json_pretty | 0.41 | 41.2% | 83.5k | 2.8 |

### nested_500

| Format | Efficiency | Acc | Tokens | og_chars/tok |
|--------|------------|-----|--------|--------------|
| minemizer_no_repeat | 1.57 | 60.0% | 15.3k | 7.5 |
| minemizer_compact_no_repeat | 1.46 | 53.0% | 14.6k | 7.9 |
| minemizer | 1.30 | 50.0% | 15.4k | 7.5 |
| minemizer_compact | 1.23 | 45.0% | 14.6k | 7.9 |
| minemizer_compact_repeat10 | 1.12 | 43.0% | 15.4k | 7.5 |
| minemizer_repeat10 | 1.09 | 44.0% | 16.2k | 7.1 |
| json_min | 1.03 | 59.0% | 23.1k | 5.0 |
| yaml | 0.82 | 57.0% | 27.9k | 4.1 |
| tson | 0.73 | 25.0% | 13.8k | 8.3 |
| toon | 0.68 | 48.0% | 28.4k | 4.0 |
| json_pretty | 0.61 | 61.0% | 40.1k | 2.9 |

## Compression Benchmarks

### simple_flat

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 763 | 384 | 334 | 264 | 270 | 319 |
| json_min | 522 | 152 | 165 | 137 | 150 | 150 |
| csv | 234 | 95 | 101 | 77 | 91 | 93 |
| tsv | 234 | 95 | 101 | 77 | 92 | 93 |
| yaml | 489 | 163 | 180 | 169 | 172 | 173 |
| toon | 246 | 98 | 103 | 96 | 93 | 103 |
| tson | 229 | 90 | 95 | 80 | 86 | 88 |
| minemizer | 251 | 74 | 83 | 72 | 75 | 76 |
| minemizer_compact | 224 | 85 | 91 | 77 | 83 | 83 |

### nested_objects

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 1,039 | 590 | 435 | 348 | 349 | 415 |
| json_min | 618 | 188 | 211 | 174 | 187 | 191 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 629 | 264 | 246 | 229 | 228 | 240 |
| toon | 675 | 315 | 238 | 223 | 224 | 231 |
| tson | 306 | 136 | 141 | 110 | 124 | 122 |
| minemizer | 325 | 126 | 132 | 121 | 120 | 126 |
| minemizer_compact | 290 | 132 | 139 | 117 | 119 | 124 |

### lists_of_primitives

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 610 | 382 | 280 | 217 | 223 | 274 |
| json_min | 330 | 115 | 125 | 103 | 115 | 119 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 341 | 153 | 157 | 149 | 152 | 155 |
| toon | 339 | 161 | 141 | 137 | 142 | 142 |
| tson | 168 | 80 | 79 | 65 | 78 | 74 |
| minemizer | 188 | 81 | 79 | 71 | 68 | 77 |
| minemizer_compact | 165 | 83 | 83 | 70 | 71 | 82 |

### sparse_data

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 611 | 323 | 285 | 227 | 229 | 271 |
| json_min | 400 | 131 | 146 | 121 | 126 | 132 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 384 | 145 | 158 | 149 | 150 | 152 |
| toon | 438 | 190 | 167 | 159 | 160 | 161 |
| tson | 328 | 146 | 145 | 113 | 117 | 131 |
| minemizer | 200 | 72 | 79 | 72 | 73 | 73 |
| minemizer_compact | 180 | 82 | 88 | 74 | 76 | 78 |

### complex_mixed

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 1,320 | 768 | 560 | 455 | 428 | 542 |
| json_min | 760 | 224 | 284 | 246 | 239 | 260 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 818 | 374 | 338 | 306 | 279 | 335 |
| toon | 881 | 434 | 329 | 304 | 279 | 324 |
| tson | 453 | 207 | 237 | 203 | 194 | 210 |
| minemizer | 403 | 157 | 203 | 193 | 161 | 200 |
| minemizer_compact | 361 | 173 | 214 | 190 | 159 | 196 |

### books

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 27,902 | 12,188 | 11,626 | 9,434 | 8,955 | 11,284 |
| json_min | 22,501 | 7,103 | 8,035 | 6,637 | 6,166 | 7,694 |
| csv | 14,071 | 5,354 | 6,151 | 4,799 | 4,463 | 5,797 |
| tsv | 14,057 | 5,564 | 6,360 | 4,883 | 4,680 | 6,007 |
| yaml | 22,400 | 8,081 | 8,859 | 7,605 | 7,159 | 8,540 |
| toon | 14,277 | 5,388 | 6,172 | 4,866 | 4,435 | 5,838 |
| tson | 14,448 | 5,433 | 6,229 | 4,845 | 4,484 | 5,876 |
| minemizer | 14,458 | 5,152 | 6,042 | 4,976 | 4,520 | 5,803 |
| minemizer_compact | 13,753 | 5,260 | 6,056 | 4,847 | 4,387 | 5,703 |

### countries

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 1,133,948 | 677,260 | 565,880 | 474,014 | 402,626 | 546,242 |
| json_min | 787,962 | 339,487 | 425,660 | 365,037 | 304,093 | 404,150 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 641,939 | 345,580 | 251,610 | 219,269 | 206,631 | 214,187 |
| toon | 691,140 | 397,301 | 246,360 | 215,450 | 202,875 | 209,098 |
| tson | 423,383 | 210,056 | 196,499 | 158,349 | 158,554 | 159,054 |
| minemizer | 324,916 | 167,101 | 152,897 | 134,184 | 120,629 | 117,449 |
| minemizer_compact | 301,053 | 171,367 | 156,942 | 134,101 | 124,714 | 125,578 |

### large_non_uniform_nested_mixed

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 2,402 | 1,292 | 1,003 | 816 | 802 | 973 |
| json_min | 1,500 | 446 | 522 | 449 | 457 | 491 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 1,573 | 661 | 617 | 559 | 533 | 600 |
| toon | 1,766 | 841 | 625 | 572 | 545 | 608 |
| tson | 1,275 | 525 | 560 | 462 | 489 | 517 |
| minemizer | 1,203 | 383 | 452 | 400 | 389 | 435 |
| minemizer_compact | 1,072 | 409 | 462 | 382 | 385 | 432 |

### large_non_uniform_nested_numerical

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 2,947 | 1,718 | 1,542 | 1,332 | 1,170 | 1,528 |
| json_min | 1,873 | 755 | 976 | 884 | 749 | 961 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 2,085 | 1,033 | 1,171 | 1,077 | 894 | 1,145 |
| toon | 2,318 | 1,249 | 1,178 | 1,090 | 906 | 1,152 |
| tson | 1,642 | 823 | 993 | 907 | 747 | 969 |
| minemizer | 1,534 | 632 | 940 | 883 | 699 | 918 |
| minemizer_compact | 1,361 | 676 | 875 | 809 | 642 | 861 |

### large_non_uniform_nested_text

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 4,214 | 1,498 | 1,268 | 997 | 986 | 1,154 |
| json_min | 3,359 | 658 | 792 | 634 | 647 | 678 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 3,387 | 818 | 843 | 716 | 703 | 742 |
| toon | 3,534 | 974 | 846 | 718 | 705 | 747 |
| tson | 3,173 | 721 | 831 | 644 | 689 | 713 |
| minemizer | 2,809 | 522 | 619 | 510 | 500 | 527 |
| minemizer_compact | 2,694 | 565 | 672 | 534 | 527 | 566 |

### mcp_tools_list

| Format | Chars | gpt2 | llama | qwen2.5 | deepseek | devstral |
|--------|-------|------|------|------|------|------|
| json_pretty | 51,663 | 27,574 | 13,539 | 11,210 | 11,303 | 13,393 |
| json_min | 30,724 | 6,840 | 7,315 | 6,368 | 6,977 | 7,070 |
| csv | N/A | N/A | N/A | N/A | N/A | N/A |
| tsv | N/A | N/A | N/A | N/A | N/A | N/A |
| yaml | 38,139 | 16,770 | 8,915 | 7,927 | 7,997 | 8,731 |
| toon | 38,376 | 17,296 | 8,649 | 7,670 | 7,767 | 8,483 |
| tson | 25,878 | 7,318 | 7,045 | 5,889 | 6,731 | 6,903 |
| minemizer | 23,383 | 5,559 | 5,767 | 5,319 | 5,342 | 5,590 |
| minemizer_compact | 21,912 | 5,672 | 5,726 | 5,112 | 5,216 | 5,583 |

## LLM Accuracy Benchmarks

### Devstral-Small-24B-Q6_K on flat_100

*100 queries, 2025-12-13*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| yaml | 90.0% | 6.6k | 665ms |
| csv | 82.0% | 3.8k | 657ms |
| tsv | 81.0% | 3.8k | 647ms |
| toon | 80.0% | 3.8k | 660ms |
| minemizer_compact | 79.0% | 3.8k | 632ms |
| minemizer_compact_no_repeat | 79.0% | 3.8k | 619ms |
| minemizer | 73.0% | 3.9k | 622ms |
| minemizer_no_repeat | 73.0% | 3.9k | 630ms |
| tson | 69.0% | 3.8k | 658ms |
| json_pretty | 66.0% | 8.6k | 627ms |
| json_min | 61.0% | 5.9k | 838ms |

### Devstral-Small-24B-Q6_K on flat_250

*100 queries, 2025-12-13*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| yaml | 74.0% | 16.4k | 948ms |
| csv | 63.0% | 9.3k | 916ms |
| toon | 62.0% | 9.4k | 915ms |
| minemizer_compact | 62.0% | 9.3k | 846ms |
| tsv | 60.0% | 9.4k | 912ms |
| minemizer | 60.0% | 9.7k | 841ms |
| minemizer_compact_no_repeat | 59.0% | 9.3k | 855ms |
| minemizer_repeat10 | 58.0% | 10.1k | 851ms |
| minemizer_no_repeat | 57.0% | 9.6k | 855ms |
| minemizer_compact_repeat10 | 57.0% | 9.8k | 848ms |
| json_pretty | 55.0% | 21.4k | 758ms |
| tson | 49.0% | 9.3k | 915ms |
| json_min | 41.0% | 14.6k | 1075ms |

### Devstral-Small-24B-Q6_K on nested_100

*100 queries, 2025-12-12*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| yaml | 82.0% | 6.2k | 861ms |
| json_min | 80.0% | 5.5k | 837ms |
| minemizer | 78.0% | 3.7k | 716ms |
| minemizer_no_repeat | 78.0% | 3.7k | 704ms |
| minemizer_compact | 76.0% | 3.6k | 755ms |
| minemizer_compact_no_repeat | 76.0% | 3.6k | 754ms |
| toon | 75.0% | 6.3k | 804ms |
| json_pretty | 69.0% | 8.7k | 878ms |
| tson | 33.0% | 3.5k | 753ms |

### Devstral-Small-24B-Q6_K on nested_50

*200 queries, 2025-12-12*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| json_pretty | 90.5% | 4.4k | 754ms |
| yaml | 87.5% | 3.1k | 648ms |
| minemizer_compact | 87.5% | 1.8k | 612ms |
| minemizer_compact_no_repeat | 87.5% | 1.8k | 612ms |
| minemizer | 84.0% | 1.9k | 591ms |
| minemizer_no_repeat | 84.0% | 1.9k | 596ms |
| toon | 82.5% | 3.2k | 788ms |
| json_min | 46.5% | 2.8k | 799ms |
| tson | 36.5% | 1.8k | 663ms |

### Devstral-Small-24B-Q6_K on sparse_250

*100 queries, 2025-12-13*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| minemizer_repeat10 | 62.0% | 17.0k | 965ms |
| minemizer_no_repeat | 61.0% | 16.5k | 905ms |
| yaml | 60.0% | 24.8k | 1075ms |
| minemizer_compact_repeat10 | 60.0% | 17.2k | 954ms |
| minemizer | 56.0% | 16.6k | 919ms |
| minemizer_compact_no_repeat | 56.0% | 16.6k | 934ms |
| tson | 55.0% | 22.3k | 1009ms |
| minemizer_compact | 54.0% | 16.6k | 905ms |
| toon | 49.0% | 24.3k | 1048ms |
| json_min | 46.0% | 22.3k | 1131ms |
| json_pretty | 42.0% | 34.1k | 1140ms |

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

### gpt-oss-20b-Q8_0 on nested_1000

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

### gpt-oss-20b on nested_500

*100 queries, 2025-12-13*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| json_pretty | 61.0% | 40.1k | 983ms |
| minemizer_no_repeat | 60.0% | 15.3k | 1198ms |
| json_min | 59.0% | 23.1k | 1065ms |
| yaml | 57.0% | 27.9k | 1271ms |
| minemizer_compact_no_repeat | 53.0% | 14.6k | 1205ms |
| minemizer | 50.0% | 15.4k | 1246ms |
| toon | 48.0% | 28.4k | 1233ms |
| minemizer_compact | 45.0% | 14.6k | 1323ms |
| minemizer_repeat10 | 44.0% | 16.2k | 1304ms |
| minemizer_compact_repeat10 | 43.0% | 15.4k | 1300ms |
| tson | 25.0% | 13.8k | 1315ms |

### Devstral-Small-24B-Q6_K on nested_1000

*50 queries, 2025-12-12*

| Format | Accuracy | Tokens | Latency |
|--------|----------|--------|---------|
| json_pretty | 36.0% | 86.0k | 5778ms |
| yaml | 36.0% | 61.6k | 12152ms |
| minemizer_no_repeat | 36.0% | 36.3k | 5552ms |
| minemizer_compact_no_repeat | 36.0% | 35.1k | 5630ms |
| toon | 34.0% | 62.6k | 11410ms |
| minemizer_compact | 34.0% | 35.2k | 5626ms |
| minemizer | 30.0% | 36.4k | 5776ms |
| json_min | 28.0% | 54.0k | 8619ms |
| tson | 24.0% | 34.3k | 5230ms |
