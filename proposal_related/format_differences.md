### This document will try to outline the differences in the way, the currently implemented methods

-------

# Native export/load method:

This method makes of the functions:
   - `export`: https://github.com/ganga-devs/ganga/blob/80bc4d9a6b5cb45bd72647236a782808bb4364e2/ganga/GangaCore/GPIDev/Persistency/__init__.py#L35
- `load`: https://github.com/ganga-devs/ganga/blob/80bc4d9a6b5cb45bd72647236a782808bb4364e2/ganga/GangaCore/GPIDev/Persistency/__init__.py#L154

An example of the file created this method is:

```
#Ganga# File created by Ganga - Mon Mar  9 02:04:44 2020
#Ganga#
#Ganga# Object properties may be freely edited before reloading into Ganga
#Ganga#
#Ganga# Lines beginning #Ganga# are used to divide object definitions,
#Ganga# and must not be deleted

#Ganga# Job object (category: jobs)
 Job (
   comment = '',
   name = '',
   do_auto_resubmit = False,
   parallel_submit = True,
   inputsandbox =[],
   info =   JobInfo (
     monitor =None
   ),
   application =   Executable (
     exe = File(name='count-word.sh',subdir='.'),
     args = ['page0.pdf', 'page1.pdf', 'page2.pdf', 'page3.pdf', 'page4.pdf', 'page5.pdf', 'page6.pdf', 'page7.pdf', 'page8.pdf', 'page9.pdf', 'page10.pdf', 'page11.pdf'],
     env = {},
     platform = 'ANY',
     is_prepared = ShareDir(name='conf-779aac10-966e-47aa-8b59-5455e98dc9da',subdir='.'),
     hash = '3ee875b5e35c98a78ffdc9b49f0bfd05'
   ),
   backend =   Local (
     nice = 0,
     force_parallel = False
   ),
   inputfiles =[    
     LocalFile (
       namePattern = 'page0.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page1.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page2.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page3.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page4.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page5.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page6.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page7.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page8.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page9.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page10.pdf',
       localDir = '',
       compressed = False
     ),    
     LocalFile (
       namePattern = 'page11.pdf',
       localDir = '',
       compressed = False
     ),],
   outputfiles =[    
     LocalFile (
       namePattern = 'result.txt',
       localDir = '',
       compressed = False
     ),],
   inputdata =None,
   splitter =   ArgSplitter (
     args = [['page0.pdf'], ['page1.pdf'], ['page2.pdf'], ['page3.pdf'], ['page4.pdf'], ['page5.pdf'], ['page6.pdf'], ['page7.pdf'], ['page8.pdf'], ['page9.pdf'], ['page10.pdf'], ['page11.pdf']]
   ),
   postprocessors =   MultiPostProcessor (
   ),
   virtualization =None
 )
```

The advantages of this method are that:

- This representation of `Job` makes it very easy for a user to understand.

- This representation of `Job` takes up lesser space when compared to `xml`'s.

  ![image-20200319133646700](image-20200319133646700.png)

The disadvantage of this method is that:

-  It is very slow. On average this method took `0.029319047927856445 seconds` to convert to ganga job from Qualification Task 2. This is nearly 200% more than that taken by `xml method`.

# XML (to_file/from_file) method:

This method makes of the functions:

   - `export`: https://github.com/ganga-devs/ganga/blob/d057b9e9f7fce0713190b4597c7e7ef8580608e3/ganga/GangaCore/Core/GangaRepository/VStreamer.py#L59
- `load`: https://github.com/ganga-devs/ganga/blob/d057b9e9f7fce0713190b4597c7e7ef8580608e3/ganga/GangaCore/Core/GangaRepository/VStreamer.py#L93

An example of the file created this method is:

