with 

source as (

    select * from {{ source('staging', 'exchanges') }}

),

renamed as (

    select
        exchangeid,
        name,
        rank,
        percenttotalvolume,
        volumeusd,
        tradingpairs,
        socket,
        exchangeurl,
        updated,
        timestamp,
        valid_from,
        valid_to,
        is_valid

    from source

)

select * from renamed
