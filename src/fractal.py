
import matplotlib.pyplot as plt
import numpy as np

def triangle_subdivision(n,pattern_name):
    """
    makes a fractal of triangluar subdivisions
    with n deep divisions
    """

    #plot main triangle
    r=1

    d_theta = 2*np.pi/3

    x_verts = []
    y_verts = []

    for i in range(0,3):

        theta = i*2*np.pi/3 + np.pi/2

        x = r*np.cos(theta)
        y = r*np.sin(theta)
        x_verts.append(x)
        y_verts.append(y)

    def divide_tri_serpinski(x_verts,y_verts):
        """
        return 3 sub triangles from 1 triangle
        """
        x_centre = np.mean(x_verts)
        y_centre = np.mean(y_verts)
     
        x_verts_new = []
        y_verts_new = []

        x_verts_new.append((x_verts[0]+x_verts[1])/2)
        y_verts_new.append((y_verts[0]+y_verts[1])/2)

        x_verts_new.append((x_verts[1]+x_verts[2])/2)
        y_verts_new.append((y_verts[1]+y_verts[2])/2)

        x_verts_new.append((x_verts[0]+x_verts[2])/2)
        y_verts_new.append((y_verts[0]+y_verts[2])/2)

        triangle_1 = ['k', [x_verts[0],x_verts_new[0],x_verts_new[2]],[y_verts[0],y_verts_new[0],y_verts_new[2]]]
        triangle_2 = ['k',[x_verts_new[0],x_verts[1],x_verts_new[1]],[y_verts_new[0],y_verts[1],y_verts_new[1]]]
        triangle_3 = ['k',  [x_verts_new[1],x_verts[2],x_verts_new[2]],[y_verts_new[1],y_verts[2],y_verts_new[2]]]

        sub_triangles = [triangle_1,triangle_2,triangle_3]
        return sub_triangles

    def n_div(x_verts,y_verts, n,sites = [],bonds=[]):
        """
        """
        # collect sites 
        for i in range(0,len(x_verts)):
            if [x_verts[i],y_verts[i]] not in sites:
                sites.append([x_verts[i],y_verts[i]])

            # collect bonds
            if n == 0:
                for j in range(0,len(x_verts)):
                    bond = [[x_verts[i],x_verts[j]],[y_verts[i],y_verts[j]]]
                    bond_rev = [[x_verts[j],x_verts[i]],[y_verts[j],y_verts[i]]]
                    if i!=j and bond not in bonds and bond_rev not in bonds:
                        bonds.append(bond)

        # recursively make pattern
        if n >= 1:
            if pattern_name == 'serpinski':
                sub_triangles = divide_tri_serpinski(x_verts,y_verts)
            for triangle in sub_triangles:
                sites,bonds = n_div(triangle[1],triangle[2],n-1,sites=sites,bonds=bonds)
        return sites,bonds

    
    sites,bonds = n_div(x_verts,y_verts, n)
    print(f'\nserpinski summary:\n - {n} dimension\n - {len(sites)} sites\n - {len(bonds)} bonds')

    return sites,bonds

#####################################################
def construct_serpinski_2d(n):
    """
    """

    sites,bonds = triangle_subdivision(n,'serpinski')

    #####################################################
    # number site locations
    sites_dict = {}
    for i in range(0,len(sites)):
        sites_dict[i] = sites[i]

    # gather bond site numbers
    bonds_dict = {}
    for i in range(0,len(bonds)):\
       # print(bonds[i])
        site1 = [bonds[i][0][0],bonds[i][1][0]]
        site2 = [bonds[i][0][1],bonds[i][1][1]]
        site_1_num = [key for key, value in sites_dict.items() if value == site1][0]
        site_2_num = [key for key, value in sites_dict.items() if value == site2][0]
        bonds_dict[i] = [site_1_num,site_2_num]
    
    # print('site no, site pos')
    # for item in sites_dict.items():
    #     print(item)

    # print('bonds no, sites')
    # for item in bonds_dict.items():
    #     print(item)

    #####################################################

    # draw fractal
    plt.figure()
    for site in sites:
        site_num = [key for key, value in sites_dict.items() if value == site][0]
        #plt.scatter(site[0],site[1],c='k')
        plt.text(site[0],site[1],site_num,c='r')

    for bond in bonds:
        plt.plot(bond[0],bond[1],c='grey')

    plt.xlim([-1,1])
    plt.ylim([-1,1])
    plt.axis('off')

    plt.xlim([-1,1])
    plt.ylim([-1,1])
    plt.axis('off')
    plt.tight_layout()
   # plt.title(f'N={n}')
    plt.text(-1,-1,f'No. of bonds = {len(bonds)}',c='k')
    plt.text(-1,-0.9,f'No. of sites = {len(sites)}',c='k')
    plt.text(-1,-0.8,'',c='k')
    plt.text(-1,-0.8,f'Fractal dim = {n}',c='k')


    #plt.show()
    import os
    if not os.path.exists(f'output/N={n}'):
        os.makedirs(f'output/N={n}')
    plt.savefig(f'output/N={n}/N={n}_lattice.png')

    return sites_dict, bonds_dict


