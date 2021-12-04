from CubeConfiguration import *
from sympy.combinatorics import SymmetricGroup, Permutation

class CubePermutation:
    def __init__(self, n):
        self.n = n # Dimension of the cube
        self.clockwise_basic_permutations = self.get_clockwise_basic_permutations() # All 6 Clockwise Face Rotation Permutations

    def get_permutation(self, move_seq):
        new_configuration_dict = CubeConfiguration(self.n).move(move_seq)
        enumerated_stickers_list = [entry for face_matrix in new_configuration_dict.values() for entry in face_matrix.reshape(-1)]
        permutation = Permutation(enumerated_stickers_list, size=6 * self.n ** 2)
        return permutation

    def get_clockwise_basic_permutations(self):
        F, L, U, B, R, D = [self.get_permutation(basic_move) for basic_move in basic_moves]
        if self.n == 2:
            B, R, D = F * F * F, L * L * L, U * U * U # Special Replacements for n=2
        return F, L, U, B, R, D

