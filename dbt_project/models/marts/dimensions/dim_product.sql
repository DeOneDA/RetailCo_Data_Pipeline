{{ config(materialized='table') }}

with snapshot_data as (
    select * from {{ ref('snap_product') }}
),

final as (
    select
        -- surrogate key
       md5(coalesce(product_id, '') || '|' || coalesce(cast(dbt_valid_from as varchar), '')) as product_key,
        product_id,
        product_name,
        sku,
        category,
        sub_category,
        brand,
        supplier,
        cost_price,
        selling_price,
        is_deleted,
        -- SCD2 columns
        dbt_valid_from                                               as valid_from,
        dbt_valid_to                                                 as valid_to,
        case
            when dbt_valid_to is null then true else false
        end                                                          as is_current
    from snapshot_data
)

select * from final
