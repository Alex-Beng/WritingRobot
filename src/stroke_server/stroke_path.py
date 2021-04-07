import math
from copy import deepcopy

from tsp import TspSolver

class StrokePath:
    '''
    This class implement the Chinese stroke path
    '''
    def __init__(self, pnts, rect_size=None):
        '''
        Init fucntion

        Args:
            pnts ([[], []]): the xs and ys of points
            rect_size (tuple): the viz rect size
        ''' 
        self.points = pnts

        x_minus_y_max_idx = max(range(len(pnts[0])), key= lambda k: pnts[1][k]-pnts[0][k])

        self.begin_point_idx = x_minus_y_max_idx
        self.begin_point = (pnts[0][x_minus_y_max_idx], pnts[1][x_minus_y_max_idx])
        self.path = get_max_continue(self.points, False, self.begin_point_idx)
        self.end_point_idx = self.path[-1]
        self.end_point = (pnts[0][self.end_point_idx], pnts[1][self.end_point_idx])

        self.points = [[pnts[0][i] for i in self.path], [pnts[1][i] for i in self.path]]

        if rect_size and isinstance(rect_size[0], int) and isinstance(rect_size[1], int):
            self.rect_size = rect_size
        else:
            max_x = max(pnts[0])
            max_y = max(pnts[1])
            self.rect_size = (max_x+1, max_y+1)

    # get&set function part
    def get_points(self):
        return self.points
    def get_normal_path(self):
        return self.path
    def get_reverse_path(self):
        return self.path[::-1]
    def get_begin_pnt(self):
        return self.begin_point, self.begin_point_idx
    def get_end_pnt(self):
        return self.end_point, self.end_point_idx

def euc_distance(pnt1, pnt2):
    '''
    This fucntion calculates the  Euclidian distance between 2 points
    Args:
        pnt1 (tuple): (x, y)
        pnt2 (tuple): (x, y)
    Returns:
        dist (float): Euclidian distance between point 1 and 2
    '''
    dist = math.sqrt((pnt1[0] - pnt2[0])**2 + (pnt1[1] - pnt2[1])**2)
    return dist

def manhat_distance(pnt1, pnt2):
    '''
    This fucntion calculates the  Manhattan distance between 2 points
    Args:
        pnt1 (tuple): (x, y)
        pnt2 (tuple): (x, y)
    Returns:
        dist (float): Manhattan distance between point 1 and 2
    '''
    dist = abs(pnt1[0] - pnt2[0]) + abs(pnt1[1] - pnt2[1])
    return dist

def get_ajmat(stroke_paths, b_pnt, e_pnt):
    n = len(stroke_paths)
    n += 2
    distance = [[0]*n for i in range(n) ]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            t_b = None
            t_e = None
            if i == 0:
                t_b = b_pnt
            elif i == n-1:
                t_b = e_pnt
            else:
                t_b = stroke_paths[i-1].get_end_pnt()[0]
            
            if j == 0:
                t_e = b_pnt
            elif j == n-1:
                t_e = e_pnt
            else:
                t_e = stroke_paths[j-1].get_begin_pnt()[0]
            distance[i][j] = manhat_distance(t_b, t_e)
    return distance
                

