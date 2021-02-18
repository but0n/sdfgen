# sdfgen [WIP]

*Signed distance fields generation on GPUs*

Example:
![](https://user-images.githubusercontent.com/7625588/108367275-635cb380-724d-11eb-9ed3-3a1a56a88568.png)


Usage:
```
usage: sdfgen [-h] -i FILE [-o OUTPUT] [-d RES] [--nofit]

Signed distance fields generation on GPUs

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --in FILE    input file [ .obj, .gltf ]
  -o OUTPUT, --out OUTPUT
                        output file name, without extension
  -d RES                Y precision
  --nofit               disable offset model
```