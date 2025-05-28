This software need 3 part:
1. client
2. server
3. intermediate layer

Note:
client: user input data
server: caculate
intermediate layer: interact client and server

//ravenzal: please decide your work part and language used, put the message into client.md/server.md/intermediate_layer.md

## PLAN:
### Python-Client
User interface that receives input and displays results.
Sends calculation requests to the middle layer via HTTP protocol.

### Go-Middle_Layer
Exposes a REST API to receive client requests.
Forwards requests to the Matlab server and returns results.

### Matlab-Calculation_Server
Runs as a TCP server listening for computation requests.
Performs trigonometric calculations and returns results.
