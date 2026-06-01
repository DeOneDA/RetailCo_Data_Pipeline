{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'customers') }}
),

staged as (
    select
        cast(customer_id as varchar)        as customer_id,
        cast(first_name as varchar)         as first_name,
        cast(last_name as varchar)          as last_name,
        cast(address as varchar)            as address,
        cast(email as varchar)              as email,
        cast(phone as varchar)              as phone,
        cast(city as varchar)               as city,
        cast(state as varchar)              as state,
        cast(segment as varchar)            as segment,
        cast(tier as varchar)               as tier,
        cast(registered_at as timestamp)    as registered_at,
        cast(is_deleted as boolean)         as is_deleted,
        cast(updated_at as timestamp)       as updated_at
    from source
)

select * from staged