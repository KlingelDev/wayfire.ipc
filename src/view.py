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
  focusable:bool = field(default_factory = bool)
  fullscreen:bool = field(default_factory = bool)
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
  wset_index:int = field(default_factory = int)

class View:
  def __new__(cls):
    raise TypeError('View is a static class and cannot be instantiated.')

  @staticmethod
  def new(*args, **kwargs):
    if 'wset-index' in kwargs:
        kwargs['wset_index'] = kwargs.pop('wset-index')
    if 'app-id' in kwargs:
        kwargs['app_id'] = kwargs.pop('app-id')
    if 'base-geometry' in kwargs:
        kwargs['base_geometry'] = kwargs.pop('base-geometry')
    if 'last-focus-timestamp' in kwargs:
        kwargs['last_focus_timestamp'] = kwargs.pop('last-focus-timestamp')
    if 'max-size' in kwargs:
        kwargs['max_size'] = kwargs.pop('max-size')
    if 'min-size' in kwargs:
        kwargs['min_size'] = kwargs.pop('min-size')
    if 'output-id' in kwargs:
        kwargs['output_id'] = kwargs.pop('output-id')
    if 'output-name' in kwargs:
        kwargs['output_name'] = kwargs.pop('output-name')
    if 'tiled-edges' in kwargs:
        kwargs['tiled_edges'] = kwargs.pop('tiled-edges')

    # Strip unknown keys
    allowed_keys = ViewData.__dataclass_fields__.keys()
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys}

    return ViewData(*args, **filtered_kwargs)

