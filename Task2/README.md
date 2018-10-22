

INSTRUCTIONS TO USE TASK 2


Make sure you are using python 3

Start the server with the command: 

python alice.py 

Start the client with the command: 

python bob.py 


Send messages from bob.py to alice.py

Send 'quit' to terminate connection and both programs.

The interactions between bob.py and alice.py are protected from:

Traffic Analysis
Modification
Replay
Interruption
Repudiation

All log files for all data sent between alice.py and bob.py for all sessions are stored in the 'log' folder.

The current port number that the server is using is stored in the 'port' file. If it is empty, then the server (alice.py) will look for an empty port. It is recommended to leave it emtpt.

It is unadvised to terminate the server (alice.py) before the client (bob.py).