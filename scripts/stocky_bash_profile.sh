if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
 fi

if [ $STOCKY_BUILD = "DEV" ]; then
	bash_color='35m'
else
	bash_color='31m'
fi
export PS1="\[\033[m\]|\[\033[1;$bash_color\]\t\[\033[m\]|\[\e[1m\]\u\[\e[1;36m\]\[\033[m\]@stocky|$STOCKY_BUILD:\[\e[0m\]\[\e[\
0;37m\][\W]> \[\e[0m\]"
