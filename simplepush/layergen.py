import tarfile as tarlib
import tempfile
import os
import hashlib
import io
import gzip
from .exceptions import PathNotExists

__all__ = [
    "generage_tar_file",
]

DOCKER_HOST = "192.168.1.37:5000"
CONST = "simplepush"
BLOCK = 4096


class ShaBytesIO(io.BytesIO):
    def __init__(self, initial_bytes, filename, algo=hashlib.sha256):
        self.fileobj = open(filename, 'wb')
        self.hashobj = algo()
        super().__init__(initial_bytes)

    def write(self, b):
        self.hashobj.update(b)
        self.fileobj.write(b)

    def hash(self):
        return self.hashobj.hexdigest()

    def close(self):
        self.fileobj.close()
        return super().close()


# TODO handle chown
# --chown will be added in future
# TODO deletion of generated temporary file should be handled by caller
def generage_tar_file(from_path, to_path='/', workdir='/', contextpath="./"):
    """generates tar.gz file with the context. 

    generages one of docker layer. which will be pushed to docker image
    
    Parameters:
    ------------

    from_path: list or string
        Relative path of files/directory to be copied
    contextpath: string
        Relative/Absolute Path. 
    to_path: string
        Relative path of files/directory to be palced in the tar/rootfs file
    workdir: string or '' optional
        If specified workdir will be used as context while generating tar/rootfs file
    """

    # temp file in with tar will be generated
    tarfile = os.path.join(
        tempfile.gettempdir(),
        CONST + "_" + next(tempfile._get_candidate_names()) + ".tar")
    fileobj = ShaBytesIO(None, filename=tarfile)

    # TODO apply gzip compression
    # applying compression will save network bandwidth.
    # while image push, user needs sha256sum for both tar file and gzip
    # sha256 for tar file is used in config file.
    # sha256 for tar.gz file/blob is used for uploading blob
    
    compressed_file = tarlib.open(mode='w', fileobj=fileobj)

    for path in from_path:
        path = os.path.join(contextpath, path)
        if not os.path.exists(path):
            raise PathNotExists(f"{path} not exist. relative?")
        """

        name of file has multiple shades

        COPY file /  
        COPY file /file
        COPY file /file2
        COPY file /somedir/
        
        COPY dir /
        COPY dir /dir2
        COPY dir /some/other/

        ❌ multiple directires behaves differently
        visit https://stackoverflow.com/a/30316600
        """
        to_name = to_path
        if to_name.endswith("/"):
            archname = os.path.join(to_name, os.path.basename(path))
        else:
            archname = os.path.basename(path)
        if not os.path.isabs(to_name):
            archname = os.path.join(workdir, archname)

        # TODO add filter
        # create filter function to exclude files from .dockerignore
        compressed_file.add(path, arcname=archname)
    compressed_file.close()
    return tarfile, fileobj.hash()


def gethash(filename, lib=hashlib.sha256):
    hashobj = lib()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hashobj.update(byte_block)
    return hashobj.hexdigest()
