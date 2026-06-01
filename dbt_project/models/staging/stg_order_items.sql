{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'order_items') }}
),

staged as (
    select
        cast(order_item_id as varchar)      as order_item_id,
        cast(order_id as varchar)           as order_id,
        cast(product_id as varchar)         as product_id,
        cast(quantity as integer)           as quantity,
        cast(unit_price as numeric)         as unit_price,
        cast(discount_amount as numeric)    as discount_amount,
        cast(line_total as numeric)         as line_total,
        cast(updated_at as timestamp)       as updated_at
    from source
)

select * from staged