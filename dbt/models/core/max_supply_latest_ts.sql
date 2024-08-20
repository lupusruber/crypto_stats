{{
    config(
        materialized='table'
    )
}}

with assets as (
    select *
    from {{ ref('stg_staging__assets') }}
),

latest_asset_with_timestamp as (
    select assets.id as id, max(assets.timestamp) as ts from assets
    group by assets.id
)

select assets.id, assets.timestamp, assets.circulatingsupply from assets
join latest_asset_with_timestamp lats on assets.id = lats.id and assets.timestamp = lats.ts
order by assets.id asc