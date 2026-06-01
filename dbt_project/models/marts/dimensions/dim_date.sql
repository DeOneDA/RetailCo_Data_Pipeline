{{ config(materialized='table') }}

with date_spine as (
    select generate_series(
        '2022-01-01'::date,
        '2026-12-31'::date,
        '1 day'::interval
    )::date as full_date
),

nigerian_holidays as (
    select * from (values
        -- 2022
        ('2022-01-01', 'New Year''s Day'),
        ('2022-04-15', 'Good Friday'),
        ('2022-04-18', 'Easter Monday'),
        ('2022-05-01', 'Workers Day'),
        ('2022-05-02', 'Eid al-Fitr'),
        ('2022-05-03', 'Eid al-Fitr Holiday'),
        ('2022-06-12', 'Democracy Day'),
        ('2022-07-10', 'Eid al-Adha'),
        ('2022-10-01', 'Independence Day'),
        ('2022-10-08', 'Eid al-Mawlid'),
        ('2022-12-25', 'Christmas Day'),
        ('2022-12-26', 'Boxing Day'),
        -- 2023
        ('2023-01-01', 'New Year''s Day'),
        ('2023-04-07', 'Good Friday'),
        ('2023-04-10', 'Easter Monday'),
        ('2023-04-21', 'Eid al-Fitr'),
        ('2023-04-22', 'Eid al-Fitr Holiday'),
        ('2023-05-01', 'Workers Day'),
        ('2023-06-12', 'Democracy Day'),
        ('2023-06-28', 'Eid al-Adha'),
        ('2023-09-27', 'Eid al-Mawlid'),
        ('2023-10-01', 'Independence Day'),
        ('2023-12-25', 'Christmas Day'),
        ('2023-12-26', 'Boxing Day'),
        -- 2024
        ('2024-01-01', 'New Year''s Day'),
        ('2024-03-29', 'Good Friday'),
        ('2024-04-01', 'Easter Monday'),
        ('2024-04-10', 'Eid al-Fitr'),
        ('2024-04-11', 'Eid al-Fitr Holiday'),
        ('2024-05-01', 'Workers Day'),
        ('2024-06-12', 'Democracy Day'),
        ('2024-06-16', 'Eid al-Adha'),
        ('2024-09-15', 'Eid al-Mawlid'),
        ('2024-10-01', 'Independence Day'),
        ('2024-12-25', 'Christmas Day'),
        ('2024-12-26', 'Boxing Day'),
        -- 2025
        ('2025-01-01', 'New Year''s Day'),
        ('2025-03-30', 'Eid al-Fitr'),
        ('2025-03-31', 'Eid al-Fitr Holiday'),
        ('2025-04-18', 'Good Friday'),
        ('2025-04-21', 'Easter Monday'),
        ('2025-05-01', 'Workers Day'),
        ('2025-06-06', 'Eid al-Adha'),
        ('2025-06-12', 'Democracy Day'),
        ('2025-09-04', 'Eid al-Mawlid'),
        ('2025-10-01', 'Independence Day'),
        ('2025-12-25', 'Christmas Day'),
        ('2025-12-26', 'Boxing Day'),
        -- 2026
        ('2026-01-01', 'New Year''s Day'),
        ('2026-03-20', 'Eid al-Fitr'),
        ('2026-03-21', 'Eid al-Fitr Holiday'),
        ('2026-04-03', 'Good Friday'),
        ('2026-04-06', 'Easter Monday'),
        ('2026-05-01', 'Workers Day'),
        ('2026-05-27', 'Eid al-Adha'),
        ('2026-06-12', 'Democracy Day'),
        ('2026-10-01', 'Independence Day'),
        ('2026-12-25', 'Christmas Day'),
        ('2026-12-26', 'Boxing Day')
    ) as t(holiday_date, holiday_name)
),

final as (
    select
        to_char(full_date, 'YYYYMMDD')::int         as date_key,
        full_date,
        extract(year from full_date)::int            as year,
        extract(quarter from full_date)::int         as quarter,
        extract(month from full_date)::int           as month,
        to_char(full_date, 'Month')                  as month_name,
        extract(week from full_date)::int            as week,
        extract(dow from full_date)::int             as day_of_week,
        to_char(full_date, 'Day')                    as day_name,
        case
            when extract(dow from full_date) in (0, 6)
            then true else false
        end                                          as is_weekend,
        case
            when h.holiday_date is not null
            then true else false
        end                                          as is_public_holiday,
        h.holiday_name                               as holiday_name
    from date_spine d
    left join nigerian_holidays h
        on d.full_date = h.holiday_date::date
)

select * from final
