with 

source as (

    select * from {{ source('staging', 'assets') }}

),

renamed as (

    select
        priceusd,
        timestamp,
        circulatingsupply,
        date,
        id,
        valid_from,
        valid_to,
        is_valid

    from source

)

select * from renamed
