
clear
this_dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
out_dir=$this_dir/out
cd "$out_dir"
ls
# convert to video with ffmpeg
ffmpeg -y -i "fr_%05d.png" bbw.m4v
# convert to gif with ImageMagick
convert -set delay 10 -colorspace RGB -colors 256 -dispose Background -loop 1 -scale 50% *.png bbw.gif
# clean up
rm *.png
        