```
<root>
 <class name="Job" version="1.6" category="jobs">
    <attribute name="outputsandbox"> 
       <sequence>
       </sequence>
    </attribute>
    <attribute name="comment"> 
        <value>''</value>
    </attribute>
    <attribute name="id"> 
        <value>13</value>
    </attribute>
    <attribute name="status"> 
        <value>'new'</value>
    </attribute>
    <attribute name="name"> 
        <value>''</value>
    </attribute>
    <attribute name="do_auto_resubmit"> 
        <value>False</value>
    </attribute>
    <attribute name="inputsandbox">
       <sequence>
       </sequence>
    </attribute>
    <attribute name="info">
          <class name="JobInfo" version="0.1" category="jobinfos">
             <attribute name="submit_counter"> 
                 <value>0</value>
             </attribute>
             <attribute name="uuid"> 
                 <value>''</value>
             </attribute>
             <attribute name="monitoring_links"> 
                <sequence>
                </sequence>
             </attribute>
             <attribute name="monitor">
                <value>None</value>
             </attribute>
          </class>
    </attribute>
    <attribute name="time">
          <class name="JobTime" version="0.0" category="jobtime">
             <attribute name="timestamps"> 
                 <value>{'new': datetime.datetime(2020, 3, 18, 22, 53, 3, 24114)}</value>
             </attribute>
          </class>
    </attribute>
    <attribute name="application">
          <class name="Executable" version="2.0" category="applications">
             <attribute name="exe"> 
                 <value>'echo'</value>
             </attribute>
             <attribute name="args"> 
                <sequence>
                   <value>'Hello World'</value>
                </sequence>
             </attribute>
             <attribute name="env"> 
                 <value>{}</value>
             </attribute>
             <attribute name="platform"> 
                 <value>'ANY'</value>
             </attribute>
             <attribute name="is_prepared"> 
                 <value>None</value>
             </attribute>
             <attribute name="hash"> 
                 <value>None</value>
             </attribute>
          </class>
    </attribute>
    <attribute name="backend">
          <class name="Local" version="1.2" category="backends">
             <attribute name="id"> 
                 <value>-1</value>
             </attribute>
             <attribute name="status"> 
                 <value>None</value>
             </attribute>
             <attribute name="exitcode"> 
                 <value>None</value>
             </attribute>
             <attribute name="workdir"> 
                 <value>''</value>
             </attribute>
             <attribute name="actualCE"> 
                 <value>''</value>
             </attribute>
             <attribute name="wrapper_pid"> 
                 <value>-1</value>
             </attribute>
             <attribute name="nice"> 
                 <value>0</value>
             </attribute>
             <attribute name="force_parallel"> 
                 <value>False</value>
             </attribute>
          </class>
    </attribute>
    <attribute name="inputfiles">
       <sequence>
       </sequence>
    </attribute>
    <attribute name="outputfiles">
       <sequence>
       </sequence>
    </attribute>
    <attribute name="non_copyable_outputfiles">
       <sequence>
       </sequence>
    </attribute>
    <attribute name="inputdata">
       <value>None</value>
    </attribute>
    <attribute name="outputdata">
       <value>None</value>
    </attribute>
    <attribute name="splitter">
       <value>None</value>
    </attribute>
    <attribute name="subjobs">
       <sequence>
       </sequence>
    </attribute>
    <attribute name="postprocessors">
          <class name="MultiPostProcessor" version="1.0" category="postprocessor">
             <attribute name="process_objects">
                <sequence>
                </sequence>
             </attribute>
          </class>
    </attribute>
    <attribute name="virtualization">
       <value>None</value>
    </attribute>
    <attribute name="merger">
       <value>None</value>
    </attribute>
    <attribute name="metadata">
          <class name="MetadataDict" version="1.0" category="metadata">
             <attribute name="data"> 
                 <value>{}</value>
             </attribute>
          </class>
    </attribute>
 </class>
</root>
```

The advantages of this method are that:

- This representation of `Job` allows for really fast conversion to/from `Job` object. On average this method took `0.00010609626770019531 seconds` to convert to ganga job from Qualification Task 2.

The disadvantage of this method is that:

- This method doesn't produce a job representation that is easily ingestible by human.

- This method takes up alot of space on local stage. 

  ![image-20200319140746060](image-20200319140746060.png)

