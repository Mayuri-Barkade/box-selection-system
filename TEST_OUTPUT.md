# Test Output

(venv) PS C:\Users\Admin\Desktop\Mayuri_Barkade_Test-Solution\box-selection-system> python manage.py test -v 2
Found 25 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: boxes, messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions
Synchronizing apps without migrations:
  Creating tables...
    Creating table boxes_product
    Creating table boxes_box
    Creating table boxes_order
    Creating table boxes_orderitem
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_bad_json_400 (boxes.tests.test_api.RecommendApiTests.test_bad_json_400) ... ok
test_empty_order_400 (boxes.tests.test_api.RecommendApiTests.test_empty_order_400) ... ok
test_get_not_allowed_on_adhoc (boxes.tests.test_api.RecommendApiTests.test_get_not_allowed_on_adhoc) ... ok
test_heavy_order_gets_medium (boxes.tests.test_api.RecommendApiTests.test_heavy_order_gets_medium) ... ok
test_nothing_fits_returns_422 (boxes.tests.test_api.RecommendApiTests.test_nothing_fits_returns_422) ... ok
test_order_endpoint_recommends_cheapest_box (boxes.tests.test_api.RecommendApiTests.test_order_endpoint_recommends_cheapest_box) ... ok
test_unknown_order_404 (boxes.tests.test_api.RecommendApiTests.test_unknown_order_404) ... ok
test_unknown_product_404 (boxes.tests.test_api.RecommendApiTests.test_unknown_product_404) ... ok
test_cheaper_bigger_box_wins_over_pricier_smaller_box (boxes.tests.test_services.RecommendBoxTests.test_cheaper_bigger_box_wins_over_pricier_smaller_box) ... ok
test_empty_order_raises (boxes.tests.test_services.RecommendBoxTests.test_empty_order_raises) ... ok
test_exact_fit_is_accepted (boxes.tests.test_services.RecommendBoxTests.test_exact_fit_is_accepted) ... ok
test_input_boxes_not_mutated_and_result_deterministic (boxes.tests.test_services.RecommendBoxTests.test_input_boxes_not_mutated_and_result_deterministic) ... ok
test_multiple_items_pack_together (boxes.tests.test_services.RecommendBoxTests.test_multiple_items_pack_together) ... ok
test_negative_weight_raises (boxes.tests.test_services.RecommendBoxTests.test_negative_weight_raises) ... ok
test_no_boxes_defined (boxes.tests.test_services.RecommendBoxTests.test_no_boxes_defined) ... ok
test_non_positive_dimension_raises (boxes.tests.test_services.RecommendBoxTests.test_non_positive_dimension_raises) ... ok
test_quantity_adds_weight_and_volume (boxes.tests.test_services.RecommendBoxTests.test_quantity_adds_weight_and_volume) ... ok
test_rotation_is_allowed (boxes.tests.test_services.RecommendBoxTests.test_rotation_is_allowed) ... ok.. ok
test_tie_on_cost_prefers_smaller_volume (boxes.tests.test_services.RecommendBoxTests.test_tie_on_cost_prefers_smaller_volume) ... ok
test_too_heavy_for_every_box (boxes.tests.test_services.RecommendBoxTests.test_too_heavy_for_every_box) ... ok
test_volume_ok_but_shape_wrong (boxes.tests.test_services.RecommendBoxTests.test_volume_ok_but_shape_wrong) ... ok
test_weight_forces_bigger_box (boxes.tests.test_services.RecommendBoxTests.test_weight_forces_bigger_box) ... ok
test_zero_quantity_raises (boxes.tests.test_services.RecommendBoxTests.test_zero_quantity_raises) ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.170s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

```
