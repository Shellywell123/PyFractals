from src.matrix import *
from src.fractal import *
from src.latex import *

def main():
    """
    """

    for n in range(3,7):

        sites_dict,bonds_dict=construct_serpinski_2d(n)
        H,H_matrix = serpinski_matrix(n,sites_dict,bonds_dict)


        evals = H_matrix.eigenvals()
        # print(' - eigen values found')
        evects = H_matrix.eigenvects()
        # print(' - eigen vaectors found')

        # export_eigen_values(n,evals)
        # export_eigen_vectors(n,evects)

        # print('\nEigen Values:')
        # pprint(evals)

        # print('\nEigen Vectors:')
        # pprint(evects)

        save_to_pdf(n,H,H_matrix,evals,evects)

       

if __name__ == "__main__":
    main()