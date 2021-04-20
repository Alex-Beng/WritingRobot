1. path planning 
2. trajectory planning
3. ik

# path planning

先代码中硬编码，后续调通信。

如果由于waypoint过多导致ik缓慢，考虑使用B样条规划path

# trajectory planning

笔画起始和结束v为0，中间的waypoint不能停。

反正不用梯形规划就是了。三次/五次规划。

后面用B样条的话，亦可用bspline。

# ik

直接matlab inversekxxxx 好8


