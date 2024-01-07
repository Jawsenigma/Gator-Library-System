import sys

class BinaryMinHeap:
    def __init__(self, maxsize):
        # Initialize the BinaryMinHeap with the specified maximum size
        self.maxsize = maxsize
        self.size = 0
        # Create a list to represent the heap, initialize elements to 0
        self.Heap = [0] * (self.maxsize + 1)
        # Set a placeholder element at index 0 to simplify calculations
        self.Heap[0] = (-1, -1, -1)
        # Set the index of the root value in the heap
        self.rootval = 1

    def parent_index(self, current_pos):
        # Calculate the index of the parent given the current position
        return current_pos // 2

    def child_indices(self, current_pos):
        # Calculate the indices of the left and right children given the current position
        left_child = 2 * current_pos
        right_child = (2 * current_pos) + 1
        return left_child, right_child

    def is_leaf(self, current_pos):
        # Check if the current position corresponds to a leaf node
        return current_pos * 2 > self.size

    def swap_elements(self, first_pos, second_pos):
        # Swap elements at two specified positions in the heap
        self.Heap[first_pos], self.Heap[second_pos] = self.Heap[second_pos], self.Heap[first_pos]

    def Heapify(self, current_pos):
        # Recursively maintain the heap property starting from the given position
        if not self.is_leaf(current_pos):
            left_child, right_child = self.child_indices(current_pos)

            for child in (left_child, right_child):
                # Check if the child is within the heap and if it violates the heap property
                if (
                        child <= self.size
                        and (
                        self.Heap[current_pos][1] > self.Heap[child][1]
                        or (
                                self.Heap[current_pos][1] == self.Heap[child][1]
                                and self.Heap[current_pos][2] > self.Heap[child][2]
                        )
                )
                ):
                    if (
                            right_child <= self.size
                            and (
                            left_child > self.size
                            or self.Heap[left_child][1] < self.Heap[right_child][1]
                            or (
                                    self.Heap[left_child][1] == self.Heap[right_child][1]
                                    and self.Heap[left_child][2] < self.Heap[right_child][2]
                            )
                    )
                    ):
                        child = left_child
                    # Swap the current element with the selected child
                    self.swap_elements(current_pos, child)
                    # Recursively call Heapify on the swapped position
                    self.Heapify(child)

    def insert(self, patron_id, priority, reservation_time):
        # Insert a new element into the heap with the specified values
        if self.size >= self.maxsize:
            return
        element = (patron_id, priority, reservation_time)
        self.size += 1
        self.Heap[self.size] = element
        current_pos = self.size

        # Maintain the heap property by swapping with the parent if necessary
        while self.Heap[current_pos][1] < self.Heap[self.parent_index(current_pos)][1]:
            self.swap_elements(current_pos, self.parent_index(current_pos))
            current_pos = self.parent_index(current_pos)

    def build_Heap(self):
        # Build a heap from the existing elements in the heap
        for current_pos in range(self.size // 2, 0, -1):
            self.Heapify(current_pos)

    def extract_min(self):
        # Extract the minimum element from the heap
        min_element = self.Heap[self.rootval]
        self.Heap[self.rootval] = self.Heap[self.size]
        self.size -= 1
        # Restore the heap property after extraction
        self.Heapify(self.rootval)
        return min_element

    def is_empty(self):
        # Check if the heap is empty
        return self.size == 0