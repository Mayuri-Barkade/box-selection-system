import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Box, Order, Product
from .services import BoxSpec, InvalidOrderError, ItemSpec, recommend_box


def _box_specs():
    return [
        BoxSpec(b.id, b.name, b.length, b.width, b.height, b.max_weight,
                float(b.cost))
        for b in Box.objects.all()
    ]


def _item_spec(product, quantity):
    return ItemSpec(product.name, product.length, product.width,
                    product.height, product.weight, quantity)


def _respond(items):
    try:
        rec = recommend_box(items, _box_specs())
    except InvalidOrderError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    body = {
        "total_weight": rec.total_weight,
        "total_volume": rec.total_volume,
        "reason": rec.reason,
        "rejected_boxes": [{"box": n, "why": w} for n, w in rec.rejected],
    }
    if rec.box is None:
        body["recommended_box"] = None
        return JsonResponse(body, status=422)
    body["recommended_box"] = {
        "id": rec.box.id,
        "name": rec.box.name,
        "cost": rec.box.cost,
    }
    return JsonResponse(body)


@require_GET
def recommend_for_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)
    items = [_item_spec(i.product, i.quantity)
             for i in order.items.select_related("product")]
    return _respond(items)


@csrf_exempt  # JSON API without sessions; add auth before real use
@require_POST
def recommend_adhoc(request):
    """Body: {"items": [{"product_id": 1, "quantity": 2}, ...]}"""
    try:
        data = json.loads(request.body or b"{}")
        raw_items = data["items"]
        if not isinstance(raw_items, list):
            raise TypeError
    except (ValueError, KeyError, TypeError):
        return JsonResponse(
            {"error": 'Send JSON like {"items": [{"product_id": 1, "quantity": 2}]}'},
            status=400)

    items = []
    for row in raw_items:
        try:
            product = Product.objects.get(pk=row["product_id"])
            quantity = int(row.get("quantity", 1))
        except (KeyError, TypeError, ValueError, AttributeError):
            return JsonResponse({"error": "Each item needs product_id and an integer quantity."},
                                status=400)
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Product {row['product_id']} not found."},
                                status=404)
        items.append(_item_spec(product, quantity))
    return _respond(items)
