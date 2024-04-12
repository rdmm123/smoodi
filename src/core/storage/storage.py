from typing import Protocol, Any

class Storage(Protocol):
    def write(self, to: str, value: Any, **params: Any) -> None:
        raise NotImplementedError()
    
    def read(self, source: str, **params: Any) -> Any:
        raise NotImplementedError()
    
    def delete(self, where: str, **params: Any) -> None:
        raise NotImplementedError()
    
    def flush(self, **params: Any) -> None:
        raise NotImplementedError()