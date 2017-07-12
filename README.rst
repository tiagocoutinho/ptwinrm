ptwinrm
=======

A Python_, prompt_toolkit_ and pywinrm_ based WinRM console:

.. image:: https://asciinema.org/a/C5wHOTBWELzNRbWFlGpuZUBUK.png
   :alt: asciinema cast
   :target: https://asciinema.org/a/C5wHOTBWELzNRbWFlGpuZUBUK?autoplay=1&speed=2&loop=1&size=medium&theme=asciinema

Installation
------------

.. code-block:: bash

    $ pip install ptwinrm


Requirements
------------

- Python_ >= 2.6
- docopt
- pywinrm
- prompt_toolkit

Usage
-----

Before connecting to the windows machine, make sure the winrm service is running and the firewall
is opened for winrm connections. On my windows machine I had to do the following on the windows
command line::

    # make firewall respect our wishes
    C:\>netsh advfirewall add rule name="WinRM-HTTP" dir=in localport=5985 protocol=TCP action=allow
    C:\>netsh advfirewall add rule name="WinRM-HTTPS" dir=in localport=5986 protocol=TCP action=allow

    # configure winrm
    C:\>winrm quickconfig

    # Allow non encrypted (for pywinrm)
    C:\>winrm set winrm/config/servive '@{AllowUnencrypted="true"}'

Then you can try to connect from another machine (linux, OSX, windows):

.. code-block:: bash

    $ ptwinrm --user="acme\roadrunner" --run="ver" acme-rr.com
    password: ********

    Microsoft Windows [Version 6.1.7601]

    $ ptwinrm --user="acme\roadrunner" acme-rr.com
   password: ********

   C:\Users\roadrunner>dir
    Volume in drive C is System
    Volume Serial Number is 8C20-216F

    Directory of C:\Users\roadrunner

   20/04/2017  09:29    <DIR>          .
   20/04/2017  09:29    <DIR>          ..
   05/07/2017  10:58    <DIR>          Contacts
   05/07/2017  10:58    <DIR>          Desktop
   03/05/2016  11:10    <DIR>          Documents
   06/07/2017  11:04    <DIR>          Downloads
   05/07/2017  10:58    <DIR>          Favorites
   05/07/2017  10:58    <DIR>          Links
   28/06/2017  08:18    <DIR>          Mails
   05/07/2017  10:58    <DIR>          Music
   05/07/2017  10:58    <DIR>          Pictures
   05/07/2017  10:58    <DIR>          Saved Games
   05/07/2017  10:58    <DIR>          Searches
   06/03/2013  15:09    <DIR>          Tracing
   05/07/2017  10:58    <DIR>          Videos

   C:\Users\roadrunner> ipconfig /all
   Windows IP Configuration

      Host Name . . . . . . . . . . . . : ACME-RR
      Primary Dns Suffix  . . . . . . . : acme.com
      Node Type . . . . . . . . . . . . : Hybrid
      IP Routing Enabled. . . . . . . . : No
      WINS Proxy Enabled. . . . . . . . : No
      DNS Suffix Search List. . . . . . : acme.com

   Ethernet adapter Local Area Connection 2:

      Media State . . . . . . . . . . . : Media disconnected
      Connection-specific DNS Suffix  . :
      Description . . . . . . . . . . . : Intel(R) Gigabit CT Desktop Adapter
      Physical Address. . . . . . . . . : 55-44-33-22-11-00
      DHCP Enabled. . . . . . . . . . . : No
      Autoconfiguration Enabled . . . . : Yes

   Ethernet adapter Local Area Connection:

      Connection-specific DNS Suffix  . : acme.com
      Description . . . . . . . . . . . : Acme(R) Gigabit Network Connection
      Physical Address. . . . . . . . . : 00-11-22-33-44-55
      DHCP Enabled. . . . . . . . . . . : Yes
      Autoconfiguration Enabled . . . . : Yes
      IPv4 Address. . . . . . . . . . . : 199.199.1.172(Preferred)
      Subnet Mask . . . . . . . . . . . : 255.255.254.0
      Lease Obtained. . . . . . . . . . : quarta-feira 5 julho 2017 10:41:49
      Lease Expires . . . . . . . . . . : quarta-feira 3 janeiro 2018 22:42:05
      Default Gateway . . . . . . . . . : 199.199.1.1
      DHCP Server . . . . . . . . . . . : 198.198.60.11
      DNS Servers . . . . . . . . . . . : 198.198.208.9
                                          198.198.209.9
      NetBIOS over Tcpip. . . . . . . . : Enabled

   Tunnel adapter isatap.acme.com:

      Media State . . . . . . . . . . . : Media disconnected
      Connection-specific DNS Suffix  . : acme.com
      Description . . . . . . . . . . . : Microsoft ISATAP Adapter
      Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
      DHCP Enabled. . . . . . . . . . . : No
      Autoconfiguration Enabled . . . . : Yes

   Tunnel adapter Local Area Connection* 11:

      Media State . . . . . . . . . . . : Media disconnected
      Connection-specific DNS Suffix  . :
      Description . . . . . . . . . . . : Teredo Tunneling Pseudo-Interface
      Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
      DHCP Enabled. . . . . . . . . . . : No
      Autoconfiguration Enabled . . . . : Yes

   Tunnel adapter isatap.{FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF}:

      Media State . . . . . . . . . . . : Media disconnected
      Connection-specific DNS Suffix  . :
      Description . . . . . . . . . . . : Microsoft ISATAP Adapter #4
      Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
      DHCP Enabled. . . . . . . . . . . : No
      Autoconfiguration Enabled . . . . : Yes

   C:\Users\roadrunner>


**That's all folks!**


.. _Python: http://www.python.org/
.. _pywinrm: http://www.github.com/diyan/pywinrm/
.. _prompt_toolkit: http://www.github.com/jonathanslenders/python-prompt-toolkit/
