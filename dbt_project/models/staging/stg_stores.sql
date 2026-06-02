{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'stores') }}
),

staged as (
    select
        cast(id as varchar) as store_id,
        cast(name as varchar) as store_name,
        cast(address as varchar) as address,
        cast(city as varchar) as city,
        cast(state as varchar) as state,
        cast(phone as varchar) as phone,
        cast(manager_name as varchar) as manager_name,
        cast(opened_date as date) as opened_date,
        cast(updated_at as timestamp) as updated_at
    from source
)

select * from staged