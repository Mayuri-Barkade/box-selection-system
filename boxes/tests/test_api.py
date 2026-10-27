import json

from django.test import TestCase

from boxes.models import Box, Order, OrderItem, Product


class RecommendApiTests(TestCase):
    def setUp(self):
        Box.objects.create(name="Small", length=20, width=15, height=10,
                           max_weight=5, cost="1.00")
        Box.objects.create(name="Medium", length=40, width=30, height=20,
                           max_weight=15, cost="2.50")
        self.mug = Product.objects.create(name="Mug", sku="MUG", length=10,
                                          width=10, height=12, weight=0.4)
        self.weights = Product.objects.create(name="Weights", sku="WGT",
                                              length=15, width=10, height=8,
                                              weight=8)

    def post(self, payload):
        return self.client.post("/api/recommend-box/", json.dumps(payload),
                                content_type="application/json")

    def test_order_endpoint_recommends_cheapest_box(self):
        order = Order.objects.create(reference="A1")
        OrderItem.objects.create(order=order, product=self.mug, quantity=1)
        r = self.client.get(f"/api/orders/{order.id}/recommend-box/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["recommended_box"]["name"], "Small")

    def test_heavy_order_gets_medium(self):
        r = self.post({"items": [{"product_id": self.weights.id, "quantity": 1}]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["recommended_box"]["name"], "Medium")

    def test_nothing_fits_returns_422(self):
        r = self.post({"items": [{"product_id": self.weights.id, "quantity": 5}]})
        self.assertEqual(r.status_code, 422)
        self.assertIsNone(r.json()["recommended_box"])

    def test_unknown_order_404(self):
        self.assertEqual(self.client.get("/api/orders/999/recommend-box/").status_code, 404)

    def test_empty_order_400(self):
        order = Order.objects.create(reference="EMPTY")
        r = self.client.get(f"/api/orders/{order.id}/recommend-box/")
        self.assertEqual(r.status_code, 400)

    def test_bad_json_400(self):
        r = self.client.post("/api/recommend-box/", "not json",
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_unknown_product_404(self):
        r = self.post({"items": [{"product_id": 12345, "quantity": 1}]})
        self.assertEqual(r.status_code, 404)

    def test_get_not_allowed_on_adhoc(self):
        self.assertEqual(self.client.get("/api/recommend-box/").status_code, 405)
