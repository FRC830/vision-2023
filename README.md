# vision-2023

Setting up vision on raspberry pi requires a static ip. To set up a static ip on your device, 

go to you wifi settings

click on ethernet or what ever stuff you are connecting the pi with

change the advance option to the following stuff. 

ip `192.168.8.1`

subnet mask `255.255.255.0` OR `/24`

gateway `192.168.8.30`

once you've done that, try `ping 192.168.8.30`

if it returned stuff that's not some thign `timed out` 

you've succeded. Move on with this command `ssh pi@192.168.8.30` 

and password is `raspberry`
