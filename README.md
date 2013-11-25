This is a skeletal ZenPack which logs "Hello World!" to the event.log file.

Installation instructions:

1) tail -f /opt/zenoss/log/event.log
2) As the zenoss user (sudo bash ; su - zenoss) install the ZenPack (on eyes-02)
   zenpack --install /clone_location/ZenPacks.EE.HelloWorld/dist/ZenPacks.EE.HelloWorld-0.0.4-py2.7.egg

   You should see the following:
<pre>
INFO:zen.ZenPackCMD:installing zenpack ZenPacks.EE.HelloWorld; launching process
2013-11-25 10:45:43,459 INFO zen.ZPLoader: Loading /opt/zenoss/ZenPacks/ZenPacks.EE.HelloWorld-0.0.4-py2.7.egg/ZenPacks/EE/HelloWorld/objects/objects.xml
2013-11-25 10:45:43,460 INFO zen.AddToPack: End loading objects
2013-11-25 10:45:43,460 INFO zen.AddToPack: Processing links
2013-11-25 10:45:43,491 INFO zen.AddToPack: Loaded 0 objects into the ZODB database
2013-11-25 10:45:43,523 INFO zen.HookReportLoader: Loading reports from /opt/zenoss/ZenPacks/ZenPacks.EE.HelloWorld-0.0.4-py2.7.egg/ZenPacks/EE/HelloWorld/reports
2013-11-25 10:45:43,609 INFO zen.ZenPacks.EE.HelloWorld: Adding ZenPacks.EE.HelloWorld relationships to existing devices
</pre>

3) restart Zope
   zopectl restart 

4) You will see something like this in the event.log file:
   "2013-11-25T10:46:04 INFO zen.ZenPacks.EE.HelloWorld Hello World!"

5) The code for this Hello World is located in the 
   ZenPacks.EE.HelloWorld/ZenPacks/EE/HelloWorld/"__init__.py" file

   # Test Logging
   LOG.info('Hello World!\n')

That's it.

To create an egg file issue the following command in the top level directory of 
the ZenPack:

python2.7 setup.py bdist_egg

Now you can start back up at step 1) above. :)

I have this alias in my .bash_aliases:

alias eggman='python2.7 setup.py bdist_egg'

