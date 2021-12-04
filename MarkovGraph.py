from CubePermutation import *
import os
import json
import scipy as sc
from scipy import sparse

class MarkovGraph:

    def __init__(self,n):
        self.n=n
        self.current_permutations_dict = self.load_current_permutations_dict() # Dictionary of Current Permutations in Graph
        self.transition_matrix_nonzero_entry_row_column_indices_dict = self.load_transition_matrix_nonzero_entry_row_column_indices_dict()
        # Dictionary of Nonzero Row Column Entry Indices of Markov Transition Matrix
        self.transition_matrix=self.load_transition_matrix_COO_format() # Transition Matrix in COO Format

    def load_current_permutations_dict(self):
        current_permutations_dict = {0: list(range(6*self.n**2))}
        directory="{}D".format(self.n)
        try:
            os.makedirs(directory)
        except:
            pass
        file_path="{}/All_Permutations.json".format(directory)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                print("LOADING EXISTING ATTAINABLE PERMUTATIONS DICTIONARY ...")
                current_permutations_dict = json.load(f)
                print("DONE !!!")
                print("CONVERTING KEYS TO INTEGERS ...")
                keys = [int(x) for x in current_permutations_dict.keys()]
                current_permutations_dict = dict(zip(keys, current_permutations_dict.values()))
                print("DONE !!!")
        return current_permutations_dict

    def update_current_permutations_dict(self):
        directory = "{}D".format(self.n)
        file_path = "{}/All_Permutations.json".format(directory)
        clockwise_basic_permutations=CubePermutation(self.n).get_clockwise_basic_permutations()
        print("CONVERTING PERMUTATION LISTS TO CYCLIC NOTATION  ...")
        current_permutations = {Permutation(val, size=6 * self.n ** 2) for val in self.current_permutations_dict.values()}
        print("DONE !!!")
        print("OBTAINING ALL ATTAINABLE PERMUTATIONS ...")
        attainable_permutations = {clockwise_basic_permutation * current_permutation
                                   for clockwise_basic_permutation in clockwise_basic_permutations for current_permutation in current_permutations}
        # Attainable permutations are obtained by composing the 6 basic clockwise face rotations with each current list permutation
        print("DONE !!!")
        print("DELETING REDUNDANT PERMUTATIONS ...")
        new_permutations = attainable_permutations - current_permutations # Deleting Redundant Permutations
        print("DONE !!!")

        if len(new_permutations) != 0:
            keys = range(len(current_permutations), len(current_permutations) + len(new_permutations))
            vals = [list(new_permutation) for new_permutation in new_permutations]
            print("UPDATING ATTAINABLE PERMUTATIONS DICTIONARY ...")
            self.current_permutations_dict.update(dict(zip(keys, vals)))
            print("DONE !!!")

            with open(file_path ,'w') as f:
                print("SAVING ATTAINABLE PERMUTATIONS DICTIONARY ...")
                json.dump(self.current_permutations_dict,f)
                print("DONE !!!")
        else:
            print("NOTHING NEW TO SAVE !!!")

        return self.current_permutations_dict

    def load_transition_matrix_nonzero_entry_row_column_indices_dict(self):
        directory = '{}D'.format(self.n)
        file_path = "{}/Transition_Matrix_Nonzero_Entry_Row_Column_Indices.json".format(directory)
        transition_matrix_nonzero_entry_row_column_indices_dict = {0 : []}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                print("LOADING TRANSITION MATRIX NONZERO ENTRY ROW COLUMN INDICES DICTIONARY ...")
                transition_matrix_nonzero_entry_row_column_indices_dict = json.load(f)
                print("DONE !!!")
                print("CONVERTING KEYS TO INTEGERS ...")
                keys = [int(x) for x in transition_matrix_nonzero_entry_row_column_indices_dict.keys()]
                transition_matrix_nonzero_entry_row_column_indices_dict = dict(zip(keys, transition_matrix_nonzero_entry_row_column_indices_dict.values()))
                print("DONE !!!")
        return transition_matrix_nonzero_entry_row_column_indices_dict


    def update_transition_matrix_nonzero_entry_row_column_indices_dict(self,stopping_index=None):
        if stopping_index == None:
            stopping_index=len(self.current_permutations_dict)

        directory = '{}D'.format(self.n)
        file_path = "{}/Transition_Matrix_Nonzero_Entry_Row_Column_Indices.json".format(directory)
        keys = self.current_permutations_dict.keys()
        clockwise_basic_permutations=CubePermutation(self.n).get_clockwise_basic_permutations()

        try:
            incomplete_row_index = next(row_index for row_index in self.current_permutations_dict.keys()
                                        if row_index not in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys() or
                                        len(self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]) != 6)

            print("CONVERTING PERMUTATION LISTS TO CYCLIC NOTATION  ...")
            current_permutations = [Permutation(val, size=6 * self.n ** 2) for val in self.current_permutations_dict.values()]
            print("DONE !!!")

            permutation_index_dict = dict(zip(current_permutations, keys))

            print("UPDATING TRANSITION MATRIX NONZERO ENTRY ROW COLUMN INDICES DICTIONARY ...")
            for row_index in range(incomplete_row_index, stopping_index):
                if row_index not in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys() or len(self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]) != 6:
                    current_permutation = Permutation(self.current_permutations_dict[row_index], size=6 * self.n ** 2)
                    attainable_permutations = [clockwise_basic_permutation * current_permutation for clockwise_basic_permutation in clockwise_basic_permutations
                                               if clockwise_basic_permutation * current_permutation in  permutation_index_dict.keys()]
                    nonzero_row_column_indices = sorted([permutation_index_dict[attainable_permutation] for attainable_permutation in attainable_permutations])
                    self.transition_matrix_nonzero_entry_row_column_indices_dict.update({row_index: nonzero_row_column_indices})
            print("DONE !!!")

            with open(file_path, 'w') as f:
                print("SAVING TRANSITION MATRIX NONZERO ENTRY ROW COLUMN INDICES DICTIONARY ...")
                json.dump(self.transition_matrix_nonzero_entry_row_column_indices_dict, f)
                print("DONE !!!")
        except:
            print("NO INDICES TO UPDATE !!!")
        return self.transition_matrix_nonzero_entry_row_column_indices_dict


    def load_transition_matrix_COO_format(self):
        directory = '{}D'.format(self.n)
        try:
            os.makedirs(directory)
        except:
            pass

        file_path = "{}/Transition_Matrix.npz".format(directory)
        transition_matrix = None
        if os.path.exists(file_path):
            print("LOADING SPARSE TRANSITION MATRIX ...")
            transition_matrix = sc.sparse.load_npz(file_path)
            print("DONE !!!")
        return transition_matrix

    def update_transition_matrix_COO_format(self):
        directory = '{}D'.format(self.n)
        file_path = "{}/Transition_Matrix.npz".format(directory)
        ij_tuples=[(row_index,col_index) for row_index in self.transition_matrix_nonzero_entry_row_column_indices_dict.keys()
                     for col_index in self.transition_matrix_nonzero_entry_row_column_indices_dict[row_index]]

        rows = np.array([t[0] for t in ij_tuples])
        cols = np.array([t[-1] for t in ij_tuples])
        data = np.repeat(1 / 6, len(rows))
        N = len(self.transition_matrix_nonzero_entry_row_column_indices_dict)
        transition_matrix = sc.sparse.coo_matrix((data, (rows, cols)), shape=(N, N))
        print("SAVING SPARSE TRANSITION MATRIX IN COO FORMAT ...")
        sc.sparse.save_npz(file_path, transition_matrix)
        print("DONE !!!")
        return transition_matrix









