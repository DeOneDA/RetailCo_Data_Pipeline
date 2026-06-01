-- Custom test: fct_payments must not contain flagged payment ids
select p.*
from {{ ref('fct_payments') }} p
inner join {{ ref('flagged_payments') }} f
    on p.payment_id = f.payment_id
