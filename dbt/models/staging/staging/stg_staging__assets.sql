with 

source as (

    select * from {{ source('staging', 'assets') }}

),

renamed as (

    select
        cast(priceUsd as numeric) as priceusd,
        TIMESTAMP_MILLIS(timestamp) as timestamp,
        cast(circulatingSupply as numeric) as circulatingsupply,
        TIMESTAMP(date) AS date,
        id,
        TIMESTAMP_MILLIS(valid_from) as valid_from,
        TIMESTAMP_MILLIS(CAST(valid_to AS INT64)) as valid_to,
        cast(is_valid as numeric) as is_valid
    from source

)

select * from renamed
