{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'payments') }}
),

staged as (
    select
        cast(payment_id as varchar)             as payment_id,
        cast(order_id as varchar)               as order_id,
        cast(customer_id as varchar)            as customer_id,
        cast(payment_method_id as varchar)      as payment_method_id,
        cast(amount_paid as numeric)            as amount_paid,
        cast(payment_date as timestamp)         as payment_date,
        cast(created_at as timestamp)           as created_at,
        cast(updated_at as timestamp)           as updated_at
    from source
)

select * from staged