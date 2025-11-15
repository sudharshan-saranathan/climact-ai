# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: factory
# Description: Factory functions and base class for creating dynamic resource classes
#              from basic Stream descriptors (see apps.stream.default).
# ----------------------------------------------------------------------------------------------------------------------

from typing import Any, Dict, List, Sequence, Tuple, Type, Union
import default as streams

StreamType = Type[streams.Stream]
StreamSpec = Union[str, StreamType]

# Instance behavior for dynamically created resource classes:
class ResourceBase:

    COMPONENTS: List[StreamType] = []

    # Default constructor:
    def __init__(self, name: str, **values: Any) -> None:

        # Resource name and value(s):
        self._label = name
        self._values: Dict[str, Any] = {}

        # initialize keys declared by COMPONENTS
        for comp in self.components():
            key = comp.KEY
            # initialize to provided value or None
            self._values[key] = values.get(key)

        # accept and store any extra values as-is (optionally enforce no extras)
        for k, v in values.items():
            if k not in self._values:
                # store extras under their keys but don't advertise them as components
                self._values[k] = v

    def set(self, key: str, value: Any) -> None:
        allowed = {c.KEY for c in self.components()}
        if key not in allowed:
            raise KeyError(f"Unknown attribute '{key}' for resource {self.__class__.__name__}")
        self._values[key] = value

    def get(self, key: str) -> Any:
        return self._values.get(key)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"name": self._label}
        d.update(self._values)
        return d

    @classmethod
    def components(cls) -> List[StreamType]:
        return list(getattr(cls, "COMPONENTS", []))

    @classmethod
    def components_metadata(cls) -> Dict[str, Dict[str, Any]]:
        return {c.KEY: c.metadata() for c in cls.components()}

    def __repr__(self) -> str:  # pragma: no cover - trivial
        comps = ",".join(c.KEY for c in self.components())
        return f"<{self.__class__.__name__} name={self._label} components=[{comps}]>"

# Class for creating dynamic resource classes:
class ResourceFactory:
    """Factory for dynamically creating resource classes composed of Stream types.

    Usage:
      ResourceFactory.create_class('Steel', ['mass', 'capex'])
      ResourceFactory.create_instance('Steel', ['mass','capex'], mass=100, capex=200)
    """

    # simple cache mapping (class_name, tuple(keys)) -> generated class
    _cache: Dict[Tuple[str, Tuple[str, ...]], Type[ResourceBase]] = {}

    @staticmethod
    def _resolve_streams(specs: Sequence[StreamSpec]) -> List[StreamType]:
        """Resolve a sequence of stream specs (keys or classes) to Stream subclasses.

        Raises ValueError if a key cannot be resolved or duplicates are encountered.
        """
        resolved: List[StreamType] = []
        seen: set[str] = set()
        for s in specs:
            if isinstance(s, str):
                cls = streams.get_stream_class(s)
                if cls is None:
                    raise ValueError(f"Unknown stream key: {s}")
            elif isinstance(s, type) and issubclass(s, streams.Stream):
                cls = s
            else:
                raise ValueError(f"Invalid stream spec: {s!r}")

            if cls.KEY in seen:
                raise ValueError(f"Duplicate stream key: {cls.KEY}")
            seen.add(cls.KEY)
            resolved.append(cls)
        return resolved

    @classmethod
    def create_class(cls, name: str, specs: Sequence[StreamSpec]) -> Type[ResourceBase]:
        """Create (or return cached) dynamic resource class composed of the given streams.

        `specs` may be a sequence of stream keys (str) or Stream subclasses.
        The returned class will have a class attribute `COMPONENTS` listing the
        Stream classes and will mix in `ResourceBase` for instance behavior.
        """
        streams_list = cls._resolve_streams(specs)
        keys = tuple(s.KEY for s in streams_list)
        cache_key = (name, keys)
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        # Build bases so users can isinstance-check against stream classes if needed
        bases: Tuple[object, ...] = tuple(streams_list + [ResourceBase])

        attrs = {
            "COMPONENTS": streams_list,
            "__doc__": f"Dynamic resource class '{name}' composed of: {', '.join(keys)}",
        }

        new_cls = type(name, bases, attrs)
        cls._cache[cache_key] = new_cls
        return new_cls

    @classmethod
    def create_instance(cls, name: str, specs: Sequence[StreamSpec], **values: Any) -> ResourceBase:
        new_cls = cls.create_class(name, specs)
        return new_cls(name, **values)

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()

    @classmethod
    def is_dynamic_resource(cls, obj: object) -> bool:
        return hasattr(obj, "COMPONENTS") and isinstance(getattr(obj, "COMPONENTS"), list)
