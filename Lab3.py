#*******************************************************************************************************************************
#Edgar Escobedo
#80502432
#Lab 3 option B
#*******************************************************************************************************************************
#In this program, I created two methods, one which will upload a file containing the english words to a AVL tree and the other
#method that will upload it to a red black tree, after this, I asked the user what word he wants to search, and give them the
#number of anagrams this particular word has. Then for the second part I read all the words from a test file I created, and
#traverse this list storing the word and the number of anagrams it has, then informing the user which word had the greatest amount
#of anagrams


#New node class that will act as a linked list, in order to store all the words as passwords and use the count for thei number of
#anagrams
class Node_list(object):
    password = ""
    count = -1
    next = None

    def __init__(self, password, count):
        self.password = password
        self.count = count
        self.next = None

    def insert(self, node):

        if self.password == "":
            self = node
            return self

        curr = self
        while curr.next != None:
            curr = curr.next
            #print("THIS IS inserted: ",curr.password, curr.count)
        curr.next = node
        return self


#******************************************************AVL****************************************************************
class Node:
    # Constructor with a key parameter creates the Node object.
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    # Calculate the current nodes' balance factor,
    # defined as height(left subtree) - height(right subtree)
    def get_balance(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # Calculate the balance factor.
        return left_height - right_height

    # Recalculate the current height of the subtree rooted at
    # the node, usually called after a subtree has been
    # modified.
    def update_height(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # Assign self.height with calculated node height.
        self.height = max(left_height, right_height) + 1

    # Assign either the left or right data member with a new
    # child. The parameter which_child is expected to be the
    # string "left" or the string "right". Returns True if
    # the new child is successfully assigned to this node, False
    # otherwise.
    def set_child(self, which_child, child):
        # Ensure which_child is properly assigned.
        if which_child != "left" and which_child != "right":
            return False

        # Assign the left or right data member.
        if which_child == "left":
            self.left = child
        else:
            self.right = child

        # Assign the parent data member of the new child,
        # if the child is not None.
        if child is not None:
            child.parent = self

        # Update the node's height, since the subtree's structure
        # may have changed.
        self.update_height()
        return True

    # Replace a current child with a new child. Determines if
    # the current child is on the left or right, and calls
    # set_child() with the new node appropriately.
    # Returns True if the new child is assigned, False otherwise.
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)

        # If neither of the above cases applied, then the new child
        # could not be attached to this node.
        return False


class AVLTree:
    # Constructor to create an empty AVLTree. There is only
    # one data member, the tree's root Node, and it starts
    # out as None.
    def __init__(self):
        self.root = None

    # Performs a left rotation at the given node. Returns the
    # new root of the subtree.
    def rotate_left(self, node):
        # Define a convenience pointer to the right child of the
        # left child.
        right_left_child = node.right.left

        # Step 1 - the right child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.
        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:  # node is root
            self.root = node.right
            self.root.parent = None

        # Step 2 - the node becomes the left child of what used
        # to be its right child, but is now its parent. This will
        # detach right_left_child from the tree.
        node.right.set_child('left', node)

        # Step 3 - reattach right_left_child as the right child of node.
        node.set_child('right', right_left_child)

        return node.parent

    # Performs a right rotation at the given node. Returns the
    # subtree's new root.
    def rotate_right(self, node):
        # Define a convenience pointer to the left child of the
        # right child.
        left_right_child = node.left.right

        # Step 1 - the left child moves up to the node's position.
        # This detaches node from the tree, but it will be reattached
        # later.
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:  # node is root
            self.root = node.left
            self.root.parent = None

        # Step 2 - the node becomes the right child of what used
        # to be its left child, but is now its parent. This will
        # detach left_right_child from the tree.
        node.left.set_child('right', node)

        # Step 3 - reattach left_right_child as the left child of node.
        node.set_child('left', left_right_child)

        return node.parent

    # Updates the given node's height and rebalances the subtree if
    # the balancing factor is now -2 or +2. Rebalancing is done by
    # performing a rotation. Returns the subtree's new root if
    # a rotation occurred, or the node if no rebalancing was required.
    def rebalance(self, node):

        # First update the height of this node.
        node.update_height()

        # Check for an imbalance.
        if node.get_balance() == -2:

            # The subtree is too big to the right.
            if node.right.get_balance() == 1:
                # Double rotation case. First do a right rotation
                # on the right child.
                self.rotate_right(node.right)

            # A left rotation will now make the subtree balanced.
            return self.rotate_left(node)

        elif node.get_balance() == 2:

            # The subtree is too big to the left
            if node.left.get_balance() == -1:
                # Double rotation case. First do a left rotation
                # on the left child.
                self.rotate_left(node.left)

            # A right rotation will now make the subtree balanced.
            return self.rotate_right(node)

        # No imbalance, so just return the original node.
        return node


    def insert(self, node):
        # Special case: if the tree is empty, just set the root to
        # the new node.
        if self.root is None:
            self.root = node
            node.parent = None

        else:
            # Step 1 - do a regular binary search tree insert.
            current_node = self.root
            while current_node is not None:
                # Choose to go left or right
                if node.key < current_node.key:
                    # Go left. If left child is None, insert the new
                    # node here.
                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        # Go left and do the loop again.
                        current_node = current_node.left
                else:
                    # Go right. If the right child is None, insert the
                    # new node here.
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        # Go right and do the loop again.
                        current_node = current_node.right

            # Step 2 - Rebalance along a path from the new node's parent up
            # to the root.
            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent


    # Searches for a node with a matching key. Does a regular
    # binary search tree search operation. Returns the node with the
    # matching key if it exists in the tree, or None if there is no
    # matching key in the tree.
    def search(self, key):
        current_node = self.root
        while current_node is not None:
            # Compare the current node's key with the target key.
            # If it is a match, return the current key; otherwise go
            # either to the left or right, depending on whether the
            # current node's key is smaller or larger than the target key.
            #Updated to search for a key and return a boolean variable
            if current_node.key == key: return True
            elif current_node.key < key: current_node = current_node.right
            else: current_node = current_node.left
        return False


#*****************************************************************************************************************************************
#********************************************AVL ENDS*************************************************************************************


#*****************************************************R&B*********************************************************************************


# RBTNode class - represents a node in a red-black tree
class RBTNode:
    def __init__(self, key, parent, is_red=False, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    # Returns true if both child nodes are black. A child set to None is considered
    # to be black.
    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count

    # Returns the grandparent of this node
    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # Gets this node's predecessor from the left child subtree
    # Precondition: This node's left child is not None
    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    # Returns this node's sibling, or None if this node does not have a sibling
    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    # Returns the uncle of this node
    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    # Returns True if this node is black, False otherwise
    def is_black(self):
        return self.color == "black"

    # Returns True if this node is red, False otherwise
    def is_red(self):
        return self.color == "red"

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    # Sets either the left or right child of this node
    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True


class RedBlackTree:
    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()

    def insert(self, key):
        new_node = RBTNode(key, None, True, None, None)
        self.insert_node(new_node)

    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root is None:
            # Special case for root
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right

        # Color the node red
        node.color = "red"

        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):
        # If node is the tree's root, then color node black and return
        if node.parent is None:
            node.color = "black"
            return

        # If parent is black, then return without any alterations
        if node.parent.is_black():
            return

        # References to parent, grandparent, and uncle are needed for remaining operations
        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        # If parent and uncle are both red, then color parent and uncle black, color grandparent
        # red, recursively balance  grandparent, then return
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # If node is parent's right child and parent is grandparent's left child, then rotate left
        # at parent, update node and parent to point to parent and grandparent, respectively
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        # Else if node is parent's left child and parent is grandparent's right child, then rotate
        # right at parent, update node and parent to point to parent and grandparent, respectively
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        # Color parent black and grandparent red
        parent.color = "black"
        grandparent.color = "red"

        # If node is parent's left child, then rotate right at grandparent, otherwise rotate left
        # at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else:  # node is root
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else:  # node is root
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)

    def _bst_remove(self, key):
        node = self.search(key)
        self._bst_remove_node(node)

    def _bst_remove_node(self, node):
        if node is None:
            return

        # Case 1: Internal node with 2 children
        if node.left is not None and node.right is not None:
            # Find successor
            successor_node = node.right
            while successor_node.left is not None:
                successor_node = successor_node.left

            # Copy successor's key
            successor_key = successor_node.key

            # Recursively remove successor
            self._bst_remove_node(successor_node)

            # Set node's key to copied successor key
            node.key = successor_key

        # Case 2: Root node (with 1 or 0 children)
        elif node is self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right

            # Make sure the new root, if not None, has parent set to None
            if self.root is not None:
                self.root.parent = None

        # Case 3: Internal with left child only
        elif node.left is not None:
            node.parent.replace_child(node, node.left)

        # Case 4: Internal with right child OR leaf
        else:
            node.parent.replace_child(node, node.right)

    def is_none_or_black(self, node):
        if node is None:
            return True
        return node.is_black()

    def is_not_none_and_red(self, node):
        if node is None:
            return False
        return node.is_red()


    def search(self, key):
        current_node = self.root
        while current_node is not None:
            # Return the node if the key matches.
            if current_node.key == key:
                return True

            # Navigate to the left if the search key is
            # less than the node's key.
            elif key < current_node.key:
                current_node = current_node.left

            # Navigate to the right if the search key is
            # greater than the node's key.
            else:
                current_node = current_node.right

        # The key was not found in the tree.
        return False

    def try_case1(self, node):
        if node.is_red() or node.parent is None:
            return True
        return False  # node case 1

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.parent.color = "red"
            sibling.color = "black"
            if node is node.parent.left:
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
            return True
        return False  # not case 2

    def try_case3(self, node, sibling):
        if node.parent.is_black() and sibling.are_both_children_black():
            sibling.color = "red"
            self.prepare_for_removal(node.parent)
            return True
        return False  # not case 3

    def try_case4(self, node, sibling):
        if node.parent.is_red() and sibling.are_both_children_black():
            node.parent.color = "black"
            sibling.color = "red"
            return True
        return False  # not case 4

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.left):
            if self.is_none_or_black(sibling.right):
                if node is node.parent.left:
                    sibling.color = "red"
                    sibling.left.color = "black"
                    self.rotate_right(sibling)
                    return True
        return False  # not case 5

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.left):
            if self.is_not_none_and_red(sibling.right):
                if node is node.parent.right:
                    sibling.color = "red"
                    sibling.right.color = "black"
                    self.rotate_left(sibling)
                    return True
        return False  # not case 6



