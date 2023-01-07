# response structure
````json
{
    "status_code": {status_code},
    "sent_cmd": {command which was sent},
    "response": {data} 
}
````
> ## status_code 
> returns the status codes that you can read more about [here](#status-codes)

> ## sent_cmd
> returns the request command that was sent to the database server

> ## response 
> it's the data that was requested

# request structure
````json
{
    "sender_uuid": {UUID},
    "command": {command string},
    "data": {data}
}
````

# establish connection
````json
{
    "user": {user_id},
    "key": {key}
}
````

# response on connection
````json
{
    "user": {user_id},
    "sender_uuid": {UUID},
    "status_code": {status_code}
}
````

# Status codes

- Succes

- Server_error

- Request_erroe

- Undefiend