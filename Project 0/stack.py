class Stack:
    #initializes stack as an empty one
    def __init__(self, max_size):
        self.size = 0
        self.max_size = max_size
        self.elements = []

    def empty(self):
        if self.size == 0:
            return 1
        return 0

    def full(self):
        if self.size == self.max_size:
            return 1
        return 0

    def push(self, item):
        if self.full():
            print "Stack is full! Cannot push the new element"
            return 0
        else:
            self.elements += item
            self.size += 1
            print "Item pushed successfully!"
            return 1

    def pop(self):
        if self.empty():
            print "Stack is empty!"
            return 0
        else:
            popped = self.elements[self.size-1]
            self.elements.remove(self.elements[self.size-1])
            self.size -= 1
            print "Item popped successfully!"
            return popped

    def print_me(self):
        print self.elements, " ", self.size


if __name__ == "__main__":
    # Define a capacity after which the stack is considered full.
    stack_size = input("Insert maximum stack capacity: ")
    stack = Stack(stack_size)
    # variable "flag" defines whether there is a mistake in the balance or not. Initializes as balanced.
    flag = 1
    stack.print_me()
    expression = raw_input("Insert an algebraic expression: ")
    for i in expression:
        if i == "(" or i == "[" or i == "{":
            if not stack.push(i):
                break
            stack.print_me()
        elif i == ")" or i == "]" or i == "}":
            temp = stack.pop()
            if not temp:
                flag = 0
                break
            stack.print_me()
            if not((temp == "(" and i == ")") or (temp == "[" and i == "]") or (temp == "{" and i == "}")):
                flag = 0
                print "Items do not match!"
                break
    if stack.empty() and flag == 1:
        print "The expression has properly balanced parentheses!"
    else:
        print "The parentheses are not balanced properly!"
