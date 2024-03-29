import json

class TspSolver:
    def __init__(self, distance, b_idx, e_idx):
        self.distance = distance
        self.b_idx = b_idx
        self.e_idx = e_idx

        self.n = len(distance)
        
        self.memo = dict()
        '''
            DP[S, i] = [j, C]
            S: visited node
            i: node last visited
            j: node to visit
            C: curr cost

            [S, i]'s format: (tuple(S), i)
            [j, C]'s format: list
        '''
    def dp(self):
        all_pnt_set = set(range(self.n))

        # memo keys: tuple(sorted_points_in_path, last_point_in_path)
        # memo values: list(next_to_visit, curr_cost)
        self.memo = { (tuple([self.b_idx]), self.b_idx): [None, 0] }
        qrq = [ (tuple([self.b_idx]), self.b_idx) ]

        while qrq:
            visited, last_vis = qrq.pop(0)
            _, curr_cost = self.memo[ (tuple(sorted(visited)), last_vis) ]
            vis_able_path = all_pnt_set.difference(set(visited))

            vis_able_path = vis_able_path.difference(set([self.e_idx]))
            if not vis_able_path: # 只能去终点啦
                new_visited = tuple( sorted(list(visited) + [self.e_idx]) )
                new_cost = curr_cost + self.distance[last_vis][self.e_idx]

                self.memo[(new_visited, self.e_idx)] = (last_vis, new_cost)
            
            for to_path in vis_able_path:
                new_visited = tuple( sorted(list(visited) + [to_path]) )
                new_cost = curr_cost + self.distance[last_vis][to_path]

                if (new_visited, to_path) not in self.memo:
                    self.memo[(new_visited, to_path)] = (last_vis, new_cost)
                    qrq += [(new_visited, to_path)]
                else:
                    if new_cost < self.memo[(new_visited, to_path)][1]:
                        self.memo[(new_visited, to_path)] = (last_vis, new_cost)

        return self.retrace_path()

    def retrace_path(self):
        points_to_retrace = set(range(self.n)) # init with all points

        full_path_memo = dict( (k, v) for k, v in self.memo.items()
                                if set(k[0]) == points_to_retrace )
        path_key = min(full_path_memo.keys(), key=lambda k: full_path_memo[k][1])

        last_point = path_key[1] 
        next_to_last_point, optimal_cost = self.memo[path_key]
        optimal_path = [last_point]

        
        while next_to_last_point is not None:
            points_to_retrace = tuple( sorted(set(points_to_retrace).difference({last_point})) )
            last_point = next_to_last_point

            path_key = (points_to_retrace, last_point)

            next_to_last_point, _ = self.memo[path_key]
                    
            optimal_path = [last_point] + optimal_path
        return optimal_path, optimal_cost


if __name__ == '__main__':
    from stroke_path import StrokePath, get_ajmat

    pnts = [
        [0, 1, 2, 3, 2, 1, 0],
        [0, 1, 2, 3, 3, 3, 3]
    ]
    t = StrokePath(pnts)

    pnts = [
        [3, 4, 5],
        [3, 4, 5]
    ]
    tt = StrokePath(pnts)


    # ajmat = get_ajmat([t, tt, t, t, t, t, t, t, t, t, t, t, t, t], (0,0), (255, 255))
    ajmat = get_ajmat([t]*7, (0,0), (255, 255))
    # n   s
    # 18  316
    # 17  61
    # 16  17
    # 15  5.4
    # 14  1.8
    # 13  0.64
    # 12  0.34
    # 11  0.11
    # 10  0.046




    print(ajmat)

    n = len(ajmat[0])

    tsp_solver = TspSolver(ajmat, 0, n-1)
    import time
    b = time.time()
    a = tsp_solver.dp()
    e = time.time()
    print(f'{a} take {e-b}s')
    # print(tsp_solver.memo)



