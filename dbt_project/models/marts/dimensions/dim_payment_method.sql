{{ config(materialized='table') }}

with staged as (
    select * from {{ ref('stg_payment_methods') }}
),

final as (
    select
        md5(payment_method_id)  as payment_method_key,
        payment_method_id,
        method_name,
        provider,
        is_digital,
        updated_at
    from staged
)

select * from final
