{{ config(materialized='table') }}

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

dim_customer as (
    select * from {{ ref('dim_customer') }}
    where is_current = true
),

dim_product as (
    select * from {{ ref('dim_product') }}
    where is_current = true
),

dim_store as (
    select * from {{ ref('dim_store') }}
),

dim_employee as (
    select * from {{ ref('dim_employee') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

final as (
    select
        -- surrogate key
        md5(oi.order_item_id)                   as sales_key,

        -- foreign keys to dimensions
        dd.date_key                             as date_key,
        dc.customer_key                         as customer_key,
        dp.product_key                          as product_key,
        ds.store_key                            as store_key,
        de.employee_key                         as employee_key,

        -- natural keys (for traceability)
        oi.order_id,
        oi.order_item_id,

        -- measures
        oi.quantity,
        oi.unit_price,
        oi.discount_amount,
        oi.line_total

    from order_items oi
    left join orders o
        on oi.order_id = o.order_id
    left join dim_customer dc
        on o.customer_id = dc.customer_id
    left join dim_product dp
        on oi.product_id = dp.product_id
    left join dim_store ds
        on o.store_id = ds.store_id
    left join dim_employee de
        on o.employee_id = de.employee_id
    left join dim_date dd
        on cast(o.created_at as date) = dd.full_date
    -- exclude cancelled orders from sales facts
    where o.status != 'cancelled'
)

select * from final
