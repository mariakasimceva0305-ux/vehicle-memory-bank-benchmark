# Vehicle Memory Bank Benchmark

[Русская версия](#ru) | [English version](#en)

## RU

### TL;DR
Гибридный retrieval-benchmark для поиска похожих автомобилей в memory bank: text + metadata + visual features, офлайн-оценка и FastAPI serving.

### Гипотезы
1. Hybrid scoring устойчивее чисто текстового baseline.
2. Метаданные улучшают top-1 точность.
3. Лёгкие визуальные признаки дают прирост без тяжёлой модели.

### Метрики
`Recall@1`, `Recall@3`, `MRR`, `top1_brand_match`, `top1_color_match`, `latency_ms_p50/p95`.

### Запуск
```bash
python -m venv .venv
pip install -r requirements.txt
python scripts/run_benchmark.py --config configs/demo_hybrid.yaml
python scripts/serve_api.py
```

## EN

### Overview
A hybrid retrieval benchmark for vehicle memory-bank search using text, metadata, and lightweight visual features with offline evaluation and API serving.
