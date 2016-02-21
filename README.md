#hostnames provider

An app to provide hostnames to hosts in a network, designed to work with inventory solutions like FusionInventory or OCSInventory that requires hosts to have distinct hostnames in a network.

It's simply a django app designed with a Host model containing three fields:

```python
class Host(models.Model):
    hostname = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17)
    ip_address = models.TextField(unique=True)
    def __str__(self):
        return self.hostname+'|'+self.mac_address+'|'+self.ip_address
```

The hosts are imported to the app through the script feeder.py, which reads csv files containing the hosts specifications.

Example of a hosts.csv file:

```csv
ap-1|00:1d:7e:39:cb:82|172.16.0.2
ap-2|00:1d:7e:39:cb:4f|172.16.0.3
ap-3|00:1d:7e:39:ac:e9|172.16.0.4
```

## Clients operation

Actually, there are two scripts: change_linux_hostname.sh and change_windows_hostname.bat.

Both of them cURL hostnames_provider URL and then, compares the client actual hostname to its final hostname (provided by hostnames_provider). If the comparison is false, the script changes the host hostname and then restarts the machine.

In a computer science lab, it's a great help to sysadmins, since a sysadmin won't need to go computer by computer changing it's hostname manually.

## Future implementations

-Adapt hostnames_provider to work with REST, allowing a host to get its hostname by his mac_address
-Adapt hostnames_provider to work with turica's rows (https://github.com/turicas/rows)
-Create a web interface to manage hosts, allowing file upload of hosts files (csv, xls, xlsx, etc)

## Further infos

This software is being developed at CEFET-MG. Any doubts, please don't hesitate to contact me:

dascaniosantos@gmail.com
