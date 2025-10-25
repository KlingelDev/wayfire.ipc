#!/usr/bin/env python3

from wayfire import WayfireSocket

import sys
sys.path.append('src')

from view import (
  View,
  ViewData
)

def run() -> int:
  socket = WayfireSocket()

  for l in socket.list_views():
    print(l, '\n')
  print('\n\n')
  print(socket.list_wsets())

  print(socket.get_tiling_layout(2, 0, 0))

  return 0

if __name__ == '__main__':
  run()
