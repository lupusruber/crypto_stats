with 

source as (

    select * from {{ source('staging', 'markets') }}

),

renamed as (

    select
        exchangeid,
        rank,
        basesymbol,
        baseid,
        quotesymbol,
        quoteid,
        pricequote,
        priceusd,
        volumeusd24hr,
        percentexchangevolume,
        tradescount24hr,
        updated,
        timestamp,
        key,
        valid_from,
        valid_to,
        is_valid

    from source

)

select * from renamed
