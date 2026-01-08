from dataclasses import (
  dataclass,
  field,
)

@dataclass(frozen=True)
class WorkspaceData:
  grid_height: int = field(default_factory=int)
  grid_width: int = field(default_factory=int)
  x: int = field(default_factory=int)
  y: int = field(default_factory=int)

@dataclass(frozen=True)
class WSetData:
  index: int = field(default_factory=int)
  name: str = field(default_factory=str)
  output_id: int = field(default_factory=int)
  output_name: str = field(default_factory=str)
  workspace: WorkspaceData = field(default_factory=WorkspaceData)

class WSet:
  def __new__(cls):
    raise TypeError('WSet is a static class and cannot be instantiated.')

  @staticmethod
  def new(*args, **kwargs):
    # Handle hyphens from IPC
    if 'output-id' in kwargs:
        kwargs['output_id'] = kwargs.pop('output-id')
    if 'output-name' in kwargs:
        kwargs['output_name'] = kwargs.pop('output-name')
    
    if 'workspace' in kwargs and isinstance(kwargs['workspace'], dict):
        kwargs['workspace'] = WorkspaceData(**kwargs['workspace'])
        
    # Strip unknown keys
    allowed_keys = WSetData.__dataclass_fields__.keys()
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys}

    return WSetData(*args, **filtered_kwargs)
