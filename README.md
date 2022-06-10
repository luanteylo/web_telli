# WEB_TELLI

A simple client-server example using json and the cherrypy library


## Getting Started

first, install the requirements

```bash
apt install python3
apt install python3-pip
```


then, install the python packages

```bash
cd web_telli/
pip3 install -r requirements.txt

```

#### Using it

start the server

```bash
python3 server.py --host_ip 0.0.0.0  --host_port 8080 
```

In a python console import and create the Client

```python
from client import Client

c = Client(host='0.0.0.0', port='8080')
```

You can send a message to the server

```python
c.send(action='echo', value='hello world')
```

If the server answers you, it will be stored in  ```response```

```python
print(c.response)
'hello world'
```

You can send more "complex" values to the server. Not only strings.

```python
c.send(action='sum', value=[1, 2])
print(c.response)
3
c.send(action='div', value=[1, 2])
print(c.response)
0.5
```


Have fun :)
