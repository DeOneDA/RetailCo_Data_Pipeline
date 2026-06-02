{{ config(materialized='table') }}

with payments as (
    select * from {{ ref('stg_payments') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

flagged as (
    select payment_id from {{ ref('flagged_payments') }}
),

dim_customer as (
    select * from {{ ref('dim_customer') }}
    where is_current = true
),

dim_store as (
    select * from {{ ref('dim_store') }}
),

dim_payment_method as (
    select * from {{ ref('dim_payment_method') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

final as (
    select
        md5(coalesce(p.payment_id, '')) as payment_key,

        dd.date_key as date_key,
        dc.customer_key as customer_key,
        ds.store_key as store_key,
        dpm.payment_method_key as payment_method_key,

        p.payment_id,
        p.order_id,

        p.amount_paid,
        case
            when p.amount_paid < 0 then true else false
        end as is_refund

    from payments p
    left join orders o
        on p.order_id = o.order_id
    left join flagged f
        on p.payment_id = f.payment_id
    left join dim_customer dc
        on p.customer_id = dc.customer_id
    left join dim_store ds
        on o.store_id = ds.store_id
    left join dim_payment_method dpm
        on p.payment_method_id = dpm.payment_method_id
    left join dim_date dd
        on cast(p.payment_date as date) = dd.full_date
    where f.payment_id is null
)

select * from final