import numpy as np
import fetchdata
from sklearn.neural_network import MLPRegressor


def mlp_predict(days, offset, name='YHOO'):
    N = 100
    # Generate sample data
    X = np.arange(N).reshape(N, 1)
    y = fetchdata.get_data(name).ravel()
    Z = np.arange(N + offset, N + days + offset).reshape(days, 1)

    # Fit regression model
    mlp_adam = MLPRegressor(algorithm='l-bfgs', activation='logistic')
    y_log = mlp_adam.fit(X, y).predict(Z)
    a = [round(i, 3) for i in list(y_log)]
    return a

if __name__=='__main__':
    print mlp_predict(15, 0, 'AAPL')
