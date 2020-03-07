from GangaCore.Core.GangaRepository.VStreamer import to_file, from_file
from GangaCore.GPIDev.Base.Proxy import addProxy, stripProxy

jid = -1
job = stripProxy(jobs[jid])

import io
import sys
stdout = sys.stdout
sys.stdout = io.StringIO()

to_file(job)

# get output and restore sys.stdout
string_rep = sys.stdout.getvalue()
sys.stdout = stdout

class StringJob:
    def __init__(self, string_rep):
        self.string_rep = string_rep

    def read(self):
        return self.string_rep.strip()