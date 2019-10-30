#create pallete:
- ffmpeg -f image2 -i anim_%04d.png -vf palettegen palette.png

#use pallete:
- ffmpeg -f image2 -framerate 1 -i anim_%04d.png -i palette.png -filter_complex "scale=493:536[x];[x][1:v]paletteuse" output.gif
