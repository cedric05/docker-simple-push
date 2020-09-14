import re
from pprint import pprint

import requests

import dockerfile

from .config import Config
from .exceptions import *
from .layer import Manifest
from .layergen import *


def url_append(*args):
    return "/".join(args)


def push(from_image, to_image, registry='http://localhost:5000/'):
    """generates docker image and pushes to registry 

    Parameters
    ----------
    from_image string
        from_image is identifier of docker image
    to_image string
        Docker image identifier 
    registry string
        Docker registry url
    """
    # TODO handle authenticated requests, docker.io/registry.gitlab.com will not allow without jwt
    session = requests.session()
    repo_name, repo_tag = from_image.split("/")
    manifest_url = url_append(registry, "v2", repo_name, "manifests", repo_tag)
    manifest_res = session.get(
        manifest_url,
        headers={
            'Accept': "application/vnd.docker.distribution.manifest.v2+json"
        })
    mani: Manifest = Manifest.from_dict(manifest_res.json())
    config_layer = mani.config
    config_blob = config_layer.digest

    config_url = url_append(registry, "v2", repo_name, "blobs", config_blob)
    config_resp = session.get(config_url)
    config = Config.from_dict(config_resp.json())
    pprint(mani.layers)
    for layer in config.rootfs.diff_ids:
        pprint(layer)


"""
    Download manifest
    generate tar file,
    rebuild config file
    push layer by mounting image from other image
    push one or more generated layer
    push generaged config
    push image manifest,
    push image manifest with multiple tags
"""

arg_regex = re.compile(r'\${.*?\}')


def _substitute(original, argdict):
    """

    """
    rep = original
    for match in arg_regex.finditer(original):
        arg = match.group()[2:-1]
        if arg not in argdict:
            raise ArgNotDefined(f"{arg} not defined")
        rep.replace(match.group(), argdict.get(arg))
    return rep


def planner(filename):
    """generates a plan. which will be executed at later point.

    Parameters
    ---------
    filename: string
        Dockerfile name 
    """
    config = Config()
    commands = dockerfile.parse_file(filename)
    argdict = dict()
    from_image = ""
    from_tag = "latest"
    for command in commands:
        value = command.value
        original = command.original
        cmd = command.cmd
        if cmd == 'arg':
            # ARG command only accepts single argument
            value = command.value[0]
            name, value = value.split("=")
            # TODO arg replace arg with value its set
            argdict.update(name, value)
        elif cmd == 'from':
            rep = _substitute(original, argdict)
            command = dockefile.parse_string(rep)
            value = command.value
            if len(value) > 1:
                # multi build
                # TODO handle multi build
                # do we need to?
                # for example `from python:3 as base`
                pass
            else:
                sp = rep.split(":")
                if len(sp) != 2:
                    raise SimplePushException("from should only have one tag")
                elif len(sp) > 2:
                    from_tag = sp[1]
                    from_image = sp[0]
                else:
                    from_image = rep
            # TODO get config form registry
        elif cmd == "run":
            raise SimplePushException("will not handle run command")
        elif cmd == "workdir":
            # workdir expects single argument
            config.working_dir = value[0]
        elif cmd == "copy" or cmd == "add":
            # TODO generate layer and add layer to manifest
            pass
        elif cmd == 'env':
            # refer https://docs.docker.com/engine/reference/builder/#env
            # two forms

            # first form
            if len(value) > 1:
                env_key = value[0]
                env_value = " ".join(value[1:])
                # TODO instead of appending, it should be maintained as dictionary
                # and update
                config.config.append(f"{env_key}={env_value}")
            else:

                if "=" not in original:
                    raise SimplePushException(
                        "syntax error at {cmd.start_line}. check https://docs.docker.com/engine/reference/builder/#env"
                    )
                # second form (already desired form)
                # just add to config
                config.config.append(value)
        elif cmd == "entrypoint":
            ## entrypoint will not be updated
            if config.config.entrypoint is None:
                config.config.entrypoint = value
        elif cmd == "label":
            # annotations
            # TODO fill it up later
            pass
        elif cmd == "cmd":
            config.config.cmd = value
        elif cmd == "expose":
            config.config.exposed_ports.update({port: {} for port in value})
        elif cmd == "volume":
            config.config.volumes.update({volume: {} for volume in value})
        elif cmd == "user":
            config.config.user = value[0]
        elif cmd == "onbuild":
            ## will not be used
            # TODO did not find any info on image spec
            # ignoring for now
            config.config.on_build = value[0]
        elif cmd == "stopsignal":
            config.config.stopsignal = value[0]
        elif cmd == "shell":
            # ignoring now
            # TODO
            pass
