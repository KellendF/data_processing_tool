'''

'''
import numpy as np
import functools
from functools import cmp_to_key

class SegmentsIntersect(object):
    def __init__(self, p1, p2, q1, q2):
        self.result = self.judge_segments_intersect(p1, p2, q1, q2)

    def __sort_by_coordiante(self, x1, x2, k):
        if x1[k] < x2[k]:
            return -1
        elif x1[k] == x2[k]:
            return 0
        else:
            return 1

    def judge_segments_intersect(self, p1, p2, q1, q2):
        p = self.minus(p2, p1)
        q = self.minus(q2, q1)

        denominator = self.crossmultiply(p, q)  # p × q
        t_molecule = self.crossmultiply(self.minus(q1, p1), q)  # (q1 - p1) × q

        if denominator == 0:
            if t_molecule == 0:  # 分子分母都为零时，共线
                p_q = [p1, p2, q1, q2]
                if p1 != q1 and p1 != q2 and p2 != q1 and p2 != q2:
                    p_q = sorted(p_q, key=cmp_to_key(functools.partial(self.__sort_by_coordiante,
                                                                       k=1 if (p2[0] - p1[0]) / (p2[1] - p1[
                                                                           1]) == 0 else 0)))  # 当线段平行于y轴时，需要用y坐标来排序
                    if p_q[0:2] == [p1, p2] or p_q[0:2] == [p2, p1] or p_q[0:2] == [q1, q2] or p_q[0:2] == [q2,
                                                                                                            q1]:  # 共线+没有交点的情况
                        return False
                    else:  # 共线+有重合的情况
                        return False
                else:  # 共线+端点重合，可以继续细分为两对端点都重合（相同线段）or只有一对端点重合 这两种情况
                    return False
            else:  # 分母为零，分子不为零，平行
                return False

        t = t_molecule / denominator
        if t >= 0 and t <= 1:
            u_molecule = self.crossmultiply(self.minus(q1, p1), p)  # (q1 - p1) × p
            u = u_molecule / denominator
            if u >= 0 and u <= 1:  # t, u都满足[0,1]区间，返回交点坐标
                return True
                # return self.plus(p1, self.nummultiply(t, p))
            else:  # u超出区间，则相离
                return False
        else:  # t超出区间，则相离
            return False

    # 向量相加
    def plus(self, a, b):
        c = a + b
        return c

    # 向量相减
    def minus(self, a, b):
        a = np.array(a)
        b = np.array(b)
        c = a - b
        return c

    # 向量叉乘
    def crossmultiply(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    # 向量数乘
    def nummultiply(self, x, a):
        c = a * x
        return c

