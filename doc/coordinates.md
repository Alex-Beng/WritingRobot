This doc is for coordinates system refer to this project

# Original coor in TTF

![ttf coor](./images/ttf_coor.png)

## after uni2pnts

<img src="https://render.githubusercontent.com/render/math?math=\begin{cases}x = x'%2B\delta x \\y = y'%2B \delta y \end{cases}">




![0base coor](images/0base_coor.png)

## after pnt2skeleton

coor sys keep the same

![0base coor](images/0base_coor.png)

## stroke analysis

green line meanning 
<img src="https://render.githubusercontent.com/render/math?math=y = x %2B m \\ \rightarrow m = y - x ">


in Chinese word, the stroke always begin at
<img src="https://render.githubusercontent.com/render/math?math=argmax(m), y \in Y, x \in X.">


![stroke analysis](images/stroke%20analysis.png)

## after get_max_continue

coor sys keep the same

![0base coor](images/0base_coor.png)


# coor system in library

## opencv

in cpp-opencv, src.at(i,j) is using (i,j) as (row,column) but Point(x,y) is using (x,y) as (column,row)

while in python-opencv, src's type is numpy.ndarray, which means that src[i, j] is in numpy's coor sys.

![0base coor](images/opencv_coor1.png)

## numpy

in numpy, src[i,j] is using (i,j) as (row,column).


![0base coor](images/opencv_coor2.png)
