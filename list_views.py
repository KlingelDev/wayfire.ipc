#!/home/karl/opt/wayfire/bin/python3

from wayfire import WayfireSocket

socket = WayfireSocket()
l = socket.list_views()

for x in l:
  print(x['app-id'], x['id'])
