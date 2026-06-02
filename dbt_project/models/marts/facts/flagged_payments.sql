{{ config(materialized='table') }}

with staged as (
    select * from {{ ref('stg_payments') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

final as (
    select
        md5(coalesce(p.payment_id, '')) as flag_key,
        p.payment_id,
        p.order_id,
        p.customer_id,
        p.payment_method_id,
        p.amount_paid,
        p.payment_date,
        case
            when p.amount_paid = 0 then 'Zero amount payment'
            when p.amount_paid < 0 then 'Unexplained negative amount'
            else 'Unknown anomaly'
        end as flag_reason,
        p.created_at as flagged_at
    from staged p
    where
        p.amount_paid = 0
        or (
            p.amount_paid < 0
            and not exists (
                select 1
                from orders o
                where o.order_id = p.order_id
                  and o.status in ('delivered', 'shipped')
            )
        )
)

select * from final