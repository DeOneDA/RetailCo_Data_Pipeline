{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'products') }}
),

staged as (
    select
        cast(id as varchar) as product_id,
        cast(name as varchar) as product_name,
        cast(sku as varchar) as sku,
        cast(category as varchar) as category,
        cast(sub_category as varchar) as sub_category,
        cast(brand as varchar) as brand,
        cast(supplier as varchar) as supplier,
        cast(cost_price as numeric) as cost_price,
        cast(selling_price as numeric) as selling_price,
        cast(is_deleted as boolean) as is_deleted,
        cast(updated_at as timestamp) as updated_at
    from source
)

select * from staged