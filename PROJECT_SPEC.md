# PROJECT SPEC

## Название
Vehicle Memory Bank Benchmark

## Короткое описание
Компактный benchmark для поиска похожих автомобильных ассетов в memory bank с гибридным ранжированием по тексту, структуре и визуальным признакам.

## Цель
Собрать воспроизводимый applied-ML проект, который показывает:
- retrieval design,
- hypothesis-driven evaluation,
- работу со structured + visual features,
- API serving,
- аккуратную инженерную упаковку.

## Основные сущности
- `asset_id` — конкретный ассет / view
- `car_id` — идентичность автомобиля
- `caption` — текстовое описание view
- `brand`, `model`, `body_type`, `color_name` — structured metadata
- `image_path` — локальное demo-изображение

## Retrieval hypotheses
1. Text + metadata baseline
2. Hybrid = text + metadata + image features

## Benchmark task
Для каждого query asset нужно вернуть другой view того же `car_id` как можно выше.

## Offline metrics
- Recall@1
- Recall@3
- MRR
- top1 brand agreement
- top1 color agreement
- latency p50/p95

## Non-goals
- полноценная 3D реконструкция,
- relighting,
- photorealistic scene insertion,
- full paper reproduction.

## Почему проект сильный
- не повторяет существующий RAG/FAQ retrieval один в один,
- добавляет transportation / CV / asset retrieval тематику,
- хорошо сочетается с NLP + retrieval профилем,
- показывает умение строить benchmark вокруг инженерной гипотезы.
