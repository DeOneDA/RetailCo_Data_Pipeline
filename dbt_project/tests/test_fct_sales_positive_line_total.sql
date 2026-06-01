-- Custom test: all non-refund line totals must be positive
select *
from {{ ref('fct_sales') }}
where line_total <= 0
