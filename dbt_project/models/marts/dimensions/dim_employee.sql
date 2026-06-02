{{ config(materialized='table') }}

with staged as (
    select * from {{ ref('stg_employees') }}
),

final as (
    select
        md5(coalesce(employee_id, '')) as employee_key,
        employee_id,
        employee_name,
        role,
        store_id,
        is_deleted,
        updated_at
    from staged
    where is_deleted = false
)

select * from final
