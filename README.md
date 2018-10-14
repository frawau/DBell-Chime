# DBell-Chime

Simple Python program that can be used to react to DBell Live and play a sound file.

## Genesis

So I bought a [DBell Live Doorbell](https://www.dbell.ca/) during their
[Indiegogo campaign](https://www.indiegogo.com/projects/dbell-live-smartest-video-doorbell-security-cam#/).

The project delivered, which is good.

Using the product, I found out a number of issues:

    The ONVIF implementation is crappy.  There is a PTZ profile, but the camera
    does not support that, the city location is Toronto and cannot be changed, ...

    It ridiculously easy to get telnet access to the device. (You do need to have
    user name and password for the Web interface)

    The doorbell opens port 81 on your firewall using UPnP

    The doorbell communicates with Amazon, probably the DBell Canada cloud service.

    The doorbell communicates with Alibaba

    The doorbell tries to communicate with www.baidu.com

    The doorbell uses some hardcoded DNS server addresses in China, as well as Google's

So, it may be advertised as Canadian, but this thing seems more like a Chinese mole trying to
report back to its Chinese master.

So I blocked the Internet access of the doorbell. I lost the remote access feature of the application,
but I felt it was safer that way.

Then the chime blew up. Since I could only get the Android app on my tablet to vibrate when someone was
rigging the bell, the doorbell was now, essentially, a pricey useless device.

I contacted them with 2 questions:

    What can I do about the chime?

    How can I detect the button has been pressed on my LAN?

They offered to send my a new chime, I would only have to pay for the shipping (around USD30). Nice of you, thank you.

To my second question, they replied by talking about video codecs. Obviously, they did not want to talk about it and were trying to
throw jargon at me. When I pointed out that they were either thinking I was an idiot, or were, themselves, idiots or deceptives, they whined
that I was calling them idiots.

So I decided I wanted nothing more to do with those idiots.

## Finding a way

At first I though about reverse engineering their protocol. I used Wireshark, with tcpdump running on my router,
as well as tcpdump on my Android device.

I could not find anything. I can see a few UDP packets being sent by the device, but could not make sense of them.

Since the device can use SMTP and FTP, I figured I could use one of them for my purpose.

Their SMTP implementation is pretty crappy, no surprise here, so I was not able to send email to my local email server.
The reason being that they always send "AUTH LOGIN" even when you set up the device to not login.

That is when I decided, I was going to provided a minimalist server that the doorbell would contact.

I am pretty sure it would work similarly with FTP.

## How to use

On the DBell Live device, you must enable "Sending Email on Alarm". You can use the Web Interface or the phone app for that.

On the DBell you have to set up the "Mail Service Settings" as follow:

    Sender:      dbell@something.com
    SMTP Server: The IP address where dbellchime runs
    SMTP Port:   The port used by dbellchime
    SSL:         None
    Receiver 1:  a@b.com    or whatever

Inside dbellchime.py, you must set:

    RING        path to your sound file
    BELLADDR    IP address of the doorbell
    MYADDR      The IP address where dbellchime runs. Same as SMTP Server on doorbell
    PORT        The port on which to listen, must be the same as SMTP Port on doorbell
    CMD         The shell command to run when the doorbell contacts you.
    DELAY       The minimum length of time between rings (in secs).

That's it.

If you have multiple doorbells, supporting multiple doorbells with separate rings is trivial and left as an exercise to the reader.

## My setup

I run this on a Raspberry Pi 3. It is started in a @boot cronjob into a tmux instance. When someone rings,
it play an except of "Let 'Em In" by McCartney with ogg123

## Peroration

To get telnet access to the DBell Live. got to the FTP setting. Do:

    FTP Server        $(killall -TERM telnetd)
    FTP Port          21
    User              $(/usr/sbin/telnetd -l /bin/sh)
    Password          12345678

Apply and connect. This was published by someone else on the DBell forum. They deleted it after whining
about it.


