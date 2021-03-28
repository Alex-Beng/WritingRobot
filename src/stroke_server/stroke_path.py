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
        print("in",res_path)
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
    print(res_path)
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
    print(get_max_continue(pnts, True, 0, None))
    
                    
                

        
