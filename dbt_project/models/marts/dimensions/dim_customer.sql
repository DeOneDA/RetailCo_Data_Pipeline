{{ config(materialized='table') }}

with snapshot_data as (
    select * from {{ ref('snap_customer') }}
),

final as (
    select
        -- surrogate key using md5 hash for stability
        md5(customer_id || '|' || cast(dbt_valid_from as varchar))  as customer_key,
        customer_id,
        first_name,
        last_name,
        first_name || ' ' || last_name                              as full_name,
        email,
        phone,
        address,
        city,
        state,
        segment,
        tier,
        registered_at,
        is_deleted,
        -- SCD2 columns
        dbt_valid_from                                              as valid_from,
        dbt_valid_to                                                as valid_to,
        case
            when dbt_valid_to is null then true else false
        end                                                         as is_current
    from snapshot_data
)

select * from final
