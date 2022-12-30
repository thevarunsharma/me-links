# `me-links`: Local URL shortcuts

A local application service similar to the popular **"go"** links. But unlike the actual go-links, me-links run and save the shortcuts locally. No need to host a public database or web server, this service can be configured to launch at startup and be accessed with the "me/" path.

Such shortcuts can come in handy to quickly navigate to desired websites and paths from the browser itself. This comes with a portal to view, add, delete, search and edit the shorcut and link pairs.

## Setup and Configuration
### 1. Install Dependencies
#### Python Dependencies
- First, make sure you've Python3 installed. If not, run the following on Debian/Ubuntu
```
$ sudo apt-get install python3
```
- Install packages
```
$ python3 -m pip install -r requirements.txt
```

#### Apache2
- Install Apache2 HTTP Server
```
sudo apt install apache2
```

#### Supervisord (optional)
This is needed if you want the me-links server to launch automatically as a daemon on boot/reboot. Follow the [steps here](http://supervisord.org/installing.html#)

### 2. Start the Python server
Navigate to the project source directory and start the Python Flask application using gunicorn
```
$ cd /home/varun/Projects/me-links
$ /usr/bin/gunicorn -b localhost:5000 webapp:app
```
This will start a Python application server on `localhost:5000`

### 3. Add local DNS hostname override
For you to access the me-links application using **me** or **me.links** domain names, these overriden in `/etc/hosts`. Add these using the following command, if not already present.
```
$ sudo sh -c 'echo "127.0.0.1\tme me.links" >> /etc/hosts'
```

### 4. Setup Apache Reverse Proxy
Add the following configuration stub to your apache default configuration file (`000-default.conf`) under `/etc/apache2/sites-enabled/` or `/etc/apache2/sites-available`:
```
<VirtualHost *:80>
    ServerName me.links
    ServerAlias www.me.links
    
    ProxyPreserveHost on
    ProxyPass /static/ http://localhost:5000/static/
    ProxyPass / http://localhost:5000/portal/

</VirtualHost>

<VirtualHost *:80>
    ServerName me
    
    ProxyPreserveHost on
    ProxyPass / http://localhost:5000/redirect/

</VirtualHost>
```
After this restart the apache2 server using systemctl
```
$ sudo systemctl restart apache2.service
```
This will proxy the requests on `me.links` and `www.me.links` hosts to me-links portal path, and those to `me` hosts to me-links redirect path.

### 5. Setup supervisord (optional)
This is neede to auto-launch the me-links Python server on boot/reboot.
Add the following stub at the end of supervisord config file `supervisord.conf`. Replace `<PATH_TO_PROJECT>` with the path to me-links project root.
```
[program:me_links]
command=/usr/bin/gunicorn -b localhost:5000 webapp:app
directory=<PATH_TO_PROJECT>
autostart = true                                                                
autorestart = true
```
Example where `<PATH_TO_PROJECT> = /home/varun/Projects/me-links`:
```
[program:me_links]
command=/usr/bin/gunicorn -b localhost:5000 webapp:app
directory=/home/varun/Projects/me-links
autostart = true                                                                
autorestart = true
```
Start supervisord `me_links` daemon after updating the configs:
```
$ supervisorctl start me_links
```

After these steps the me-links server should be up and running.

## Me-Links Portal
Type `me.links/` in the browser to open the portal
![me-links-portal](setup-example/portal.png)

### Add
Use the `+` button to add a new url shortcut.
**Query enabled**
If you want to append variable arguments to the URL (possible in cases where a URL passed can be appended with a string) check the `has query` box.
For example:
| me-link shortcut     | URL Mapping | Has Query?  | Example     |
|        :----:        |    :----:   |    :----:   |:---         |
| me/gh | https://github.com/ | Yes | `me/gh thevaraunsharma` => `https://github.com/thevarunsharma` |
| me/google | https://www.google.com/search?q= | Yes | `me/google apache server` => `https://www.google.com/search?q=apache%20server` |

### Search
Type the keyword in the search bar to search the shortcut

### Delete
Use the red `Delete` button in the search results to delete a me-link

### Edit
Use the `+` button and put in the new value for an existing link to be edited.

## Using `me/` links
After all the setup is complete, simply open your browser and type `me/key` and see yourself getting redirected to the desired destination!
