from turtle import st


class Solution:
    # 简化文件路径//../ 栈
    def simplifyPath(self, path: str):
        p = path.split('/')
        stk = list()
        for i in p:
            if i in ['.', '/','']:
                continue
            if i == '..' and len(stk) > 0:
                stk.pop()
            elif i != '..':
                stk.append(i)
        ss = '/'
        if len(stk) > 0:
            ss = ss.join(stk)
            ss = '/' + ss
        return ss                
                
            
    
    
if __name__ == '__main__':

    s = Solution()
    ss = "/a/./b/../../c/"
    ret = s.simplifyPath(ss)
    print(ret)