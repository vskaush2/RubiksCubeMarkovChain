import pandas as pd
from joblib import Parallel, delayed
from MarkovGraph import *



class MarkovChainCalculations:

    def __init__(self, n):
        self.n=n
        self.transition_matrix = MarkovGraph(self.n, True).transition_matrix


    def compute_chain_distribution(self, t):
        directory = '{}D/Chain_Distributions'.format(self.n)
        try:
            os.makedirs(directory)
        except:
            pass
        file_path = "{}/{}_Scrambles.npz".format(directory, t)
        pi_t = None

        if os.path.exists(file_path):
            pi_t = sc.sparse.load_npz(file_path)

        else:
            if t == 0:
                N = self.transition_matrix.shape[0]
                I = sc.sparse.identity(N)
                pi_t = I.getcol(0) # pi_0 is the first basis vector in R^N (corresponding to the constant random variable equal to the identity permutation)

            if t > 0:
                pi_t = self.transition_matrix * self.compute_chain_distribution(t-1) # Recursive Sparse Matrix Vector Calculation

            if np.isclose(pi_t.data.sum(), 1.0):
                print("SAVING CHAIN DISTRIBUTION {} ... ".format(t))
                sc.sparse.save_npz(file_path, pi_t)
                print("DONE !!!")

        return pi_t


    def compute_current_total_variation_distances_df(self):
        N = self.transition_matrix.shape[0]
        t=len(os.listdir('{}D/Chain_Distributions'.format(self.n)))
        pis = Parallel(n_jobs=t, verbose=0, prefer='threads')(delayed(self.compute_chain_distribution)(j) for j in range(t))
        current_total_variation_distances_df=pd.DataFrame(index=range(t))
        current_total_variation_distances_df['Total Variation Distance to Discrete Uniform Distribution'] \
            = [0.5 * np.linalg.norm(pi.data - 1 / N, 1) + 0.5 * (N - len(pi.data)) / N for pi in pis]
        current_total_variation_distances_df.index.rename("Chain Distribution",inplace=True)
        return current_total_variation_distances_df







