from dataclasses import (
  dataclass,
  field,
)
from workspace import WorkspaceData

@dataclass(frozen=True)
class OutputData:
  geometry: dict = field(default_factory=dict)
  id: int = field(default_factory=int)
  name: str = field(default_factory=str)
  workarea: dict = field(default_factory=dict)
  workspace: WorkspaceData = field(default_factory=WorkspaceData)
  wset_index: int = field(default_factory=int)

class Output:
  def __new__(cls):
    raise TypeError('Output is a static class and cannot be instantiated.')

  @staticmethod
  def new(*args, **kwargs):
    # Handle the hyphen in 'wset-index' from IPC
    if 'wset-index' in kwargs:
        kwargs['wset_index'] = kwargs.pop('wset-index')
    
    if 'workspace' in kwargs and isinstance(kwargs['workspace'], dict):
        kwargs['workspace'] = WorkspaceData(**kwargs['workspace'])

    # Strip unknown keys
    allowed_keys = OutputData.__dataclass_fields__.keys()
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys}

    return OutputData(*args, **filtered_kwargs)
