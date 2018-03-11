# Raspi_Sysinfo_oled_display
Display your raspi's sysinfo on little LLC oled monitor

![](https://github.com/EricHerilan/Raspi_Sysinfo_oled_display/raw/master/img/IMG_20180311_214125.jpg)

First of all
----

we need `Luma` to drive our devise, To get them from here [luma.oled](https://github.com/rm-hull/luma.oled) <br>
or <br>

    $ sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg-dev
    $ sudo -H pip install --upgrade pip 
    $ sudo apt-get purge python-pip 
    $ sudo -H pip install --upgrade luma.oled

Run as boots
----

Add a `.service` file in /etc/systemd/system/ like `oled.service` <br>
edit with any tool you like

    [Unit]
    Description=oled autostart
    [Service]
    Type=idle
    ExecStart=/usr/bin/python /home/sysinfo_display.py
    Restart=always
    [Install]
    WantedBy=multi-user.target

remember to change `/home/sysinfo_display.py` as your download place<br>
then <br>

    sudo systemctl daemon-reload
    sudo systemctl start oled
    sudo systemctl enable oled

End
===

准备
----

需要Luma模块作为oled的驱动：[luma.oled](https://github.com/rm-hull/luma.oled) <br>
当然也可以直接安装 <br>

    $ sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg-dev
    $ sudo -H pip install --upgrade pip 
    $ sudo apt-get purge python-pip 
    $ sudo -H pip install --upgrade luma.oled

设置开机启动
------

通过systemclt
新建 `.service` 文件于 /etc/systemd/system/ 比如 `oled.service` <br>
然后用nano vi随便哪个工具修改

    [Unit]
    Description=oled autostart
    [Service]
    Type=idle
    ExecStart=/usr/bin/python /home/sysinfo_display.py
    Restart=always
    [Install]
    WantedBy=multi-user.target

记得更改 `/home/sysinfo_display.py` 到你源码下载目录<br>
然后 <br>

    sudo systemctl daemon-reload
    sudo systemctl start oled
    sudo systemctl enable oled

完
===
