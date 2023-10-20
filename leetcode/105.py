from tree import *

class Solution:
    # 从前序和中序遍历建立树，DFS，前序遍历获取根节点，拆开中序遍历数组，按长度拆开前序遍历数组
    def buildTree(self, preorder, inorder):
        if len(preorder) == 0:
            return None
        root = TreeNode(preorder[0])
        idx = 0
        for i in range(len(inorder)):
            if inorder[i] == root.val:
                idx = i
                break
        left_inorder = inorder[0:idx]    
        right_inorder = inorder[idx+1:]
        left_preorder = preorder[1:len(left_inorder)+1]
        right_preorder = preorder[len(left_inorder)+1:]
        root.left = self.buildTree(left_preorder, left_inorder)
        root.right = self.buildTree(right_preorder, right_inorder)
        return root
    
    
if __name__ == '__main__':
    s = Solution()
    preorder = [3,9,20,15,7]
    inorder = [9,3,15,20,7]
    ret = s.buildTree(preorder, inorder)
    print_tree(ret)