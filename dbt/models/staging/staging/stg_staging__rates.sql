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
        rateusd,
        timestamp,
        valid_from,
        valid_to,
        is_valid

    from source

)

select * from renamed
