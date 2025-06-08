
# UDP File Transfer System

This project has implemented a file transfer system based on the UDP protocol. The client and the multi-threaded server communicate through a protocol to achieve functions such as resume from breakpoint, retransmission after timeout, and Base64 encoding.

## Project Structure

- `UDPclient.py` – The file download client
- `UDPserver.py` – The multi-threaded file server
- `files.txt` – List of filenames to download

## Start the Server
```
python UDPserver.py <port>
```

## Start the Client
```
python UDPclient.py <server_ip> <port> <file_list_path>
```
