{{ config(materialized='table') }}

with staged as (
    select * from {{ ref('stg_payments') }}
),

final as (
    select
        md5(payment_id)     as flag_key,
        payment_id,
        order_id,
        customer_id,
        payment_method_id,
        amount_paid,
        payment_date,
        case
            when amount_paid = 0 then 'Zero amount payment'
            when amount_paid < 0 then 'Unexplained negative amount'
            else 'Unknown anomaly'
        end                 as flag_reason,
        created_at          as flagged_at
    from staged
    where
        amount_paid = 0
        or (amount_paid < 0 and order_id not in (
            -- exclude legitimate refunds (orders that exist and were paid)
            select order_id from {{ ref('stg_orders') }}
            where status in ('delivered', 'shipped')
        ))
)

select * from final
