# Примеры запросов

- blue toyota camry sedan daylight side view
- black bmw x5 suv
- orange renault duster crossover
- white volkswagen tiguan overcast
- red honda civic sedan evening

Пример CLI:

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
