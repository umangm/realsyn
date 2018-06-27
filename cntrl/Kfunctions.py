import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import cvxopt as cvx
import picos as pic
import numpy as np
from control import *


def ellipsoid_bounds(P):
        dimension = len(P)
        radius_dim = []
        for d in range(dimension):
                d_vec = []
                for temp in range(0,d):
                        d_vec.append(0)
                d_vec.append(1)
                for temp in range(d,dimension-1):
                        d_vec.append(0)

                A = cvx.matrix(P)
                c = cvx.matrix([1])

                #create the problem, variables and params
                prob=pic.Problem()
                AA=cvx.sparse(A,tc='d') #each AA[i].T is a 3 x 5 observation matrix

                AA=pic.new_param('A',AA)
                cc=pic.new_param('c',c)
                ss = pic.new_param('s',cvx.matrix(d_vec))

                x = prob.add_variable('x',AA.size[1])
                # mu = prob.add_variable('mu',1)


                #define the constraints and objective function
                prob.add_list_of_constraints(
                        [x.T*AA*x < cc], #constraints
                        )

                prob.set_objective('max', ss|x)

                #solve the problem and retrieve the optimal weights of the optimal design.
                # print prob
                prob.solve(verbose=0,solver='cvxopt')
                x=x.value

                radius_dim.append(x[d])

        return radius_dim

def radius_array(P, initial_radius, radius_dim, num_steps, lam):
        dimension = len(radius_dim)
        # radius_dim = np.array(radius_dim)

        radius = []
        # Initial radius is just the radius of the initial ball for each dimension

        initial_rad = [initial_radius for i in range(dimension)]
        radius.append(initial_rad)

        # First, we need to use the initial ellispoid x'Px <= c to bound the ball 
        # of x'x <= initial_radius
        # That means, the minimum eigenvalue of x'(P/c)x <= 1 should be at least initial_radius
        # so, \sqrt{c}/\sqrt{max(eig(P))} >= initial_radius
        initial_c = (np.sqrt(max(np.linalg.eigvals(P)))*initial_radius)**2
        # radius_dim is the maximum value of each dimension for the ellipsoid x'Px <= 1
        # at the k-th step, the ellipsoid is x'Px <= lam^{i} * initial_c
        for i in range(1, num_steps+1):
                current_radius = [r * np.sqrt((initial_c*(lam**i))) for r in radius_dim]
                radius.append(current_radius)        
        return radius

def radius_without_r0(P, radius_dim, num_steps, lam):
        dimension = len(radius_dim)
        # radius_dim = np.array(radius_dim)

        radius = []
        # Initial radius is just the radius of the initial ball for each dimension

        initial_rad = [1.0 for i in range(dimension)]
        radius.append(initial_rad)

        # First, we need to use the initial ellispoid x'Px <= c to bound the ball 
        # of x'x <= initial_radius
        # That means, the minimum eigenvalue of x'(P/c)x <= 1 should be at least initial_radius
        # so, \sqrt{c}/\sqrt{max(eig(P))} >= initial_radius
        initial_c = max(np.linalg.eigvals(P))
        # radius_dim is the maximum value of each dimension for the ellipsoid x'Px <= 1
        # at the k-th step, the ellipsoid is x'Px <= lam^{i} * initial_c
        for i in range(1, num_steps+1):
                current_radius = [r * np.sqrt((initial_c*(lam**i))).real for r in radius_dim]
                radius.append(current_radius)        
        return radius 



