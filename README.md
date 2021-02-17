# sdfgen [WIP]

*Signed distance fields generation on GPUs*

Example:
![](https://user-images.githubusercontent.com/7625588/108215054-faaa0400-7184-11eb-8036-65ae81e3426b.png)


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