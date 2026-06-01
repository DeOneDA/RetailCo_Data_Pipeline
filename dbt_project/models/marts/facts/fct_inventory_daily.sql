{{ config(materialized='table') }}

with movements as (
    select * from {{ ref('stg_inventory_movements') }}
),

dim_product as (
    select * from {{ ref('dim_product') }}
    where is_current = true
),

dim_store as (
    select * from {{ ref('dim_store') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

-- aggregate movements into daily snapshots
daily_movements as (
    select
        cast(movement_date as date)     as movement_day,
        product_id,
        store_id,
        sum(case when movement_type = 'received'
            then quantity else 0 end)   as quantity_received,
        sum(case when movement_type = 'sold'
            then quantity else 0 end)   as quantity_sold,
        sum(case when movement_type = 'adjustment'
            then quantity else 0 end)   as quantity_adjusted
    from movements
    group by
        cast(movement_date as date),
        product_id,
        store_id
),

final as (
    select
        -- surrogate key
        md5(
            dm.product_id || '|' ||
            dm.store_id   || '|' ||
            cast(dm.movement_day as varchar)
        )                               as inventory_key,

        -- foreign keys
        dd.date_key                     as date_key,
        dp.product_key                  as product_key,
        ds.store_key                    as store_key,

        -- measures
        dm.quantity_received,
        dm.quantity_sold,
        dm.quantity_adjusted,
        -- running quantity on hand
        sum(dm.quantity_received - dm.quantity_sold + dm.quantity_adjusted)
            over (
                partition by dm.product_id, dm.store_id
                order by dm.movement_day
                rows between unbounded preceding and current row
            )                           as quantity_on_hand

    from daily_movements dm
    left join dim_product dp
        on dm.product_id = dp.product_id
    left join dim_store ds
        on dm.store_id = ds.store_id
    left join dim_date dd
        on dm.movement_day = dd.full_date
)

select * from final
