import numpy as np
import fetchdata
from sklearn.svm import SVR


def svm_predict(days=10, offset=0, name='YHOO'):
    N = 100
    # Generate sample data
    X = np.arange(N).reshape(N, 1)
    y = fetchdata.get_data(name).ravel()
    Z = np.arange(N+offset, N+days+offset).reshape(days, 1)

    # Fit regression model
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.018)
    # svr_lin = SVR(kernel='linear', C=1e3)
    # svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    y_rbf = svr_rbf.fit(X, y).predict(Z)
    # y_lin = svr_lin.fit(X, y).predict(Z)
    # y_poly = svr_poly.fit(X, y).predict(Z)
    # print y_rbf
    # print y_lin
    # print y_poly
    a = [round(i, 3) for i in list(y_rbf)]
    return a

if __name__=='__main__':
    print svm_predict(15, 0, 'AAPL')
