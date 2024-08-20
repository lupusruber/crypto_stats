with 

source as (

    select * from {{ source('staging', 'markets') }}

),

renamed as (

    select
        exchangeid,
        cast(rank as numeric) as rank,
        basesymbol,
        baseid,
        quotesymbol,
        quoteid,
        cast(pricequote as numeric) as pricequote,
        cast(priceusd as numeric) as priceusd,
        cast(volumeusd24hr as numeric) as volumeusd24hr,
        cast(percentexchangevolume as numeric) as percentexchangevolume,
        cast(tradescount24hr as numeric) as tradescount24hr,
        TIMESTAMP_MILLIS(updated) as updated,
        TIMESTAMP_MILLIS(timestamp) as timestamp,
        key,
        TIMESTAMP_MILLIS(valid_from) as valid_from,
        TIMESTAMP_MILLIS(CAST(valid_to AS INT64)) as valid_to,
        cast(is_valid as numeric) as is_valid,
        
    from source

)

select * from renamed
