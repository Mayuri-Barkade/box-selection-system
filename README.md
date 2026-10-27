# AI-Assisted Box Selection System (Django)

Recommends the most suitable shipping box for an order, based on product
dimensions/weight and each box's internal dimensions, max weight and cost.

Units: dimensions in **cm**, weight in **kg**.

## How it works

The logic lives in `boxes/services.py` (plain Python, no Django imports, so it
is easy to test). For each box it checks:

1. **Weight** - total order weight <= box max weight.
2. **Volume** - total item volume <= box volume (cheap early rejection).
3. **Packing** - items must physically fit. A guillotine packer tries all 6
   rotations of each item (largest first) with bounded backtracking.

Of the boxes that pass, the **cheapest** wins. Ties go to the smaller volume,
then lower max weight, then name, so the answer is deterministic.

### Design decisions / limitations

- The packer is a heuristic. If it says "fits", the items really fit (no
  overlaps). If it says "doesn't fit", a perfect packer *might* still find a
  way. I chose this direction because shipping a too-small box is worse than
  picking a slightly larger one.
- Search is capped (`MAX_SEARCH_NODES`) so huge orders can't hang the request;
  hitting the cap counts as "doesn't fit".
- Items are treated as rigid rectangular blocks. No fragility, "this side up",
  or stacking-weight rules.
- Box *internal* dimensions are assumed to be the usable space.
- The ad-hoc POST endpoint is CSRF-exempt and unauthenticated. Add auth before
  real use.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # to use /admin/ for products, boxes, orders
python manage.py runserver
```

Add Products, Boxes and Orders (with items) in `/admin/`.

## API

`GET /api/orders/<order_id>/recommend-box/`

`POST /api/recommend-box/`
```json
{"items": [{"product_id": 1, "quantity": 2}]}
```

Example success (200):
```json
{
  "recommended_box": {"id": 1, "name": "Small", "cost": 1.0},
  "total_weight": 0.8,
  "total_volume": 2400.0,
  "reason": "Cheapest box that fits the weight and dimensions.",
  "rejected_boxes": []
}
```

| Status | Meaning |
|--------|---------|
| 200 | A box was found |
| 400 | Bad input (empty order, bad JSON, invalid quantity/size) |
| 404 | Order or product not found |
| 422 | Valid order, but no box can hold it (`recommended_box` is null, `rejected_boxes` says why) |

## Tests

```bash
python manage.py test -v 2
```

- `boxes/tests/test_services.py` - selection logic (weight limits, rotation,
  exact fit, ties, quantities, invalid input, determinism).
- `boxes/tests/test_api.py` - endpoints and status codes.

CI: `.github/workflows/tests.yml` runs the suite on every push.
Test output: see `TEST_OUTPUT.md`.
