{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'payment_methods') }}
),

staged as (
    select
        cast(id as varchar) as payment_method_id,
        cast(name as varchar) as method_name,
        cast(provider as varchar) as provider,
        cast(is_digital as boolean) as is_digital,
        cast(updated_at as timestamp) as updated_at
    from source
)

select * from staged