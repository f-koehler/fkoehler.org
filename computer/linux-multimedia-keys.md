---
title: Multimedia keys for Linux using xbindkeys
created: 2015-06-04-15-52
updated: 2015-06-04-15-52
abstract: xbindkeys offers an easy way to get multimedia keys to work in the way you want them work.
keywords: linux xbindkeys playerctl alsa multimedia key
---

[xbindkeys](http://www.nongnu.org/xbindkeys/xbindkeys.html) offers a way to run custom commands on key press. If you combine it with tools like amixer and [playerctl](https://github.com/acrisci/playerctl) you can use your keyboard to change volume and to control video/audio players. The setup is very easy and straightforward.

To get identifiers for keypresses run
~~~ bash
xbindkeys -k
~~~
which will open a white window. As soon as it shwos up you can press any key or key combination. The window will close and on your console you will see the corresponding format for xbindkeys. Copy the program output to the file `~/.xbindkeysrc` and replace `(Scheme function)` with the desired command.

I use the following to control my ALSA volume and my players via playerctl. playerctl supports a large variety of players and therefore is a good choice if you are using common players.
~~~ bash
"playerctl play-pause"
    m:0x0 + c:172
    XF86AudioPlay
"playerctl previous"
    m:0x0 + c:173
    XF86AudioPrev
"playerctl next"
    m:0x0 + c:171
    XF86AudioNext

"amixer sset Master toggle"
    m:0x0 + c:121
    XF86AudioMute
"amixer sset Master 5%- unmute"
    m:0x0 + c:122
    XF86AudioLowerVolume
"amixer sset Master 5%+ unmute"
    m:0x0 + c:123
    XF86AudioRaiseVolume
~~~

Of course you have to launch xbindkeys. You can do this manually or automatically at login/startup. My X session runs with my user account so I start xbindkeys with my account as well. For this purpose I use a systemd user service. The way you want to achieve this depends on your init system and the way you init your X server. I assume that you know how to automatically start programs. Your distribution should have a recommendation in its documentation at some place.

