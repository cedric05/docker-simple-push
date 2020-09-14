from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Layer:
    media_type: str
    size: int
    digest: str

    @staticmethod
    def from_dict(obj: Any) -> 'Layer':
        assert isinstance(obj, dict)
        media_type = from_str(obj.get("mediaType"))
        size = from_int(obj.get("size"))
        digest = from_str(obj.get("digest"))
        return Layer(media_type, size, digest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mediaType"] = from_str(self.media_type)
        result["size"] = from_int(self.size)
        result["digest"] = from_str(self.digest)
        return result


@dataclass
class Manifest:
    schema_version: int
    media_type: str
    config: Layer
    layers: List[Layer]

    @staticmethod
    def from_dict(obj: Any) -> 'Manifest':
        assert isinstance(obj, dict)
        schema_version = from_int(obj.get("schemaVersion"))
        media_type = from_str(obj.get("mediaType"))
        config = Layer.from_dict(obj.get("config"))
        layers = from_list(Layer.from_dict, obj.get("layers"))
        return Manifest(schema_version, media_type, config, layers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["schemaVersion"] = from_int(self.schema_version)
        result["mediaType"] = from_str(self.media_type)
        result["config"] = to_class(Layer, self.config)
        result["layers"] = from_list(lambda x: to_class(Layer, x),
                                     self.layers)
        return result