{{
    config(
        materialized='table'
    )
}}


with markets as (
    select *
    from {{ ref('stg_staging__markets') }}
),

most_recent_timestamp as (
    select markets.baseid as id, max(date(markets.updated)) as date
    from markets
    where markets.volumeusd24hr is not null and markets.volumeusd24hr > 0
    group by markets.baseid
),


ranked_excahnges as (
    select m.baseid as id, m.rank as rank, m.exchangeid as exchangeid, m.volumeusd24hr as volumeusd24hr, date(m.updated) as date,
    row_number() over (
        partition by m.baseid, date(m.updated)
        order by rank, volumeusd24hr desc
    ) as rn
    
    from markets m
    join most_recent_timestamp mrt on m.baseid = mrt.id and date(m.updated) = mrt.date
),

get_top_5 as (
    select re.id as id, re.exchangeid, max(re.volumeusd24hr), max(re.date) as date from ranked_excahnges re where re.rn <= 5
    group by id, exchangeid
)

select distinct * from get_top_5 where id = 'bitcoin'