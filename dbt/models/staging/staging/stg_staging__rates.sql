with 

source as (

    select * from {{ source('staging', 'rates') }}

),

renamed as (

    select
        id,
        symbol,
        currencysymbol,
        type,
        cast(rateusd as numeric) as rateusd,
        TIMESTAMP_MILLIS(timestamp) as timestamp,
        TIMESTAMP_MILLIS(valid_from) as valid_from,
        TIMESTAMP_MILLIS(CAST(valid_to AS INT64)) as valid_to,
        cast(is_valid as numeric) as is_valid,

    from source

)

select * from renamed