def get_overapproximate_rectangles(A, B, Q_multiplier, num_steps):
        A = np.array(A)
        B = np.array(B)
        dimension = len(A)
        u_dimension = len(B[0])
        Q = Q_multiplier*np.eye(dimension)
        R = np.eye(u_dimension)     
        (X,L,G) = dare(A,B,Q,R) 

        AK = (A-np.dot(B,G))
        # print np.linalg.eigvals(AK)
        minimum_lam = max(abs(np.linalg.eigvals(AK)))

        E = np.sqrt(minimum_lam) * np.eye(dimension)#In general a function of A and B
        # Try to find P such that AK'PAK - EPE = -Q, which implies  AK'PAK \preceq EPE
        try:
                P = dlyap(np.transpose(AK),Q,None,E)
        except ValueError:
                print("Opps! Error finding the minimum spectral value")

        lam = minimum_lam

        radius_dim = ellipsoid_bounds(P)
        # print(radius_dim)

        # G is the -K matrix
        # print("----------------")
        # print(radius_array(P, initial_size, radius_dim, num_steps, lam))
        # print([[r1*initial_size, r2*initial_size] for [r1,r2] in radius_without_r0(P, radius_dim, num_steps, lam)])
        # print("----------------")


        return P, radius_dim, num_steps, lam, G
        # return radius_array(P, initial_size, radius_dim, num_steps, lam),G


def Dis_simulate(A,B,u_ref,X0):
        X = X0
        dimension = len(X0)
        for i in range(len(u_ref)):
                cur_step = np.reshape(np.dot(A,X[:,-1]),(dimension,1)) + np.reshape(np.dot(B,u_ref[i]),(dimension,1))
                X = np.append(X,cur_step,axis=1)
        return X


def demo():
        # A = [[0,2],[1,0]]
        # B = [[1],[1]]

        A = [[2.0001,-1],[1,0]] 
        B = [[0.0078125],[0]] 

        initial_size = 1.0
        num_steps = 10
        P, radius_dim, num_steps, lam, G = get_overapproximate_rectangles(A, B, 1000, num_steps)
        radius_list_original = radius_without_r0(P, radius_dim, num_steps, lam)
    
        radius = [[radius_per_dim * initial_size for radius_per_dim in radius] for radius in radius_list_original]
        print(radius)


        # The following is plotting to double check the result
        plot_flag = True
        plot_dim = 0

        # Random u_ref here
        u_ref = np.random.rand(num_steps,1)-0.5
        X0 = np.array([[1],[1]])

        X_ref = Dis_simulate(A,B,u_ref,X0)
        X_ref = np.array(X_ref)

        u_x = np.array([])
        for i in range(0,len(u_ref)):
                cur_input = u_ref[i] + np.dot(G,X_ref[:,i])
                u_x = np.append(u_x,cur_input)

        if plot_flag == True:
                fig = plt.figure()
                ax1 = fig.add_subplot(211)
                ax1.plot(u_ref)

                ax2 = fig.add_subplot(212)
                ax2.plot(X_ref[plot_dim,:],'k')

                for cnt in range(0,10):
                        X_test = Dis_simulate((A-np.dot(B,G)),B,u_x,X0+(np.random.rand(2,1)-0.5)*initial_size*2)
                        X_test = np.array(X_test)
                        ax2.scatter([i for i in range(0,len(u_ref)+1)],X_test[plot_dim,:])

                # Plot the error bar as the radius
                radius_dim1 = [ra[plot_dim] for ra in radius]
                ax2.errorbar([i for i in range(0,len(u_ref)+1)],X_ref[plot_dim,:],xerr=0,yerr=radius_dim1,color='red')
                fig.savefig('K_function_test.png')
        
        if plot_flag == False:
                fig = plt.figure()
                ax1 = fig.add_subplot(211)
                ax1.plot(u_ref)

                ax2 = fig.add_subplot(212)
                ax2.plot(X_ref[plot_dim,:],'k')

                for cnt in range(0,10):
                        X_test = Dis_simulate((A-np.dot(B,G)),B,u_x,X0+(np.random.rand(2,1)-0.5)*initial_size*2)
                        X_test = np.array(X_test)
                        ax2.scatter([i for i in range(0,len(u_ref)+1)],X_test[plot_dim,:])
                fig.savefig('test.png')

if __name__ == "__main__":
    # execute only if run as a script
    demo()
