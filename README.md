Python script to monitor SFTP connections
=========================================

Python script used to test the connection by runnning (listdir, get, put) for a given site to proactively monitor for any connection or timed out issues.

### **Versions:** Python 3.x

```
├── README.md
├── test_sftp.log
├── site.ini
└── test_sftp.py
```
**test_sftp.py** - Python script for performing the checks

**site.ini** - Details on sites to be monitored

**test_sftp.log** - File contiaining logs of the current execution (will be overwritten on each run)

## Command
```
 python test_sftp.py
```

## Sample Log File

```
 # cat test_sftp.log
19-Oct-22 14:32:29 - Connected (version 2.0, client srtSSHServer_19.00)
19-Oct-22 14:32:30 - Authentication (password) successful!
19-Oct-22 14:32:30 - Connection successfully established...
19-Oct-22 14:32:30 - [chan 0] Opened sftp connection (server version 3)
19-Oct-22 14:32:30 - Listing directory for sftptest user (before deleting testfile): ['sftptestfile']
19-Oct-22 14:32:30 - Cleaning testfile.
19-Oct-22 14:32:30 - Listing directory for sftptest user (after placing testfile): ['sftptestfile']
19-Oct-22 14:32:30 - [chan 0] sftp session closed
```


```
# cat test_sftp.log
19-Oct-22 14:37:50 - ConnectionException: ('sftp.test.net', 22)
```

```
# cat test_sftp.log
19-Oct-22 14:38:42 - KeyError: 'username'
```