def get_max_continue(pnts, head_part_cont=False, start_idx=0, bit_map=None):
    '''
    This function get the longest continue path from pnts[0].

    Args:
        pnts ([[], []]): the xs and ys of points, assume all greater than 0
        head_part_cont (bool): whether the head point is continue
        start_idx (int): index of start of pnts, default 0

    Returns:
        path (list): index of pnts that have the longest continue path begin at pnt[0]
    '''

    if not bit_map:
        # create bit map 
        max_x = max(pnts[0])
        max_y = max(pnts[1])
        # [m, n], m is flag for whether, n is for index for point
        bit_map = [[[0, 0] for i in range(max_y+2)] for j in range(max_x+2)]

        for i in range(len(pnts[0])):
            bit_map[pnts[0][i]] [pnts[1][i]] [0] = 1
            bit_map[pnts[0][i]] [pnts[1][i]] [1] = i


    def check8neighbor(pnt, map):
        neighbor = []
        neignbor_idx = []
        move_vecs = [
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
            [-1, -1],
            [-1, 1],
            [1, 1],
            [1, -1]
        ]
        x = pnt[0]
        y = pnt[1]

        for move_vec in move_vecs:
            new_x = x + move_vec[0]
            new_y = y + move_vec[1]
            if new_x>0 and new_y>0:
                if bit_map[new_x][new_y][0]:
                    neighbor.append((new_x, new_y))
                    neignbor_idx.append(bit_map[new_x][new_y][1])
        return neighbor, neignbor_idx
        
    def verifyneighbor(pnt1, pnt2):
        d_x = abs(pnt1[0]-pnt2[0])
        d_y = abs(pnt1[1]-pnt2[1])
        if d_x <= 1 and d_y <= 1 and d_x+d_y != 0:
            return True
        else:
            return False

    res_path = []
    curr_pnt_idx = start_idx

    # STUPID OPTIMIZATION
    # if head_part_cont:
    #     while True:
    #         curr_pnt = (pnts[0][curr_pnt_idx], 
    #                     pnts[1][curr_pnt_idx])
    #         next_pnt = (pnts[0][curr_pnt_idx+1], 
    #                     pnts[1][curr_pnt_idx+1])
    #         if verifyneighbor(curr_pnt, next_pnt):
    #             res_path.append(curr_pnt_idx)
    #             bit_map[curr_pnt[0]][curr_pnt[1]][0] = 0
                
    #             curr_pnt_idx += 1
    #         else:
    #             break

    while True:
        # print("in",res_path)
        curr_pnt = (pnts[0][curr_pnt_idx], 
                    pnts[1][curr_pnt_idx])

        res_path.append(curr_pnt_idx)
        bit_map[curr_pnt[0]] [curr_pnt[1]] [0] = 0

        
        t_neighbors, t_neighbor_idx = check8neighbor(curr_pnt,
                                                        bit_map)
        # print(curr_pnt_idx, t_neighbors, t_neighbor_idx)
        if len(t_neighbors) == 0:
            break
        elif len(t_neighbors) == 1:
            curr_pnt_idx = t_neighbor_idx[0]
        else:
            branch_paths = []
            for n_idx in t_neighbor_idx:
                branch_paths.append(
                    get_max_continue(pnts, False, n_idx, bit_map)
                )
                # print(branch_paths[-1])
            longest_branch_idx = max(range(len(t_neighbors)), key=lambda k: len(branch_paths[k]))
            res_path += branch_paths[longest_branch_idx]
            break
    # print(res_path)
    return res_path

def paths_planning(stroke_paths, b_pnt, e_pnt, dp_thre=13):
    '''
        This function combine dp and heuristic alg to solve the stroke paths planning,
        which is acutally a tsp-like problem (or AKA NP-hard problem)     
    '''
    raw_stroke_paths = deepcopy(stroke_paths)
    n = len(raw_stroke_paths)

    path_valid = [1 for i in range(n)]
    res_path = []
    if n > dp_thre:
        t_b_pnt = b_pnt
        for i in range(n): # 路径数量大于预设使用 dp 阈值，使用“启tan发xin式”算法
            min_idx = min(range(len(stroke_paths)), 
                            key=lambda k: 
                            float('inf') if not path_valid[k] 
                            else manhat_distance(t_b_pnt, stroke_paths[k].get_begin_pnt()[0]))
            path_valid[min_idx] = 0
            res_path.append(min_idx)

            t_b_pnt = stroke_paths[min_idx].get_end_pnt()[0]
        return res_path


    ajmat = get_ajmat(stroke_paths, (0,0), (255, 255))
    tsp_solver = TspSolver(ajmat, 0, n+1) # 增加了起点终点

    tsp_res, _ = tsp_solver.dp()
    print(tsp_res)
    tsp_res = tsp_res[1:-1]
    tsp_res = [i-1 for i in tsp_res]
    print(tsp_res)

    res_path += tsp_res

    return res_path


# simple test
if __name__ == "__main__":
    pnts = [
        (1, 1),
        (2, 2),
        (3, 3),
        (2, 4),
        (4, 2)
    ]
    pnts = [
        [0, 1, 2, 3, 2, 4, 5, ],
        [0, 1, 2, 3, 4, 2, 1, ]
    ]
    # print(get_max_continue(pnts, True, 0, None))
    
    t = StrokePath(pnts)
    ajmat = get_ajmat([t, t, t, t, t, t, t, t, t, ], (0,0), (255, 255))

    # res = [float('inf'), []]
    paths_planning_dp(ajmat, 0, len(ajmat)-1)
    # print(res)
    
                    
                

        
