
#Data model

##Tabla users

Cada fila va a tener un usuario

Campos:
    -user_id
    -age
    -country
    -device
    -acquisition_channel
    -registration_date
    -income_level
    -occupation

##Tabla events

Cada fila representa un evento de un usuario 

Campos: 
    -user_id
    -event
    -timestamp

Eventos posibles
    singup
    -kyc_completed
    -first_deposit
    -card_ordered
    -first_payment
    -investment_started
