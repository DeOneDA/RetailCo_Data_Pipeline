{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

dim_customer as (
    select * from {{ ref('dim_customer') }}
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
        md5(coalesce(o.order_id, '')) as order_key,

        dd.date_key as date_key,
        dc.customer_key as customer_key,
        ds.store_key as store_key,
        de.employee_key as employee_key,

        o.order_id,
        o.status,

        o.pending_at,
        o.paid_at,
        o.shipped_at,
        o.delivered_at,
        o.cancelled_at,

        case
            when o.paid_at is not null and o.pending_at is not null
            then extract(epoch from (o.paid_at - o.pending_at))/3600
        end as hours_pending_to_paid,

        case
            when o.shipped_at is not null and o.paid_at is not null
            then extract(epoch from (o.shipped_at - o.paid_at))/3600
        end as hours_paid_to_shipped,

        case
            when o.delivered_at is not null and o.shipped_at is not null
            then extract(epoch from (o.delivered_at - o.shipped_at))/3600
        end as hours_shipped_to_delivered,

        case
            when o.delivered_at is not null and o.pending_at is not null
            then extract(epoch from (o.delivered_at - o.pending_at))/3600
        end as total_fulfillment_hours

    from orders o
    left join dim_customer dc
        on o.customer_id = dc.customer_id
    left join dim_store ds
        on o.store_id = ds.store_id
    left join dim_employee de
        on o.employee_id = de.employee_id
    left join dim_date dd
        on cast(o.created_at as date) = dd.full_date
)

select * from final