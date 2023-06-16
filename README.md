# CMDB

Python utility for working with ServiceNow CMDB.
Just provides an interface to perform CRUD actions, like importing hosts from Ansible.

### Installation
Clone the repo. Activate the virtualenv and run pip install.

### Instructions

Run:
```
python cmdb.py <arg>
```

The ServiceNow instance connection details are taken from Linux environment variables. You should add your own details to the .env file and run

```
source .env
```

Should be able to do most actions with cli arguments.
Currently there's the following:

```
--output <hostname>
--output-all
--add
--update
--delete <hostname>
--delete-all
```

output and output-all dump out the host contents from SN. Output requires the hostname as an addition argument, output-all just dumps everything.
Add and update require an 'out' folder to be present and contain Ansible host files in JSON format. These can be generated from Ansible using:

```
ansible -i inventory all -m setup --tree out/
```

These arguments will read all Ansible hostfiles in the 'out' folder and either add hosts to the CMDB if they don't already exist, or update hosts if they do. Update checks for a 'sys_id' first from ServiceNow.

Delete and delete-all are obvious. Delete needs the hostname as an extra argument. Delete-all doesn't, it just deletes everything in the CMDB.
