# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = config_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, Optional, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser

T = TypeVar("T")


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class The8080_TCP:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'The8080_TCP':
        assert isinstance(obj, dict)
        return The8080_TCP()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class Conconfig:
    hostname: str
    domainname: str
    user: str
    attach_stdin: bool
    attach_stdout: bool
    attach_stderr: bool
    exposed_ports: dict
    tty: bool
    open_stdin: bool
    stdin_once: bool
    env: List[str]
    cmd: List[str]
    args_escaped: bool
    image: str
    volumes: None
    working_dir: str
    entrypoint: None
    on_build: None
    labels: Optional[The8080_TCP] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Conconfig':
        assert isinstance(obj, dict)
        hostname = from_str(obj.get("Hostname"))
        domainname = from_str(obj.get("Domainname"))
        user = from_str(obj.get("User"))
        attach_stdin = from_bool(obj.get("AttachStdin"))
        attach_stdout = from_bool(obj.get("AttachStdout"))
        attach_stderr = from_bool(obj.get("AttachStderr"))
        exposed_ports = obj.get("ExposedPorts")
        tty = from_bool(obj.get("Tty"))
        open_stdin = from_bool(obj.get("OpenStdin"))
        stdin_once = from_bool(obj.get("StdinOnce"))
        env = from_list(from_str, obj.get("Env"))
        cmd = from_list(from_str, obj.get("Cmd"))
        args_escaped = from_bool(obj.get("ArgsEscaped"))
        image = from_str(obj.get("Image"))
        volumes = from_none(obj.get("Volumes"))
        working_dir = from_str(obj.get("WorkingDir"))
        entrypoint = from_none(obj.get("Entrypoint"))
        on_build = from_none(obj.get("OnBuild"))
        labels = from_union([from_none, The8080_TCP.from_dict],
                            obj.get("Labels"))
        return Conconfig(hostname, domainname, user, attach_stdin,
                         attach_stdout, attach_stderr, exposed_ports, tty,
                         open_stdin, stdin_once, env, cmd, args_escaped, image,
                         volumes, working_dir, entrypoint, on_build, labels)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Hostname"] = from_str(self.hostname)
        result["Domainname"] = from_str(self.domainname)
        result["User"] = from_str(self.user)
        result["AttachStdin"] = from_bool(self.attach_stdin)
        result["AttachStdout"] = from_bool(self.attach_stdout)
        result["AttachStderr"] = from_bool(self.attach_stderr)
        result["ExposedPorts"] = self.exposed_ports
        result["Tty"] = from_bool(self.tty)
        result["OpenStdin"] = from_bool(self.open_stdin)
        result["StdinOnce"] = from_bool(self.stdin_once)
        result["Env"] = from_list(from_str, self.env)
        result["Cmd"] = from_list(from_str, self.cmd)
        result["ArgsEscaped"] = from_bool(self.args_escaped)
        result["Image"] = from_str(self.image)
        result["Volumes"] = from_none(self.volumes)
        result["WorkingDir"] = from_str(self.working_dir)
        result["Entrypoint"] = from_none(self.entrypoint)
        result["OnBuild"] = from_none(self.on_build)
        result["Labels"] = from_union(
            [from_none, lambda x: to_class(The8080_TCP, x)], self.labels)
        return result


@dataclass
class Rootfs:
    type: str
    diff_ids: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Rootfs':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        diff_ids = from_list(from_str, obj.get("diff_ids"))
        return Rootfs(type, diff_ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["diff_ids"] = from_list(from_str, self.diff_ids)
        return result


@dataclass
class Config:
    architecture: str
    config: Conconfig
    # container: str
    # container_config: Conconfig
    created: datetime
    docker_version: str
    history: List[Any]
    os: str
    rootfs: Rootfs

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        architecture = from_str(obj.get("architecture"))
        config = Conconfig.from_dict(obj.get("config"))
        # container = from_str(obj.get("container"))
        # container_config = Conconfig.from_dict(obj.get("container_config"))
        created = from_datetime(obj.get("created"))
        docker_version = from_str(obj.get("docker_version"))
        history = from_list(lambda x: x, obj.get("history"))
        os = from_str(obj.get("os"))
        rootfs = Rootfs.from_dict(obj.get("rootfs"))
        return Config(
            architecture,
            config,
            # container,
            # container_config,
            created,
            docker_version,
            history,
            os,
            rootfs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["architecture"] = from_str(self.architecture)
        result["config"] = to_class(Conconfig, self.config)
        # result["container"] = from_str(self.container)
        # result["container_config"] = to_class(Conconfig, self.container_config)
        result["created"] = self.created.isoformat()
        result["docker_version"] = from_str(self.docker_version)
        result["history"] = from_list(lambda x: x, self.history)
        result["os"] = from_str(self.os)
        result["rootfs"] = to_class(Rootfs, self.rootfs)
        return result
