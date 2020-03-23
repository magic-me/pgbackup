import tempfile, pytest

from pgbackup import storage

@pytest.fixture()
def infile():
    f = tempfile.TemporaryFile('w+b')
    f.write(b'Testing')
    f.seek(0)


def test_storing_file_locally(infile):
    """
    Writes content from one file-like to another
    """
    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile,outfile)
    with open(outfile.name,'rb') as f:
        assert f.read() == b'Testing'

def test_storing_file_os_aws_s3(mocker,infile):
    """
    Writes content from one file-line to S3
    """
    client = mocker.Mock()

    storage.s3(client, infile, "bucket", "file-name")

    client.ipload_fileobj.assert_called_with(infile, "bucket", "file-name")
