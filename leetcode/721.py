class Solution:
    # 合并Email地址相同的账户，交并集合处理，记录email到索引ID的map，每次有重合的email地址，则更新
    # 合并索引ID
    # 再按索引ID反转并转为LIST
    def accountsMerge(self, accounts):
        m = dict()
        
        for idx in range(len(accounts)):
            id_num = set()
            for i in range(1,len(accounts[idx])):
                if accounts[idx][i] in m:
                    id_num.add(m[accounts[idx][i]])
            if len(id_num) == 0:
                for j in range(1, len(accounts[idx])):
                    m[accounts[idx][j]] = idx
            else:
                lst = list(id_num)
                merge_id = lst[0]
                for w in lst[1:]:
                    for k in m:
                        if m[k] == w:
                            m[k] = merge_id

                for q in range(1, len(accounts[idx])):
                    m[accounts[idx][q]] = merge_id

        reverse_m = dict()
        for i in m:
            if m[i] not in reverse_m:
                reverse_m[m[i]] = [i]
            else:
                reverse_m[m[i]].append(i)
        ret = list()
        for i in reverse_m:
            em = reverse_m[i]
            em.sort()
            name = [accounts[i][0]]
            for j in em:
                name.append(j)
            ret.append(name)
        return ret


if __name__ == '__main__':
    s = Solution()
    accounts = [["John", "johnsmith@mail.com", "john00@mail.com"], ["John", "johnnybravo@mail.com"], ["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["Mary", "mary@mail.com"]]
    accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
    accounts = [["David","David4@m.co","David2@m.co","David4@m.co"],["John","John7@m.co","John5@m.co","John3@m.co"],["Fern","Fern6@m.co","Fern4@m.co","Fern5@m.co"],["Celine","Celine0@m.co","Celine7@m.co","Celine7@m.co"],["Gabe","Gabe8@m.co","Gabe8@m.co","Gabe1@m.co"],["Ethan","Ethan1@m.co","Ethan6@m.co","Ethan6@m.co"],["Celine","Celine4@m.co","Celine8@m.co","Celine6@m.co"],["Celine","Celine0@m.co","Celine0@m.co","Celine4@m.co"]]
    ret = s.accountsMerge(accounts)
    print(ret)