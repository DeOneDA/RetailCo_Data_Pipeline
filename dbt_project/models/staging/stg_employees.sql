{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'employees') }}
),

staged as (
    select
        cast(employee_id as varchar)        as employee_id,
        cast(employee_name as varchar)      as employee_name,
        cast(role as varchar)               as role,
        cast(store_id as varchar)           as store_id,
        cast(is_deleted as boolean)         as is_deleted,
        cast(updated_at as timestamp)       as updated_at
    from source
)

select * from staged