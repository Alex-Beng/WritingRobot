This doc is for coordinates system refer to this project

# Original coor in TTF

![ttf coor](./images/ttf_coor.png)

## after uni2pnts
```math
\begin{cases}
x = x' + \delta x \\
y = y' + \delta y 
\end{cases}
```

![0base coor](images/0base_coor.png)

## after pnt2skeleton

coor sys keep the same

![0base coor](images/0base_coor.png)

## stroke analysis

green line meanning 
```math
    y = x + m \\
    \rightarrow m = y-x
```

in Chinese word, the stroke always begin at

```math
    argmax(m), y \in Y, x \in X.
```


![stroke analysis](images/stroke%20analysis.png)

## after get_max_continue

coor sys keep the same

![0base coor](images/0base_coor.png)