#READING FILE
#creation of a list with all the words from the file
my_file = open("words_alpha.txt", "r")
list_words = my_file.readlines()

#Introduction of all the words to the AVL tree by the use of the split method to erase any spaces
def load_AVL():
    tree = AVLTree()
    counter = 0
    while (counter != len(list_words)):
        list_x = list_words[counter].lower()
        wrds = list_x.split()
        tree.insert(Node(wrds[0]))
        counter = counter + 1
    return tree


#Introduction of all the words to the Red and Black tree by the use of the split method to erase any spaces
def load_red_black():
    tree = RedBlackTree()
    counter = 0
    while (counter != len(list_words)):
        list_x = list_words[counter].lower()
        wrds = list_x.split()
        tree.insert(wrds[0])
        counter = counter + 1
    return tree

#Creating of the list with all the valid english words in it
def english_words_file():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

#Variables that will be used throughout the program
valid_words = english_words_file()
count = 0
max_count = 0
max_word = ""

#Count anagrams method adapted to take the word and the type of tree it is in order to look for permutations of a word, but only if the
#word exists in the particular tree will the counter be updated to give the total amount of anagrams
def count_anagrams_trees(word, tree, prefix=""):
    global count
    if len(word) <= 1:
        str = prefix + word
        if tree.search(prefix + word) == True :
            count +=1
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i] # letters before cur
            after = word[i + 1:] # letters after cur
            if cur not in before: # Check if permutations of cur have not been generated.
                count_anagrams_trees(before + after, tree,  prefix + cur)


