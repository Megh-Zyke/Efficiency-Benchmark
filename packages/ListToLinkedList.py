from packages.ListNode import ListNode
def list_to_linked_list(lst):
        if not lst:
            return None
        head = ListNode(lst[0])
        current = head
        for value in lst[1:]:
            current.next = ListNode(value)
            current = current.next
        return head

def linked_list_to_list(node : ListNode):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result