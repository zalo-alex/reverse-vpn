import os

#wt.exe -w 1 new-tab 

project_dir = os.path.dirname(__file__)

server_dir = os.path.join(project_dir, "server")
client_dir = os.path.join(project_dir, "client")

os.system(f'wt.exe -w 1 new-tab cmd /c "cd /d {server_dir} && py main.py"')
os.system(f'wt.exe -w 1 new-tab cmd /c "cd /d {client_dir} && py main.py localhost 16782 h"')
os.system(f'wt.exe -w 1 new-tab cmd /c "cd /d {client_dir} && py main.py localhost 16782 c"')