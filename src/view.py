from dataclasses import (
  dataclass,
  field,
)

@dataclass(frozen=True)
class ViewData:
  activated:bool = field(default_factory = bool)
  app_id:str = field(default_factory = str)
  base_geometry:dict = field(default_factory = dict)
  bbox:dict = field(default_factory = dict)
  geometry:dict = field(default_factory = dict)
  id:int = field(default_factory = int)
  last_focus_timestamp:str = field(default_factory = str)
  layer:str = field(default_factory = str)
  mapped:bool = field(default_factory = bool)
  max_size:dict = field(default_factory = dict)
  min_size:dict = field(default_factory = dict)
  minimized:bool = field(default_factory = bool)
  output_id:int = field(default_factory = int)
  output_name:str = field(default_factory = str)
  parent:int = field(default_factory = int)
  pid:int = field(default_factory = int)
  role:str = field(default_factory = str)
  sticky:bool = field(default_factory = bool)
  tiled_edges:int = field(default_factory = int)
  title:str = field(default_factory = str)
  type:str = field(default_factory = str)
  wset_index:int = field(default_factory = str)

class View:
  def __new__(cls):
    raise TypeError('View is a static class and cannot be instantiated.')

  @staticmethod
  def new(*args, **kwargs):
    return ViewData(*args, **kwargs)

