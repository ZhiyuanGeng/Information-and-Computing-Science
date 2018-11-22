def safety_test(process_list, available):
    work = list(available)
    finish = [False for i in process_list]
    safety_sequence = []
    n = 0
    N = len(process_list)

    while n < N:
        org = n
        for i in process_list:
            re = 0
            for j in range(len(work)):
                if finish[process_list.index(i)] is False and i.get_need(j) <= work[j]:
                    re = re + 1
            if re == len(work):
                safety_sequence.append(i)
                for j in range(len(work)):
                    work[j] = work[j] + i.get_allocation(j)
                    finish[process_list.index(i)] = True
                n = n + 1
        if org == n:
            return False
    return True


class Process:
    def __init__(self, max, allocation, need):
        self._max = max  # constant
        self._allocation = allocation  # 1*n
        self._need = need  # 1*n

    def get_allocation(self, j):
        return self._allocation[j]

    def get_need(self, j):
        return self._need[j]

    def request(self, k, process_list, available):
        # Validity test
        for p in range(len(k)):
            if k[p] > self.get_need(p):
                print('The number of requested resources is larger than the maximal need.')
                return
            if k[p] > available[p]:
                print('Resource is not enough.')
                return

        # Try to assign the resource to the process
        for p in range(len(k)):
            available[p] = available[p] - k[p]
            self._allocation[p] = self.get_allocation(p) + k[p]
            self._need[p] = self.get_need(p) - k[p]

        # Safety test
        tmp = tuple(available)
        if safety_test(process_list, tmp):
            print('The request is satisfied.')
            return
        else: # If the system is not safe, the process must return the resource
            for p in range(len(k)):
                available[p] = available[p] + k[p]
                self._allocation[p] = self.get_allocation(p) - k[p]
                self._need[p] = self.get_need(p) + k[p]
            print('The process must be waiting.')
            return


if __name__ == '__main__':
    p0 = Process([7, 5, 3], [0, 1, 0], [7, 4, 3])
    p1 = Process([3, 2, 2], [2, 0, 0], [1, 2, 2])
    p2 = Process([9, 0, 2], [3, 0, 2], [6, 0, 0])
    p3 = Process([2, 2, 2], [2, 1, 1], [0, 1, 1])
    p4 = Process([4, 3, 3], [0, 0, 2], [4, 3, 1])
    process_list = [p0, p1, p2, p3, p4]
    available = [3, 3, 2]
    p1.request([1, 0, 2], process_list, available)
    p4.request([3, 3, 0], process_list, available)
    p0.request([0, 2, 0], process_list, available)