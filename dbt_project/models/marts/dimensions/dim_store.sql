{{ config(materialized='table') }}

with staged as (
    select * from {{ ref('stg_stores') }}
),

final as (
    select
        md5(coalesce(store_id, '')) as store_key,
        store_id,
        store_name,
        address,
        city,
        state,
        phone,
        manager_name,
        opened_date,
        updated_at
    from staged
)

select * from final
