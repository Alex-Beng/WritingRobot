import json

class TspSolver:
    def __init__(self, distance, b_idx, e_idx):
        self.distance = distance
        self.b_idx = b_idx
        self.e_idx = e_idx

        self.n = len(distance)
        
        # final result
        self.res = [float('inf'), []]

        self.memo = dict()

    
    def dfs(self, s_unsort: list, out: int)->list:
        s_sort = sorted(s_unsort)

        curr_status_key = f'{str(s_sort)};{out}'
        if curr_status_key in self.memo:
            return self.memo[curr_status_key]
        
        if out == self.e_idx:
            return self.distance[out][self.e_idx]
        
        s_unsort.append(out)
        result = float('inf')
        for i in range(self.n):
            if i in s_unsort:
                continue
            if i==self.e_idx and self.n-len(s_unsort)>1:
                continue
            result = min([result, 
                          self.dfs(s_unsort, i)+self.distance[out][i]])
        del s_unsort[-1]

        self.memo[curr_status_key] = result
        return result

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


    ajmat = get_ajmat([t, tt], (0,0), (255, 255))
    print(ajmat)

    n = len(ajmat[0])

    tsp_solver = TspSolver(ajmat, 0, n-1)
    a = tsp_solver.dfs([], 0)
    print(a)
    print(tsp_solver.memo)



