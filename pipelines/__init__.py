from dagster import Definitions, load_assets_from_package_module

import pipelines.example as test1

print(load_assets_from_package_module(test1, group_name="example_raw"))

defs = Definitions(
    assets=load_assets_from_package_module(test1)
)