# Json method:

This method aims to use the best of both worlds:

- `json` allows storing of `jobs` in a way which allows human to understand better and if needed use in external applications.

- `json` objects by default take up less space than `xml` documents and also have great compressibility. Database 's have inbuilt compression which will beneficial here. 

  ![image-20200319140803510](image-20200319140803510.png)

- `json` representation will allow users to search for ganga jobs from the repository by making use of `schema` fields. Consider the following example:

  ```python
  >>> jobs.search({
      "name": "CaculusSolverROOT",
      "comment": "additional fields can use to match objects"
  })
  ```

  This will request for jobs that have the matching fields in their `schema` can easily served by directly searching in the database with the required fields:

  ```python
  >>> db.jobs.find({ # db is a mongo database and job is the document name
      "name": "CaculusSolverROOT",
      "comment": "additional fields can use to match objects"
  })
  
  
  ```

  

  

  An example of file created by the proposed method is :

```json
# job.json
{
    "outputsandbox": [],
    "comment": "",
    "id": 8,
    "status": "",
    "name": "",
    "inputdir": "/home/needshelp/gangadir/workspace/needshelp/LocalXML/8/input/",
    "outputdir": "/home/needshelp/gangadir/workspace/needshelp/LocalXML/8/output/",
    "do_auto_resubmit": "False",
    "parallel_submit": "True",
    "inputsandbox": [],
    "info": {
        "submit_counter": 0,
        "uuid": "",
        "monitoring_links": [],
        "monitor": "None"
    },
    "time": {
        "new": "2020/03/18 07:53:55",
        "backend_running": "2020/03/18 07:53:58",
        "running": "2020/03/18 07:53:58",
        "submitted": "2020/03/18 07:53:58",
        "submitting": "2020/03/18 07:53:58"
    },
    "application": {
        "exe": {
            "name": "count-word.sh",
            "subdir": "."
        },
        "args": [
            "page0.pdf",
            "page1.pdf",
            "page2.pdf",
            "page3.pdf",
            "page4.pdf",
            "page5.pdf",
            "page6.pdf",
            "page7.pdf",
            "page8.pdf",
            "page9.pdf",
            "page10.pdf",
            "page11.pdf"
        ],
        "env": "{}",
        "platform": "ANY",
        "is_prepared": {
            "name": "conf-e5d9209c-0775-453c-a73d-fabc213b1885",
            "subdir": ".",
            "associated_files": {
                "_list": [],
                "_is_preparable": "False"
            }
        },
        "hash": "3ee875b5e35c98a78ffdc9b49f0bfd05"
    },
    "backend": {
        "id": -1,
        "exitcode": "None",
        "workdir": "",
        "actualCE": "",
        "nice": 0,
        "wrapper_pid": -1,
        "force_parallel": "False"
    },
    "inputfiles": [
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page0.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page1.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page2.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page3.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page4.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page5.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page6.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page7.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page8.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page9.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page10.pdf"
        },
        {
            "localDir": "",
            "subfiles": "",
            "compressed": "False",
            "namePattern": "page11.pdf"
        }
    ],
    "outputfiles": {
        "localDir": "",
        "subfiles": "",
        "compressed": "False",
        "namePattern": "result.txt"
    },
    "non_copyable_outputfiles": "",
    "inputdata": "None",
    "outputdata": "None",
    "splitter": {
        "args": [
            {
                "_list": "page0.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page1.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page2.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page3.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page4.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page5.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page6.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page7.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page8.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page9.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page10.pdf",
                "_is_preparable": "False"
            },
            {
                "_list": "page11.pdf",
                "_is_preparable": "False"
            }
        ]
    },
    "subjobs": "Registry Slice: jobs(8).subjobs (0 objects)",
    "postprocessors": [
        "MultiPostProcessor" # GangaCore.GPIDev.Adapters.IPostProcessor.MultiPostProcessor object at 0x7f7ca843a590
    ],
    "virtualization": "None",
    "metadata": {}
}
```

