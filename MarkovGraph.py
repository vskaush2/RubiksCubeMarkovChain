import os
import json
import scipy as sc
from scipy import sparse
from sympy.combinatorics import Permutation
from CubeConfiguration import *

def get_permutation(move_seq, n):
    new_configuration_dict = CubeConfiguration(n=n).move(move_seq)
    enumerated_stickers_list = [entry for face_matrix in new_configuration_dict.values() for entry in face_matrix.reshape(-1)]
    permutation = Permutation(enumerated_stickers_list, size=6 * n ** 2)
    return permutation

def get_rotation_permutations(n):
    F, L, U, B, R, D = [get_permutation(basic_move,n) for basic_move in basic_moves]
    if n == 2:
        return F, L, U, F*F*F, L*L*L, U*U*U
    elif n == 3:
        return F, L, U, B, R, D, F*F*F, L*L*L, U*U*U, B*B*B, R*R*R, D*D*D

class MarkovGraph:
    def __init__(self, n, load_only_transition_matrix = False):
        self.n = n # Dimension of Cube
        self.directory = "{}D".format(self.n)
        try:
            os.makedirs(self.directory)
        except:
            pass
        if load_only_transition_matrix:
            self.transition_matrix = self.load_transition_matrix_COO_format()  # Transition Matrix in COO Format
        else:
            self.rotation_permutations = get_rotation_permutations(self.n)
            self.current_permutations_dict = self.load_current_permutations_dict()  # Dictionary of Current Permutations in Graph
            self.transition_matrix_nonzero_entry_row_column_indices_dict = self.load_transition_matrix_nonzero_entry_row_column_indices_dict()  # Dictionary of Nonzero Row Column Entry Indices of Markov Transition Matrix
            self.transition_matrix = self.load_transition_matrix_COO_format()

    def load_current_permutations_dict(self):
        current_permutations_dict = {0 : get_permutation('', self.n)}
        file_path = "{}/All_Permutations.json".format(self.directory)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                current_permutations_dict = json.load(f)
                keys = [int(x) for x in current_permutations_dict.keys()]
                print("CONVERTING LISTS TO PERMUTATIONS ... ")
                current_permutations = [Permutation(val, size=6 * self.n ** 2) for val in current_permutations_dict.values()]
                current_permutations_dict = dict(zip(keys, current_permutations))
        return current_permutations_dict

    def update_current_permutations_dict(self):
        file_path = "{}/All_Permutations.json".format(self.directory)
        current_permutations = set(self.current_permutations_dict.values())
        print("FINDING ALL ATTAINABLE PERMUTATIONS ... ")
        attainable_permutations = {rotation_permutation * current_permutation for rotation_permutation in self.rotation_permutations
                                   for current_permutation in current_permutations}
        # Attainable permutations are obtained by composing each rotation permutation with each current list permutation
        print("DELETING REDUNDANT PERMUTATIONS ... ")
        new_permutations = attainable_permutations - current_permutations  # Deleting Redundant Permutations

        if len(new_permutations) != 0:
            new_keys = list(range(len(current_permutations), len(current_permutations) + len(new_permutations)))
            new_vals = list(new_permutations)
            new_dict = dict(zip(new_keys, new_vals))
            self.current_permutations_dict.update(new_dict)
            with open(file_path, 'w') as f:
                keys=self.current_permutations_dict.keys()
                print("SAVING ALL PERMUTATIONS ... ")
                vals=[list(current_permutation) for current_permutation in self.current_permutations_dict.values()]
                json.dump(dict(zip(keys, vals)), f)
        return self.current_permutations_dict

    def load_transition_matrix_nonzero_entry_row_column_indices_dict(self):
        file_path = "{}/Transition_Matrix_Nonzero_Entry_Row_Column_Indices.json".format(self.directory)
        transition_matrix_nonzero_entry_row_column_indices_dict = {0 : []}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                print("LOADING TRANSITION MATRIX NONZERO ROW COLUMN INDICES DICTIONARY ... ")
                transition_matrix_nonzero_entry_row_column_indices_dict = json.load(f)
                keys = [int(x) for x in transition_matrix_nonzero_entry_row_column_indices_dict.keys()]
                vals = transition_matrix_nonzero_entry_row_column_indices_dict.values()
                transition_matrix_nonzero_entry_row_column_indices_dict = dict(zip(keys, vals))
        return transition_matrix_nonzero_entry_row_column_indices_dict

    def update_transition_matrix_nonzero_entry_row_column_indices_dict(self, stopping_index=None):
        file_path = "{}/Transition_Matrix_Nonzero_Entry_Row_Column_Indices.json".format(self.directory)

        if stopping_index == None:
            stopping_index = len(self.current_permutations_dict)

        keys = self.current_permutations_dict.keys()
        current_permutations = self.current_permutations_dict.values()

        try:
            incomplete_row_index = next(row_index for row_index in self.current_permutations_dict.keys()
                                        if row_index not in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys() or
                                        len(self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]) != len(self.rotation_permutations))


            permutation_index_dict = dict(zip(current_permutations, keys))

            for row_index in range(incomplete_row_index, stopping_index):
                if row_index not in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys() or \
                        len(self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]) != len(self.rotation_permutations):

                    current_permutation = self.current_permutations_dict[row_index]
                    attainable_permutations = [rotation_permutation * current_permutation for
                                               rotation_permutation in self.rotation_permutations
                                               if rotation_permutation * current_permutation in permutation_index_dict.keys()]

                    nonzero_row_column_indices = sorted([permutation_index_dict[attainable_permutation] for attainable_permutation in
                                                         attainable_permutations])

                    self.transition_matrix_nonzero_entry_row_column_indices_dict.update({row_index : nonzero_row_column_indices})

            with open(file_path, 'w') as f:
                print("SAVING TRANSITION MATRIX NONZERO ROW COLUMN INDICES DICTIONARY ... ")
                json.dump(self.transition_matrix_nonzero_entry_row_column_indices_dict, f)
        except:
            pass



    def load_transition_matrix_COO_format(self):
        file_path = "{}/Transition_Matrix.npz".format(self.directory)
        transition_matrix = None
        if os.path.exists(file_path):
            print("LOADING TRANSITION MATRIX IN SPARSE COO FORMAT ... ")
            transition_matrix = sc.sparse.load_npz(file_path)
        return transition_matrix

    def update_transition_matrix_COO_format(self):
        file_path = "{}/Transition_Matrix.npz".format(self.directory)
        ij_tuples = [(row_index, col_index) for row_index in
                     self.transition_matrix_nonzero_entry_row_column_indices_dict.keys()
                     for col_index in self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]]

        rows = np.array([t[0] for t in ij_tuples])
        cols = np.array([t[-1] for t in ij_tuples])
        data = np.repeat(1 / len(self.rotation_permutations), len(rows))
        N = len(self.transition_matrix_nonzero_entry_row_column_indices_dict)
        self.transition_matrix = sc.sparse.coo_matrix((data, (rows, cols)), shape=(N, N))
        print("SAVING TRANSITION MATRIX IN SPARSE COO FORMAT ... ")
        sc.sparse.save_npz(file_path, self.transition_matrix)


