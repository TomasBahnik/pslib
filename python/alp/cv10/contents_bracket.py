# def brackets(text):
#     stack = []
#     for letter in text:
#         if letter in "[(":
#             stack.append(letter)
#         elif letter in "])":
#             top = stack.pop() + letter
#             print(top)
#         else:
#             if len(stack) > 0:
#                 stack[-1] += letter
#
#
# brackets("aa[bb(cc)dd(ee)fff[gggg]]hhh")

def brackets(text):
    stack = []
    for letter in text:
        if letter in "[({":
            stack.append(letter)
        elif letter in "])}":
            if len(stack) == 0:
                return False
            top = stack.pop() + letter
            if top[0] == '(' and top[-1] != ')':
                return False
            if top[0] == '{' and top[-1] != '}':
                return False
        else:
            if len(stack) > 0:
                stack[-1] += letter
    if len(stack) > 0:
        return False
    return True


brackets("aa[bb(cc)dd(ee)fff[gggg]]hhh")
