# Архитектура

## 1. Источник данных
Локальный CSV-каталог demo-ассетов с несколькими views на один `car_id`.

## 2. Индексация
- text index: char-ngram TF-IDF по `caption`
- image index: histogram-based descriptor по demo-изображениям

## 3. Scoring
Итоговый score = 
- `w_text * text_similarity`
- `+ metadata bonuses`
- `+ w_image * image_similarity`

## 4. Retrieval
Top-k кандидаты сортируются по суммарному score.

## 5. Evaluation
Для каждого query asset релевантны все записи с тем же `car_id`, кроме самого query asset.

## 6. Serving
FastAPI endpoint `/search` принимает query text + structured fields и возвращает top-k кандидатов.

## 7. Расширение
Отдельный adapter layer позволяет подключить внешний публичный memory bank датасет, не меняя retrieval/evaluation логику.
