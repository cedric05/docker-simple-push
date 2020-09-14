import os
import sys
import tarfile
import unittest

from simplepush import PathNotExists, generage_tar_file, push


@unittest.skip
class GeneragedTest(unittest.TestCase):
    def test_raises(self):
        with self.assertRaises(PathNotExists):
            generage_tar_file(from_path=["testdata", "testdata2", "testdir"],
                              to_path="haha",
                              workdir="/",
                              contextpath="./")

    def test_2(self):
        from_path = ["testfile", "testdir"]
        filename, sha = generage_tar_file(from_path=from_path,
                                          to_path="haha",
                                          workdir="/",
                                          contextpath="./testdata/")
        print(filename, sha)
        tar = tarfile.open(filename, 'r:gz')
        names = tar.getnames()
        for path in from_path:
            if path not in names:
                raise Exception("file not included in layer")
        tar.close()

    def test_3(self):
        workdir = "/test"
        from_path = ["testfile", "testdir"]
        filename, sha = generage_tar_file(from_path=from_path,
                                          to_path="haha",
                                          workdir=workdir,
                                          contextpath="./testdata/")
        print(filename, sha)


class haha(unittest.TestCase):
    def test_run(self, ):
        push("hello/latest", "ram/latest", "http://172.17.0.3:5000")


if __name__ == "__main__":
    unittest.main()
