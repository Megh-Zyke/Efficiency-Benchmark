from typing import List, Tuple
from math import log

class Solution:
    def maxLoaves(self, k: float) -> Tuple[int, List[Tuple[int, float]]]:
        # Calculate the maximum number of loaves
        answer = int(log(2.0, 2.0 / k))
        n = 2 * answer  # Max achievable loaves

        # Calculate the lengths of loaves after each cut
        m = 2 ** (1.0 / answer)
        thesum = sum(m**i for i in range(answer))
        
        loaves = [1.0]  # Start with the full loaf
        cuts = []

        # Generate desired loaf sizes
        desired = [m**i / thesum for i in range(answer)]
        desired.reverse()

        # Create the cuts until the desired sizes are achieved
        while len(desired) > 1:
            cuts.append(desired[-1])
            lastsum = desired[-1] + desired[-2]
            del desired[-2:]
            desired.insert(0, lastsum)

        # Generate the cut operations
        operations = []
        
        while cuts:
            length = cuts.pop()
            idx = self.maxIndex(loaves)
            operations.append((idx, length))
            
            loaves[idx] -= length
            loaves.append(length)

        # Final balancing to achieve the maximum loaves
        for _ in range(answer):
            idx = self.maxIndex(loaves[:answer])
            cut_length = loaves[idx] / 2.0
            operations.append((idx, cut_length))

            loaves.append(cut_length)
            loaves[idx] -= cut_length

        return n, operations

    def maxIndex(self, loaves: List[float]) -> int:
        max_val = -1
        max_idx = -1
        
        for i, loaf in enumerate(loaves):
            if loaf > max_val:
                max_val = loaf
                max_idx = i

        return max_idx


solution = Solution()
print(solution.maxLoaves(1.5))