import unittest

from boxes.services import (BoxSpec, InvalidOrderError, ItemSpec, can_pack,
                            recommend_box)


def box(name, l, w, h, max_weight, cost, id=None):
    return BoxSpec(id, name, l, w, h, max_weight, cost)


SMALL = box("Small", 20, 15, 10, 5, 1.0)
MEDIUM = box("Medium", 40, 30, 20, 15, 2.5)
LARGE = box("Large", 60, 40, 40, 30, 4.0)
ALL = [LARGE, SMALL, MEDIUM]  # deliberately unsorted


class RecommendBoxTests(unittest.TestCase):
    def test_single_small_item_picks_cheapest_fitting(self):
        r = recommend_box([ItemSpec("pen", 15, 2, 2, 0.1)], ALL)
        self.assertEqual(r.box.name, "Small")

    def test_weight_forces_bigger_box(self):
        # fits Small by size, but 8kg > Small's 5kg limit
        r = recommend_box([ItemSpec("dumbbell", 15, 10, 8, 8)], ALL)
        self.assertEqual(r.box.name, "Medium")
        self.assertIn(("Small", "over weight limit"), r.rejected)

    def test_quantity_adds_weight_and_volume(self):
        r = recommend_box([ItemSpec("book", 20, 14, 3, 1.0, quantity=4)], ALL)
        # 4kg fits Small by weight, but 4 books (stacked 12cm high) do not fit 10cm
        self.assertEqual(r.box.name, "Medium")
        self.assertEqual(r.total_weight, 4.0)

    def test_rotation_is_allowed(self):
        # 18 x 9 x 14 only fits Small (20x15x10) when rotated
        self.assertTrue(can_pack([(18, 9, 14)], (20, 15, 10)))

    def test_item_too_long_for_every_box(self):
        r = recommend_box([ItemSpec("pole", 100, 5, 5, 1)], ALL)
        self.assertIsNone(r.box)
        self.assertEqual(len(r.rejected), 3)

    def test_too_heavy_for_every_box(self):
        r = recommend_box([ItemSpec("anvil", 10, 10, 10, 50)], ALL)
        self.assertIsNone(r.box)

    def test_exact_fit_is_accepted(self):
        r = recommend_box([ItemSpec("tight", 20, 15, 10, 5)], ALL)
        self.assertEqual(r.box.name, "Small")

    def test_volume_ok_but_shape_wrong(self):
        # volume 3000 equals Small's volume, but a long thin item can't fit
        self.assertFalse(can_pack([(30, 10, 10)], (20, 15, 10)))

    def test_multiple_items_pack_together(self):
        items = [ItemSpec("a", 10, 15, 10, 1), ItemSpec("b", 10, 15, 10, 1)]
        r = recommend_box(items, [SMALL])
        self.assertEqual(r.box.name, "Small")

    def test_tie_on_cost_prefers_smaller_volume(self):
        a = box("A", 30, 30, 30, 10, 2.0)
        b = box("B", 25, 25, 25, 10, 2.0)
        r = recommend_box([ItemSpec("x", 5, 5, 5, 1)], [a, b])
        self.assertEqual(r.box.name, "B")

    def test_cheaper_bigger_box_wins_over_pricier_smaller_box(self):
        pricey_small = box("PS", 20, 20, 20, 10, 9.0)
        cheap_big = box("CB", 40, 40, 40, 10, 3.0)
        r = recommend_box([ItemSpec("x", 5, 5, 5, 1)], [pricey_small, cheap_big])
        self.assertEqual(r.box.name, "CB")

    def test_no_boxes_defined(self):
        r = recommend_box([ItemSpec("x", 1, 1, 1, 1)], [])
        self.assertIsNone(r.box)

    def test_empty_order_raises(self):
        with self.assertRaises(InvalidOrderError):
            recommend_box([], ALL)

    def test_zero_quantity_raises(self):
        with self.assertRaises(InvalidOrderError):
            recommend_box([ItemSpec("x", 1, 1, 1, 1, quantity=0)], ALL)

    def test_non_positive_dimension_raises(self):
        with self.assertRaises(InvalidOrderError):
            recommend_box([ItemSpec("x", 0, 1, 1, 1)], ALL)

    def test_negative_weight_raises(self):
        with self.assertRaises(InvalidOrderError):
            recommend_box([ItemSpec("x", 1, 1, 1, -1)], ALL)

    def test_input_boxes_not_mutated_and_result_deterministic(self):
        boxes = list(ALL)
        r1 = recommend_box([ItemSpec("x", 5, 5, 5, 1)], boxes)
        r2 = recommend_box([ItemSpec("x", 5, 5, 5, 1)], list(reversed(boxes)))
        self.assertEqual(boxes, ALL)
        self.assertEqual(r1.box, r2.box)


if __name__ == "__main__":
    unittest.main()
