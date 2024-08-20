with 

source as (

    select * from {{ source('staging', 'exchanges') }}

),

renamed as (

    select
        exchangeid,
        name,
        cast(rank as numeric) as rank,
        cast(percenttotalvolume as numeric) as percenttotalvolume,
        cast(volumeusd as numeric) as volumeusd,
        cast(tradingpairs as numeric) as tradingpairs,
        socket,
        exchangeurl,
        TIMESTAMP_MILLIS(updated) as updated,
        TIMESTAMP_MILLIS(timestamp) as timestamp,
        TIMESTAMP_MILLIS(valid_from) as valid_from,
        TIMESTAMP_MILLIS(CAST(valid_to AS INT64)) as valid_to,
        cast(is_valid as numeric) as is_valid,

    from source

)

select * from renamed
