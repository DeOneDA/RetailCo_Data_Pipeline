-- Custom test: quantity on hand should never be negative
select *
from {{ ref('fct_inventory_daily') }}
where quantity_on_hand < 0
