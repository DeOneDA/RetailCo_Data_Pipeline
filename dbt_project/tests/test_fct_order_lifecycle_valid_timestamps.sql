-- Custom test: paid_at must always be after pending_at
select *
from {{ ref('fct_order_lifecycle') }}
where paid_at is not null
  and pending_at is not null
  and paid_at < pending_at
