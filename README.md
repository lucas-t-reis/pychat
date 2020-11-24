# Pychat: TCP/UDP Server/client interface using Python

## Non-functional requirements

- ~List with active nodes, with command "BYE" to remove a node.~
  
- Buffer with size = 1 to store files.
  
## Functional requirements

- MSG:"text" forward message to all other nodes excepts source.

- MSG:"name":"text" repeats above function plus printing source's name.

- ~LIST: print the entire list.~

- FILE:"file" starts a TCP connection with server, send file and finish it.

- INFO:"text" send a message to all active nodes to sinalize that the given node share a file.

- GET:"file" starts a TCP connection with server, get file "file" and finish it, print and error message if it fails.

- ~BYE: finish connection with server and send message to all other nodes informing it.~
