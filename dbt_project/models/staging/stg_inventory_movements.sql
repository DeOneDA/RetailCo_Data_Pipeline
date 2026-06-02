{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'inventory_movements') }}
),

staged as (
    select
        cast(id as varchar) as movement_id,
        cast(product_id as varchar) as product_id,
        cast(store_id as varchar) as store_id,
        cast(movement_type as varchar) as movement_type,
        cast(quantity as integer) as quantity,
        cast(moved_at as timestamp) as movement_date,
        cast(created_at as timestamp) as created_at,
        cast(updated_at as timestamp) as updated_at
    from source
)

select * from staged