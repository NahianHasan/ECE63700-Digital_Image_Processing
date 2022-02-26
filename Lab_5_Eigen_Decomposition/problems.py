import numpy as np
import numpy.random as nr
import matplotlib.pyplot as plt


################ Section 2.1 #################
def plot_figure(A,name,title):
	plt.figure()
	plt.plot(A[0,:],A[1,:],'.')
	plt.title(title)
	plt.axis('equal')
	plt.savefig(name+'.png')
	plt.savefig(name+'.tif')

N = 1000#number of samples
W = list()
Xi = list()
X = list()

mean = list((np.zeros((1,2))).squeeze())
cov = [[2,-1.2],[-1.2,1]]
[w,v] = np.linalg.eig(cov)
w = np.diag(np.sqrt(w))

for i in range(0,N):
	W_i = nr.multivariate_normal(mean, cov, size=1, check_valid='warn', tol=1e-8)
	X_i = np.matmul(w,np.transpose(W_i))
	W.append(W_i)
	Xi.append(X_i)
	X.append(np.matmul(v,X_i))
W = np.transpose((np.array(W)).squeeze())
Xi = np.transpose((np.array(Xi)).squeeze())
X = np.transpose((np.array(X)).squeeze())
print('W = ',W.shape)
print('Xi = ',Xi.shape)
print('X = ',X.shape)
plot_figure(W,'W','W')
plot_figure(Xi,'X',r'$\tilde{X}$')
plot_figure(X,'X','X')

################ Section 2.2 #################
mu_hat = (np.sum(X,axis=1))/N
mu_hat = np.reshape(mu_hat,[mu_hat.shape[0],1])
print('mu_hat = ',mu_hat.shape)
Z = X-mu_hat
print('Z = ',Z.shape)
R_hat = np.matmul(Z,np.transpose(Z))/(N-1)
print('R_hat = ',R_hat.shape)
print('R_hat = \n',R_hat)
[w,v] = np.linalg.eig(R_hat)
Xi_hat = np.matmul(np.transpose(v),X)
w = np.diag(1/np.sqrt(w))
W_hat = np.matmul(w,Xi_hat)


print('Xi_hat = ',Xi_hat.shape)
print('W_hat = ',W_hat.shape)
plot_figure(W_hat,'W_hat',r'$W_i$')
plot_figure(Xi_hat,'Xi_hat',r'$\tilde{X_i}$')

Rw_h = np.matmul(W_hat,np.transpose(W_hat))/N
print(Rw_h)
