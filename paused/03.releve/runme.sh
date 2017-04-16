
clear
RUNCMD="python"
THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
while :
    do
        echo -n  "run --> "$THISDIR"/"
        read MYFILENAME
        $RUNCMD "$THISDIR""/""$MYFILENAME"
        clear
    done
