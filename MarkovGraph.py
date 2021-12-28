import os
import json
import scipy as sc
from scipy import sparse
from sympy.combinatorics import Permutation
from CubeConfiguration import *

def get_permutation(move_seq, n):
    new_configuration_dict = CubeConfiguration(n=n).move(move_seq)
    enumerated_stickers_list = [entry for face_matrix in new_configuration_dict.values() for entry in face_matrix.reshape(-1)]
    permutation = Permutation(enumerated_stickers_list, size = 6 * n ** 2)
    return permutation

def get_face_rotation_permutations(n):
    F, L, U, B, R, D = [get_permutation(basic_move,n) for basic_move in basic_moves] # The 6 clockwise permutations
    if n == 2:
        return F, L, U, F*F*F, L*L*L, U*U*U # B,R,D are the same as F^3, L^3, U^3 in the 2D cube
    if n == 3:
        return F, L, U, B, R, D, F*F*F, L*L*L, U*U*U, B*B*B, R*R*R, D*D*D

class MarkovGraph:
    def __init__(self, n, load_only_transition_matrix = True):
        self.n = n # Dimension of the Cube i.e. the square root of the quantity total number of stickers divided by 6
        self.directory = "{}D Scrambling Chain".format(self.n)
        try:
            os.makedirs(self.directory)
            load_only_transition_matrix = False
        except:
            pass

        if load_only_transition_matrix == False:
            self.face_rotation_permutations = get_face_rotation_permutations(self.n) # All face rotation permutations
            self.current_permutations_dict = self.get_current_permutations_dict()  # Dictionary of Current Permutations in Graph
            self.transition_matrix_nonzero_entry_row_column_indices_dict = self.get_transition_matrix_nonzero_entry_row_column_indices_dict()  # Dictionary of Nonzero Row Column Entry Indices of Markov Transition Matrix

        self.transition_matrix = self.get_transition_matrix_COO_format() # Transition Matrix in COO Format

    def get_current_permutations_dict(self):
        current_permutations_dict = dict()
        file_path = "{}/All_Permutations.json".format(self.directory)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                current_permutations_dict = json.load(f)
                keys = [int(x) for x in current_permutations_dict.keys()] # Dictionary keys need to be converted to integers when loading the JSON file
                print("CONVERTING LISTS TO PERMUTATIONS ... ")
                current_permutations = [Permutation(l, size = 6 * self.n ** 2) for l in current_permutations_dict.values()] # Dictionary values need to be converted to Sympy permutations when loading the JSON file
                current_permutations_dict = dict(zip(keys, current_permutations))
        else:
            print("INITIALIZING THE DICTIONARY OF PERMUTATIONS TO BE UPDATED ... ")
            current_permutations_dict = {0 : get_permutation('', self.n)}  # Initialize the dictionary of current permutations to have key 0 and value the identity permutation
        print("DONE !!!")
        return current_permutations_dict

    def update_current_permutations_dict(self):
        file_path = "{}/All_Permutations.json".format(self.directory)
        current_permutations = set(self.current_permutations_dict.values())
        print("FINDING ALL ATTAINABLE PERMUTATIONS ... ")
        attainable_permutations = {face_rotation_permutation * current_permutation for face_rotation_permutation in
                                   self.face_rotation_permutations for current_permutation in current_permutations}
        print("DONE !!!")
        print("DELETING PERMUTATIONS ALREADY IN CHAIN ... ")
        future_permutations = attainable_permutations - current_permutations
        print("DONE !!!")
        if len(future_permutations) != 0:
            new_keys = list(range(len(self.current_permutations_dict), len(self.current_permutations_dict) + len(future_permutations)))
            new_vals = list(future_permutations)
            new_dict = dict(zip(new_keys, new_vals))
            self.current_permutations_dict.update(new_dict)

            with open(file_path, 'w') as f:
                keys=self.current_permutations_dict.keys()
                print("SAVING ALL NEW PERMUTATIONS ... ")
                vals=[list(current_permutation) for current_permutation in self.current_permutations_dict.values()]
                json.dump(dict(zip(keys, vals)), f)
        else:
            print("NOTHING NEW TO SAVE ... ")
        print("DONE !!!")


    def get_transition_matrix_nonzero_entry_row_column_indices_dict(self):
        transition_matrix_nonzero_entry_row_column_indices_dict = dict()
        file_path = "{}/Transition_Matrix_Nonzero_Entry_Row_Column_Indices.json".format(self.directory)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                print("LOADING TRANSITION MATRIX NONZERO ROW COLUMN INDICES DICTIONARY ... ")
                transition_matrix_nonzero_entry_row_column_indices_dict = json.load(f)
                keys = [int(x) for x in transition_matrix_nonzero_entry_row_column_indices_dict.keys()]
                vals = transition_matrix_nonzero_entry_row_column_indices_dict.values()
                transition_matrix_nonzero_entry_row_column_indices_dict = dict(zip(keys, vals))
        else:
            print("INITIALIZING THE TRANSITION MATRIX NONZERO ROW COLUMN INDICES DICTIONARY TO BE UPDATED ... ")
            transition_matrix_nonzero_entry_row_column_indices_dict = {0: [0]}

        print("DONE !!!")
        return transition_matrix_nonzero_entry_row_column_indices_dict




    def update_transition_matrix_nonzero_entry_row_column_indices_dict(self, stopping_index=None):
        file_path = "{}/Transition_Matrix_Nonzero_Entry_Row_Column_Indices.json".format(self.directory)
        if stopping_index == None:
            stopping_index = len(self.current_permutations_dict)

        keys = self.current_permutations_dict.keys()
        current_permutations = self.current_permutations_dict.values()

        try:
            print("FINDING THE FIRST INCOMPLETE ROW INDEX ...")
            incomplete_row_index = next(row_index for row_index in self.current_permutations_dict.keys()
                                        if row_index not in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys() or
                                        len(self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]) != len(self.face_rotation_permutations))
            print("DONE !!!")
            permutation_index_dict = dict(zip(current_permutations, keys))

            print("UPDATING TRANSITION MATRIX NONZERO ROW COLUMN INDICES DICTIONARY ...")
            for row_index in range(incomplete_row_index, stopping_index):
                if row_index not in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys() or \
                        len(self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]) != len(self.face_rotation_permutations):

                    current_permutation = self.current_permutations_dict[row_index]
                    attainable_permutations = [face_rotation_permutation * current_permutation for
                                               face_rotation_permutation in self.face_rotation_permutations
                                               if face_rotation_permutation * current_permutation in permutation_index_dict.keys()]

                    nonzero_row_column_indices = sorted([permutation_index_dict[attainable_permutation] for attainable_permutation in
                                                         attainable_permutations]) # Sorting Column indices in ascending order

                    self.transition_matrix_nonzero_entry_row_column_indices_dict.update({row_index : nonzero_row_column_indices})
            print("DONE !!!")
            with open(file_path, 'w') as f:
                print("SAVING TRANSITION MATRIX NONZERO ROW COLUMN INDICES DICTIONARY ... ")
                json.dump(self.transition_matrix_nonzero_entry_row_column_indices_dict, f)
        except:
            print("NOTHING NEW TO UPDATE ... ")
        print("DONE !!!")

    def get_transition_matrix_COO_format(self):
        file_path = "{}/Transition_Matrix.npz".format(self.directory)
        transition_matrix = sc.sparse.identity(1)
        if os.path.exists(file_path):
            print("LOADING TRANSITION MATRIX IN SPARSE COO FORMAT ... ")
            transition_matrix = sc.sparse.load_npz(file_path)
        else:
            print("INITIALIZING THE TRANSITION MATRIX IN SPARSE COO FORMAT TO BE UPDATED ... ")
        print("DONE !!!")
        return transition_matrix

    def update_transition_matrix_COO_format(self):
        file_path = "{}/Transition_Matrix.npz".format(self.directory)
        ij_tuples = [(row_index, col_index) for row_index in
                     self.transition_matrix_nonzero_entry_row_column_indices_dict.keys()
                     for col_index in self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]]

        rows = np.array([t[0] for t in ij_tuples])
        cols = np.array([t[-1] for t in ij_tuples])
        data = np.repeat(1 / len(self.face_rotation_permutations), len(rows))
        N = len(self.transition_matrix_nonzero_entry_row_column_indices_dict)
        self.transition_matrix = sc.sparse.coo_matrix((data, (rows, cols)), shape=(N, N))
        print("SAVING TRANSITION MATRIX IN SPARSE COO FORMAT ... ")
        sc.sparse.save_npz(file_path, self.transition_matrix)
        print("DONE !!!")

    def update_chain(self):
        self.update_current_permutations_dict()
        self.update_transition_matrix_nonzero_entry_row_column_indices_dict()
        self.update_transition_matrix_COO_format()


