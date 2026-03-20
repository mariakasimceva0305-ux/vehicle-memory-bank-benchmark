# Vehicle Memory Bank Benchmark

Система для поиска похожих автомобилей в memory bank для задач симуляции и scene editing: локальный каталог ассетов, retrieval по текстовым и структурированным признакам, гибридное ранжирование, офлайн-оценка и FastAPI API.

## Краткий обзор

Основной фокус:
- поиск похожих автомобилей по brand / model / body type / color / view description,
- сравнение retrieval-гипотез на компактном воспроизводимом benchmark,
- локальный demo-каталог ассетов без обязательных внешних скачиваний.

В репозитории есть:
- встроенный demo-каталог автомобилей с несколькими view per car,
- baseline text+metadata конфигурация,
- hybrid конфигурация с image features,
- офлайн-оценка Recall@k / MRR / agreement-метрик,
- API для поиска кандидатов в memory bank.

## Что делает проект

Система:

- загружает каталог автомобильных ассетов из CSV,
- индексирует текстовые описания views,
- извлекает простые image features из demo-изображений,
- объединяет text similarity, metadata match и color similarity,
- ранжирует кандидатов и возвращает top-k похожих автомобилей,
- считает офлайн-метрики по задаче multi-view retrieval.

## Где проект полезен

Такой pipeline нужен как компактный retrieval-слой для:
- memory bank поиска похожих автомобилей,
- asset retrieval в задачах scene editing,
- каталогизации и дедупликации vehicle assets,
- экспериментов перед переходом к более тяжёлым multimodal или simulation pipelines.

## Pipeline (шаг за шагом)

1. **Catalog loading**  
   Загрузка локального каталога `data/demo_catalog/vehicles.csv`.

2. **Text indexing**  
   Построение char-ngram TF-IDF представления по captions вида  
   `blue Toyota Camry sedan, front-left walkaround view in daylight`.

3. **Metadata scoring**  
   Дополнительные бонусы за совпадение `brand`, `model`, `body_type`, `color_name` и близость RGB.

4. **Image feature extraction**  
   Для demo-изображений извлекается компактный histogram-based visual descriptor.

5. **Hybrid scoring**  
   Итоговый score объединяет:
   - text similarity,
   - image similarity,
   - structured metadata priors.

6. **Evaluation**  
   Для каждого query asset задача — вернуть другой view того же `car_id` как можно выше в выдаче.

## Конфигурации

### Text + metadata (`configs/demo_text.yaml`)

- без image features,
- быстрый baseline,
- подходит для smoke run и CI.

### Hybrid (`configs/demo_hybrid.yaml`)

- text similarity,
- metadata priors,
- image features,
- более сильный локальный baseline для demo-каталога.

## Demo-каталог

В репозитории уже включён компактный каталог:

- путь: `data/demo_catalog/`
- объём: 12 автомобилей × 3 views = 36 ассетов
- поля:
  - `asset_id`
  - `car_id`
  - `view_id`
  - `brand`
  - `model`
  - `body_type`
  - `color_name`
  - `r,g,b`
  - `caption`
  - `image_path`

Demo-изображения созданы локально и нужны только для воспроизводимого benchmark-режима. Код проекта допускает расширение до внешнего каталога и адаптеров к публичным датасетам.

## Структура репозитория

```text
configs/                # конфигурации retrieval и evaluation
data/demo_catalog/      # локальный каталог ассетов и demo-изображения
docs/                   # заметки по архитектуре и идее проекта
eval/results/           # результаты benchmark-запусков
examples/               # примеры запросов
scripts/                # CLI-скрипты
src/vehicle_bank/       # код retrieval, evaluation и API
tests/                  # smoke-тесты
```

## Как запустить

### 1) Установка

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 2) Benchmark

```bash
python scripts/run_benchmark.py --config configs/demo_hybrid.yaml
```

Результаты сохраняются в:
- `eval/results/hybrid_demo/latest_summary.json`
- `eval/results/hybrid_demo/latest_rows.jsonl`

### 3) Поиск через CLI

```bash
python scripts/query_demo.py \
  --config configs/demo_hybrid.yaml \
  --text "black bmw x5 suv" \
  --brand BMW \
  --model X5 \
  --body-type suv \
  --color-name black \
  --rgb 35,35,35
```

### 4) API

```bash
python scripts/serve_api.py
```

Эндпоинты:
- `GET /health`
- `POST /search`

Пример запроса:

```json
{
  "query_text": "blue toyota camry sedan",
  "brand": "Toyota",
  "model": "Camry",
  "body_type": "sedan",
  "color_name": "blue",
  "rgb": "36,103,214",
  "top_k": 5
}
```

## Метрики

Текущая офлайн-оценка считает:

- `Recall@1`
- `Recall@3`
- `MRR`
- `top1_brand_match`
- `top1_color_match`
- `latency_ms_p50`
- `latency_ms_p95`

## Ограничения текущей версии

- Demo-каталог небольшой и предназначен для локально воспроизводимого benchmark.
- Визуальные признаки реализованы как лёгкий descriptor, а не тяжёлая deep visual encoder.
- Retrieval работает по статическим ассетам и не включает 3D reconstruction, relighting или scene insertion.
- Для подключения внешних memory bank источников требуется отдельный adapter layer.

## Дальнейшее развитие

Следующие разумные шаги:
- подключить реальный публичный каталог multi-view car assets,
- заменить text encoder на sentence-transformers / CLIP text branch,
- добавить обучение pairwise reranker,
- поддержать image-to-catalog search,
- добавить grouping и aggregation по `car_id`,
- расширить evaluation до brand/model/color consistency@k и hard-negative splits.

## Идея проекта

Проект вдохновлён задачей retrieval-а похожих автомобилей из внешнего memory bank для дальнейшей работы с driving scenes, но реализован как компактный прикладной benchmark с локальным reproducible demo-режимом.
