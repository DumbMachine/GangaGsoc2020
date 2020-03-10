This file has explanations and implementation details for many things.

## 1. Task1:

Let starts with task1. This asks us to write a ganga jobs to count the number of 'the' in a multi page pdf.

My approach for this was:

- I ran a script, `split-pdf.py`, to get all the separate pages from the multi page pdf.

- Using the `ArgSplitter` Class I split the job of counting the number of **the** to multiple subjobs.

  ```python
  # Creating a new job object
  job = Job()
  
  #specifies executable to run on Grid
  job.application = Executable()
  job.application.exe = File("count-word.sh")
  
  #specifies pagewise arguments to the executable, these are arugments are used to split the job into subjobs
  args = [["page0.pdf"],["page1.pdf"],["page2.pdf"],["page3.pdf"],["page4.pdf"],["page5.pdf"],["page6.pdf"],["page7.pdf"],["page8.pdf"],["page9.pdf"],["page10.pdf"],["page11.pdf"]]
  
  #splits the job
  splitter = ArgSplitter(args=args)
  job.outputfiles = [LocalFile("result.txt")]
  
  filelist = []
  for i in range(len(args)):
  	filename = args[i][0]
  	filelist.append(filename)
  job.application.args = filelist
  job.splitter = splitter
  job.inputfiles = filelist
  job.backend = "Local"
  
  # Using the CustomMerger to merge the 'the' counts from each subjob
  job.postprocessors = CustomMerger(module="./custom.py", files=['result.txt'])
  job.submit()
  
  ```

  

This document is still a work in progress, I will update this document with more details today.

## 2. Task2:

Now comes the turn of task2, my favorite.

This task is about finding ways:

- to store the `ganga job` object as a `blob` or `string` and 
- to retrieve `ganga job` from the `blob` or `string`
- storing and retrieving `ganga job`s from a database.

### 2.1 Converting `ganga job` to blob or string:

I have implemented 3 methods here:

	#### 2.1.1: `full_print` method:

​	Since this was mentioned in the first version of `ganga-dev/GangaGsoc2020` readme I decided implement this. 

​	The basic cycle of this method is:

- Capturing the stdout from `full_print(<job>)`. Which is done through:

  ```python
  job = jobs[jid]
  stdout = sys.stdout
  sys.stdout = io.StringIO()
  
  full_print(job)
  
  # get output and restore sys.stdout
  string_rep = sys.stdout.getvalue() # string_rep now holds the output from full_print(job)
  sys.stdout = stdout
  ```

  This representation of the job is then stored in an instance of mongodb (or postgres, if one chooses to use that):

  ```python
  db.jobs.insert({"jid": job_id, "string": string_rep})
  ```

  When the need for the particular job string arises, it can be retrieved by:

  ```python
  [item['string'].strip() for item in db.jobs.find({"jid": jid})]
  ```

  This will return the output of `full_print` for the particular job. But this isn't useful, in the real world, as AFAIK it cannot be used to make the `Ganga Job` object.

  ![image-20200309060808691](/home/needshelp/code/gsoc/GangaGSoC2020/src/Project.assets/image-20200309060808691.png)![image-20200309060756799](/home/needshelp/code/gsoc/GangaGSoC2020/src/Project.assets/image-20200309060756799.png)

	#### 2.1.2: `export/load` method:

​	This method makes use of the `export` and `load` functions from ``.../Persistency/__init__.py`. 

​		The basic cycle of this method is:

- `custom_export` function is used to export `jobs` to `string_rep`. Since `export` functions only works on file like objects, I made a Wrapper Class for string (StringWrapper) to mimic the method from file-like objects. This allowed me to use the same code as that of `export` with minimal changes.

- Once I obtain the string representation of the object, it can be easily stored in the database by supplying a unique identifier `jid` job id.

  ```python
  db.jobs.insert({"jid": jid, "string": string_rep})
  ```

- When the need requires it, the job string can be retrieved :

  ```python
  [custom_load(item['string']) for item in db.jobs.find({"jid": jid})]
  ```

- `custom_load` function is used to do the same thing `load`, while `load` works for file-like objects `custom_load` works on strings and converts the string to `Ganga Job`.

  ![image-20200309210916530](Project.assets/image-20200309210916530.png)

  This method is far superior to `full_print` as we can obtain the string representation of the jobs and convert the job string back to the job object.

	#### 2.1.3: `from_file/to_file` method:

​	The story this is also the same, I tweaked the default implementation to suit the task at hand, conversion of job to string also avoid the overhead of creation of new files.

![image-20200309205733131](Project.assets/image-20200309205733131.png)