num = 0
#Second count anagrams that does not require the tree, used in the second part of the program to find the word with the greatest amount
#of anagrams through a node with the information
def count_anagrams(word, prefix=""):
    global num
    if len(word) <= 1:
        str = prefix + word
        if str in valid_words:
            num +=1
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i] # letters before cur
            after = word[i + 1:] # letters after cur
            if cur not in before: # Check if permutations of cur have not been generated.
                count_anagrams(before + after, prefix + cur)


#Creation of a list with all the words from the test file, which will be inserted into a node, and using the "next" property it will
#traverse the whole list, and for each word it will find its number of anagrams and store it as a counter, to be able to tell at the
#end which is the word with the greatest number of anagrams
my_file = open("test.txt", "r")
passwords_list = my_file.readlines()
counter = 0
head = Node_list("", 0)
while (counter != len(passwords_list)):
    list_x = passwords_list[counter]
    wrds = list_x.split()
    count_anagrams(wrds[0].lower())
    head = head.insert(Node_list(wrds[0], num))
    num = 0
    counter = counter + 1

#Menu for first part of the program, which will ask user to pick a tree, and only if the user intorduces the number "3" will it exit this
#part of the program, user can look for the anagram of whatever the number of words s/he wants
choice = input("Select which tree you want to use\n1.- AVL tree\n2.- Red Black tree\n3.- Exit\n")
while choice is not "3":
    if choice == "1":
        print("Loading AVL tree")
        words_AVL = load_AVL()
        print("Remember to type 3 at any point if you want to exit")
        while choice !=3:
            anagrams = input("select the word that you want to search for:\n")
            anagrams = str(anagrams).lower()
            choice = anagrams
            if choice == "3":
                break
            if words_AVL.search(anagrams) != True:
                print("Please enter a valid word")
            else:
                count_anagrams_trees(anagrams, words_AVL)
                print("The word "+anagrams.upper()+" that you searched for has "+str(count)+" anagrams")
                count = 0
    if choice == "2":
        print("Loading Red Black tree")
        words_red_black = load_red_black()
        print("Remember to type 3 at any point if you want to exit")
        while choice != "3":
            anagrams = input("select the word that you want to search for:\n")
            anagrams = str(anagrams).lower()
            choice = anagrams
            if choice == "3":
                break
            if words_red_black.search(anagrams) != True:
                print("Please enter a valid word")
            else:
                count_anagrams_trees(anagrams, words_red_black)
                print("The word " + anagrams.upper() + " that you searched for has " + str(count) + " anagrams")
                count = 0
    if choice != "1" and choice != "2" and choice !="3":
        print("Please enter valid choice")
    if choice == "3":
        print("Thank you")
        break
    else:
        choice = input("Select which tree you want to use\n1.- AVL tree\n2.- Red Black tree\n3.- Exit\n")

print("Now from your text file you will know which is the word with the greatest number of anagrams")

curr = head
max_word=""
max_count=0

#Second part of the program, traversal of the node to look fo rthe word with the greatest number of anagrams
while(curr!= None):
    if curr.count > max_count:
        max_count = curr.count
        max_word = curr.password
    curr = curr.next

print("The word with the greatest number of anagrams is: "+max_word.upper()+".\nThe amount of anagrams that it has is: "+str(max_count))