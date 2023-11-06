class Solution:
    # 单词字符翻转，双指针快慢指针移动追加
    def reverseWords(self, s: str) -> str:
        st = 0
        et = 0
        ret = ''
        while st < len(s):
            while st < len(s) and s[st] == ' ':
                st += 1
            et = st
            while et < len(s) and s[et] != ' ':
                et += 1
            print(f'#{s[st:et]}#')
            if len(ret) == 0:
                ret = s[st:et]
            elif st != et:
                ret = s[st:et] + ' '+ret
            st = et+1
        return ret
    
    
if __name__ == '__main__':
    s = Solution()
    v = s.reverseWords("the sky is blue") 
    print(f'#{v}#')