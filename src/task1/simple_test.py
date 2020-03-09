import unittest

class SimpleTest(unittest.TestCase): 
    def test_job(self):
        import ganga
        from GangaCore.GPIDev.Lib.Job import Job
        from GangaCore.GPIDev.Lib.File import File 
        from GangaCore.GPIDev.Lib.File import LocalFile
        from GangaCore.Lib.Mergers.Merger import CustomMerger

        # from GangaCore.GPI import Job, Executable, Local, File, LocalFile


        j = Job()
        print(j.status)
        j.submit()

        assert True

if __name__ == '__main__':
    unittest.main()