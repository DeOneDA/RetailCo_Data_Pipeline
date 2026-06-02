{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'orders') }}
),

staged as (
    select
        cast(id as varchar) as order_id,
        cast(customer_id as varchar) as customer_id,
        cast(store_id as varchar) as store_id,
        cast(employee_id as varchar) as employee_id,
        cast(status as varchar) as status,
        cast(ordered_at as timestamp) as ordered_at,
        cast(ordered_at as timestamp) as pending_at,
        cast(paid_at as timestamp) as paid_at,
        cast(shipped_at as timestamp) as shipped_at,
        cast(delivered_at as timestamp) as delivered_at,
        cast(cancelled_at as timestamp) as cancelled_at,
        cast(created_at as timestamp) as created_at,
        cast(updated_at as timestamp) as updated_at
    from source
)

select * from staged