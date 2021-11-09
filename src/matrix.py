from sympy import *
import numpy as np

def avalible_site_nums(root_site_num,bonds_dict):
    """
    """
   # print(f'looking for sites realting to {root_site_num}')

    # collect all bonds containing current root site number
    bonds_containing_site = [bonds_dict[x] for x in bonds_dict if root_site_num in bonds_dict[x]]

    # collect all non root site locations in collect bonds
    avalible_site_jump_nums = []

    for bond in bonds_containing_site:
        for site_num in bond:
            if site_num != root_site_num:
                avalible_site_jump_nums.append(site_num)

   # print(avalible_site_jump_nums)
    return avalible_site_jump_nums

def export_matrix(n,matrix):
    """
    """
    with open(f'output/N={n}/N={n}_matrix.txt', 'w') as f:
        for row in matrix:
          #  print(row)
            f.write(str(row)+'\n')

def export_eigen_values(n,matrix):
    """
    """
    with open(f'output/N={n}/N={n}_Eigen_Values.txt', 'w') as f:
        for row in matrix:
            f.write(str(row)+'\n')

def export_eigen_vectors(n,matrix):
    """
    """
    with open(f'output/N={n}/N={n}_Eigen_Vectors.txt', 'w') as f:
        for row in matrix:
            f.write(str(row)+'\n')

def serpinski_matrix(n,sites_dict,bonds_dict):
    """
    """
    #print(bonds_dict[0])

    col_dim = 3**(n+1)
    #print(f'fractal dimension = {col_dim}')
    row_dim = col_dim

    #define matrix symbols
    A   = MatrixSymbol('A',row_dim,col_dim)
    PSI = MatrixSymbol('psi',row_dim,1)

    #define constant symbols
    t = symbols("t")
    E = symbols("epsilon")

    #create matries
    a = Matrix(A)
    psi = Matrix(PSI)
    # psi[0] will corressponnd to site 0 etc

    static_terms = [site*conjugate(site) for site in psi]
    bond_terms = []
    for i in range(0,len(psi)):
        site_1 = psi[i]
        avalible_nums = avalible_site_nums(i,bonds_dict)
        avalible_sites_psi = [psi[num] for num in avalible_nums]
        for site_2 in avalible_sites_psi:
            bond_terms.append(conjugate(site_1)*site_2)

    H = E*sum(static_terms) - t*sum(bond_terms)
    #pprint(H)    

    # compute psi_dot matrix
    psi_dot_matrix = []
    for col_ind in range(0,col_dim):

        # work around for sympy differentitaing in terms of a conjugate variable
        #temporarily replace conjugate variable in question with a dummy symbol
        dummy = symbols('dummy')
        diff_by = conjugate(psi[col_ind])

        # comeplex i seems to mess with eigen vals
        psi_dot_entry = 1 * diff(expand(H.subs(diff_by, dummy)), dummy).subs(dummy, diff_by)
        psi_dot_matrix.append(psi_dot_entry)

    s=Matrix(psi_dot_matrix)
    #pprint(s)

    eq = Eq(a*psi,s)

    # contructuct matrix via observation
    constucted_matrix = []
    for row_ind in range(0,row_dim):
        constucted_matrix_row = []

        for col_ind in range(0,col_dim): 
            
            a_matrix_entry = Matrix(A)[row_ind,col_ind]
            s_matrix_entry = (s)[row_ind]
            associated_psi = psi[col_ind]

            result_matrix_entry = expand(s_matrix_entry).coeff(associated_psi)

            constucted_matrix_row.append(result_matrix_entry)
            
            #pprint([associated_psi,'is associated with',a_matrix_entry,'with coeff',result_matrix_entry])
        constucted_matrix.append(constucted_matrix_row)

    H_matrix = Matrix(constucted_matrix)
    print(f' - matrix created ({len(constucted_matrix)}x{len(constucted_matrix)})')
    #pprint(H_matrix)
    #export_matrix(n,constucted_matrix)
    return H,H_matrix

    

