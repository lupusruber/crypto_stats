{{
    config(
        materialized='table'
    )
}}

with assets as ( 
    select*
    from {{ ref('stg_staging__assets') }}
)

select assets.id, avg(assets.priceusd) as avg_asset_price, assets.timestamp from assets
group by assets.id, assets.timestamp
order by assets.id asc, timestamp asc