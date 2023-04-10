# Copyright (c) 2023 OMRON SINIC X Corporation
# Author: Shuwa Miura, Kazumi Kasaura
from .quadratic_constraint import QuadraticConstraint
import torch as th

import cvxpy as cp
import gurobipy as gp
import math

from ..cvxpy_variables import CVXPYVariables
from .power_constraint import make_compatible

class TipConstraint(QuadraticConstraint):

    """
    State-dependent Action Constraints with the from
    $a_0^2+2a_0(a_0+a+1)\cos\theta_2+(a_0+a_1)^2$.
    """

    def __init__(self, max_M, **kargs):
        super().__init__(max_M, 2, 9, **kargs)
        
    def getTensorQ(self, states):
        Q=th.zeros((states.shape[0],2,2),device = states.device)
        cosg = th.cos(states[:,7])
        Q[:,0,0] = 2 + 2 *cosg
        Q[:,0,1]=Q[:,1,0]=1+cosg
        Q[:,1,1]=1
        return Q

    
    def cvxpy_constraints(self, x, state = None):
        cons = [cp.square(x[0])+cp.square(x[0]+x[1])+2*x[0]*(x[0]+x[1])*
                (1-cp.power(state[7],2)/2+cp.power(state[7],4)/24
                 -cp.power(state[7],6)/720+cp.power(state[7],8)/40320
                 -cp.power(state[7],10)/3628800+cp.power(state[7],12)/479001600)
                <= self.max_M]
        print(cons)
        return cons

    def gp_constraints(self, model, x, s):
        Sq = gp.QuadExpr()
        cosg = math.cos(s[7])
        Sq+=x[0]*x[0]+(x[0]+x[1])*(x[0]+x[1])+2*x[0]*(x[0]+x[1])*cosg
        model.addConstr(Sq <= self.max_M)


if __name__ == "__main__":
    constraint = TipConstraint(0.05)
    states=th.tensor([[ 1.8320e-01, -1.5764e-01, -3.7405e-02,  1.0267e-02,  5.1187e-01,
         -8.5906e-01, -4.5078e-01,  1.5164e-01,  8.1063e-01],
        [-1.2841e-01, -1.0619e-01,  5.6862e-02, -6.6311e-02,  8.9963e-02,
         -9.9595e-01, -1.0231e-01, -3.3542e-01, -3.3383e-01],
        [-9.6614e-02,  1.2436e-01, -8.8864e-02, -2.5948e-02, -8.8712e-01,
          4.6154e-01,  1.6002e-01, -8.9188e-03, -3.7412e-01],
        [ 1.4109e-01,  4.5607e-02, -1.0881e-01,  2.2218e-02, -6.8323e-01,
          7.3020e-01, -8.2575e-01, -7.5437e-01,  9.2613e-01],
        [ 1.3156e-01,  1.1313e-01, -2.3143e-02,  8.6857e-03,  2.8196e-02,
          9.9960e-01, -1.3445e-01, -4.4995e-01,  9.2404e-02],
        [ 2.3610e-01,  2.7571e-02, -1.5175e-01,  4.3976e-02, -1.9267e-01,
          9.8126e-01, -2.0409e-01, -6.7312e-01,  9.9564e-02],
        [ 9.5906e-02, -7.2765e-02, -1.8310e-01,  1.1592e-01, -7.9309e-01,
         -6.0911e-01, -4.1237e-01, -7.7382e-01, -8.4190e-01],
        [-2.6493e-02, -1.1129e-01, -9.7531e-02,  2.8042e-01, -5.3531e-01,
          8.4466e-01, -8.9416e-02,  4.6762e-02,  2.3578e-01],
        [ 5.2737e-02, -1.6635e-01,  6.7426e-02,  2.9614e-01,  2.0968e-01,
          9.7777e-01, -3.9352e-01, -3.8360e-01, -6.4619e-02],
        [ 4.1588e-02, -9.6503e-02, -1.0680e-01,  4.2423e-02,  3.3904e-01,
         -9.4077e-01, -2.5552e-01, -7.7012e-01,  3.5925e-02],
        [-1.9536e-01, -1.0919e-01,  2.3155e-01,  4.2231e-02, -7.3762e-01,
         -6.7522e-01,  4.2337e-03,  8.1003e-01,  1.4798e-01],
        [-1.7193e-01,  2.6708e-01,  1.2781e-01, -1.5978e-01,  6.0622e-01,
          7.9529e-01,  1.0703e-01,  6.4415e-01, -2.5370e-01],
        [ 2.1081e-01,  1.8435e-01, -3.6944e-02, -6.6586e-02,  8.3082e-01,
          5.5654e-01,  1.1817e-02, -4.0813e-04, -8.9231e-02],
        [-2.2798e-01,  2.6716e-02,  2.2169e-01, -1.4165e-02, -3.5069e-01,
         -9.3649e-01,  1.9723e-02, -1.0159e+00,  0.0000e+00],
        [ 1.4427e-01,  1.2218e-01,  1.6949e-02, -1.1593e-04,  9.3954e-01,
          3.4243e-01, -7.1718e-02,  1.8670e-01,  8.1036e-02],
        [ 2.4308e-01,  1.5988e-01, -7.6241e-02, -5.8548e-02,  9.8955e-01,
          1.4416e-01, -2.4803e-02,  2.5290e-01,  1.4468e-02],
        [-2.1995e-01,  2.4489e-01,  4.7054e-02, -2.8255e-01, -9.1998e-01,
          3.9196e-01, -1.0542e-01,  3.7617e-01, -6.1844e-02],
        [ 9.5906e-02, -7.2765e-02, -8.4770e-02,  7.7624e-02, -9.5543e-01,
          2.9520e-01, -4.4436e-01, -1.0253e+00,  0.0000e+00],
        [-1.6567e-02, -1.1778e-01, -6.0481e-02,  1.3783e-01, -5.1129e-01,
         -8.5941e-01, -7.7052e-02, -8.3015e-01, -7.3317e-01],
        [ 1.8572e-01,  2.0678e-01, -7.9348e-03, -1.5137e-01,  9.7423e-01,
         -2.2557e-01, -1.4413e-01,  3.3027e-01,  1.7400e-01],
        [ 1.9805e-01, -1.2779e-01, -3.2554e-04,  6.6961e-02,  8.8112e-01,
         -4.7289e-01, -7.6104e-02,  1.1023e-01, -9.5515e-02],
        [ 2.4602e-02, -2.1116e-01, -2.6810e-02,  1.9340e-01,  7.7527e-01,
          6.3163e-01,  1.7385e+00, -1.0000e+00,  3.9291e-14],
        [ 2.0714e-01, -1.5270e-02, -6.5214e-03, -4.7860e-03,  9.2134e-01,
         -3.8875e-01, -1.1639e-02,  1.8540e-01, -6.9389e-02],
        [ 2.0401e-01,  1.3602e-01, -3.3934e-01, -1.8223e-01, -4.0614e-01,
         -9.1381e-01, -3.0699e-01, -5.8965e-01, -7.4583e-01],
        [-7.5421e-02, -1.6144e-02,  4.1996e-02,  5.0506e-03,  4.3251e-01,
         -9.0163e-01,  2.7007e-02, -9.3872e-01,  1.2478e-02],
        [ 1.0846e-01,  9.9337e-02, -3.3758e-02, -6.2992e-02, -1.1327e-01,
          9.9356e-01, -2.7986e-01, -7.5972e-01,  3.2931e-01],
        [-5.8949e-02, -2.0931e-01,  7.5779e-02,  2.1469e-01, -8.3897e-01,
          5.4417e-01,  9.4286e-01, -1.0007e+00,  3.1399e-03],
        [ 1.9137e-01, -2.1385e-01, -7.0773e-03,  1.8877e-01,  7.9730e-01,
         -6.0358e-01, -2.6127e-02,  3.1761e-01, -8.4677e-02],
        [-2.5788e-01, -1.5271e-01,  2.5780e-01,  2.1453e-01,  9.9917e-01,
         -4.0851e-02, -1.1021e+00,  9.0781e-01,  1.0428e+00],
        [-2.2205e-01,  3.0545e-02,  2.3723e-01, -3.8390e-02, -8.8281e-01,
         -4.6973e-01, -2.8692e-01,  9.9921e-01, -7.1263e-02],
        [ 1.1406e-01,  3.0687e-02,  1.2989e-03,  2.3440e-02,  1.5227e-01,
          9.8834e-01, -2.1426e-02, -6.1160e-01,  3.4739e-02],
        [ 5.9732e-02,  2.5014e-01, -4.0865e-02, -2.4222e-01, -7.4692e-01,
          6.6491e-01,  1.3502e-01, -1.0045e+00, -2.5752e-01],
        [-1.9243e-01,  1.4527e-01,  1.9735e-01, -1.6079e-01,  6.6832e-01,
          7.4387e-01, -4.0629e-01, -1.0051e+00,  2.3042e-02],
        [ 4.6327e-02,  3.0584e-02, -5.0195e-02, -1.7612e-01, -8.3896e-01,
         -5.4420e-01, -6.8624e-01,  4.9996e-01, -6.7928e-01],
        [-2.6227e-01, -1.8429e-01,  2.7370e-01,  1.7832e-01, -9.9454e-01,
          1.0437e-01, -2.0936e+00,  1.0213e+00,  0.0000e+00],
        [-1.4551e-01,  4.4989e-02,  1.4488e-01, -1.6085e-01,  8.7471e-01,
         -4.8465e-01,  6.0875e-02, -6.6676e-01, -1.4619e-01],
        [ 1.3737e-01,  1.3935e-01,  6.1545e-03, -1.3965e-01,  6.3909e-01,
         -7.6913e-01, -2.9661e-02,  5.4604e-01, -5.3186e-03],
        [ 2.5603e-01, -1.4094e-01, -7.4301e-02,  1.7236e-01,  9.3303e-01,
         -3.5981e-01, -8.5294e-02,  3.2390e-01, -1.6248e-01],
        [-1.0117e-01, -1.9024e-01,  7.8590e-02,  2.4379e-01, -9.5423e-01,
         -2.9906e-01,  8.9652e-02, -8.7500e-01, -2.1984e-01],
        [-1.7206e-01, -7.8571e-02,  1.6677e-01, -4.6847e-02, -8.4842e-01,
         -5.2933e-01,  1.4997e-01,  6.2589e-01,  8.7443e-02],
        [ 2.5588e-01, -1.6800e-01, -4.1788e-01,  2.4987e-01, -9.9468e-01,
         -1.0298e-01,  9.5747e-02, -3.6193e-01, -1.8553e-01],
        [ 7.6981e-02, -3.5777e-02, -8.0278e-02,  5.5422e-02, -8.6179e-01,
         -5.0727e-01, -4.6081e-01, -1.0090e+00, -3.0229e-01],
        [ 3.1120e-02, -2.1374e-02, -1.1562e-01,  6.8736e-02,  1.5641e-01,
          9.8769e-01, -1.9128e-01,  7.5827e-01,  5.3134e-01],
        [ 2.6689e-01, -1.3015e-01, -1.5124e-01, -3.3241e-02,  3.0154e-01,
         -9.5345e-01,  7.7906e-02,  2.0443e-01, -9.1836e-03],
        [ 1.5794e-01, -1.6047e-01, -1.7740e-01,  1.4733e-01,  8.5832e-01,
         -5.1312e-01,  6.1850e-01, -9.6909e-01,  1.9071e-01],
        [ 1.9805e-01, -1.2779e-01, -8.8190e-02, -5.1159e-02,  4.8637e-01,
         -8.7375e-01, -1.6041e-01,  8.5268e-05, -1.8568e-01],
        [-2.3627e-01, -1.8825e-01,  2.3476e-01,  3.5532e-01,  7.3609e-01,
          6.7689e-01, -8.9894e-01,  4.8513e-01,  9.2152e-01],
        [-8.0491e-04,  2.5744e-01, -3.3972e-02, -2.0605e-01,  7.4207e-01,
          6.7032e-01, -1.0938e-02,  8.2298e-01, -4.8571e-01],
        [-1.4558e-01,  5.6405e-02,  9.1604e-03,  8.7207e-02, -9.0843e-01,
          4.1803e-01,  1.4570e-01, -2.5292e-01, -4.8987e-01],
        [ 1.5794e-01, -1.6047e-01, -1.6855e-01,  1.7482e-01, -3.4020e-01,
         -9.4035e-01,  3.9129e-01, -1.0001e+00,  5.8146e-04],
        [-1.0272e-01,  1.3983e-01,  1.1016e-01, -7.2283e-02, -9.6495e-01,
          2.6245e-01,  1.8502e-01, -8.6011e-01, -5.5235e-01],
        [ 1.8644e-01,  1.6413e-02, -1.8327e-01, -2.6501e-02,  1.2385e-01,
          9.9230e-01, -4.8969e-01,  1.0581e+00,  0.0000e+00],
        [-2.2467e-01,  1.2656e-01,  1.2444e-01, -1.1338e-01, -2.6591e-01,
          9.6400e-01, -8.1238e-02,  6.2769e-01, -1.5642e+00],
        [ 1.0696e-01,  2.5812e-01, -1.1316e-01, -2.5016e-01,  6.6828e-01,
         -7.4391e-01,  1.3040e+00, -1.0428e+00,  0.0000e+00],
        [-5.2173e-02, -1.4447e-01,  1.8761e-01,  2.3472e-01,  2.7679e-01,
          9.6093e-01, -1.2907e-01, -4.3628e-01,  3.6993e-01],
        [-1.2841e-01, -1.0619e-01,  6.4605e-02,  1.3630e-01, -5.8368e-01,
         -8.1198e-01,  1.3919e-01, -7.8860e-01,  5.8789e-01],
        [ 2.1081e-01,  1.8435e-01, -4.8475e-02, -7.2713e-02,  9.6667e-01,
          2.5603e-01,  1.6961e-01,  2.2385e-01, -2.1960e-01],
        [ 1.1092e-01,  2.4205e-01, -2.1314e-02, -5.4704e-02,  5.6766e-01,
          8.2326e-01, -6.6414e-03,  9.6259e-02, -5.9421e-02],
        [ 1.9046e-01,  1.6985e-01, -2.7190e-02, -4.0215e-02,  8.4937e-01,
          5.2780e-01,  6.8751e-02,  7.4697e-02, -1.0401e-01],
        [ 1.0989e-01, -1.0523e-01, -3.6461e-02,  4.2261e-02, -2.8819e-01,
         -9.5757e-01,  1.9405e-01,  7.3822e-01,  1.5771e-01],
        [ 1.6965e-01,  2.0781e-01, -6.6745e-02, -3.5913e-01,  8.9288e-01,
         -4.5029e-01, -2.0470e-01, -3.7416e-01, -5.7983e-01],
        [-5.1685e-02,  5.0972e-02, -6.5238e-02, -7.5389e-02, -3.5952e-01,
         -9.3314e-01, -2.3778e-01, -6.4139e-01,  6.4520e-02],
        [-2.0239e-01, -8.1387e-02,  3.2574e-01,  1.2562e-01,  2.2458e-01,
          9.7446e-01,  2.5393e-01, -6.0578e-01, -1.2533e-01],
        [-7.5421e-02, -1.6144e-02,  5.0420e-02,  1.9265e-02,  1.9355e-01,
         -9.8109e-01,  1.4493e-01, -9.7084e-01,  4.9250e-02],
        [ 1.6701e-01,  9.1604e-02, -4.0769e-02, -3.0067e-02,  2.4395e-01,
          9.6979e-01, -1.3173e-01, -5.1368e-01,  8.3635e-01],
        [ 1.3156e-01,  1.1313e-01, -1.5625e-01, -8.0319e-02, -7.8229e-01,
         -6.2291e-01, -1.3983e-01, -9.4268e-01, -4.1545e-01],
        [-5.8949e-02, -2.0931e-01,  3.9744e-02,  2.0774e-01,  4.9230e-01,
         -8.7042e-01, -1.9549e-01, -9.6385e-01,  5.6265e-01],
        [-5.2173e-02, -1.4447e-01,  1.2499e-01,  2.6095e-01,  9.9971e-01,
          2.3921e-02, -4.4858e-01,  6.3995e-01,  1.2230e+00],
        [ 7.0893e-02,  1.2322e-02, -6.4323e-02, -2.0734e-02, -3.3465e-01,
          9.4234e-01,  3.2380e-01, -1.0351e+00,  3.5233e-03],
        [-2.0239e-01, -8.1387e-02,  2.9158e-01,  1.4889e-01, -2.0730e-01,
          9.7828e-01,  2.7321e-01, -6.8015e-01, -1.1346e-01],
        [ 5.2737e-02, -1.6635e-01, -5.1120e-02,  1.7999e-01,  5.2518e-01,
         -8.5099e-01, -7.9028e-01,  1.0173e+00,  0.0000e+00],
        [ 2.6689e-01, -1.3015e-01, -1.4593e-01, -2.6749e-02,  2.8306e-01,
         -9.5910e-01, -8.8583e-02,  2.2614e-01,  9.3122e-03],
        [-1.2841e-01, -1.0619e-01,  1.0166e-01, -9.9029e-02, -3.6151e-01,
         -9.3237e-01, -3.7250e-01,  2.0520e-01,  1.6625e+00],
        [ 2.5431e-01, -1.1782e-01, -2.4572e-01,  1.0933e-01, -1.4669e-01,
          9.8918e-01, -9.8805e-02,  1.0685e+00, -2.9642e-03],
        [-2.2370e-01, -1.5470e-01,  1.4518e-01, -1.8860e-02,  1.1537e-01,
         -9.9332e-01,  5.0572e-01, -3.2005e-01, -5.4727e-01],
        [-1.7176e-01,  1.8518e-01,  1.3073e-01, -9.9114e-02,  6.6989e-01,
          7.4246e-01,  1.0031e-01,  7.2699e-01, -1.3682e-01],
        [ 1.8644e-01,  1.6413e-02, -1.9379e-01,  3.6640e-02,  9.8955e-01,
          1.4419e-01, -3.9230e-01,  8.3653e-01, -7.5699e-01],
        [ 1.6254e-01, -1.5441e-01, -1.3764e-01, -4.6595e-02, -1.7109e-01,
         -9.8526e-01, -8.7949e-02,  1.6710e-01, -2.0584e-01],
        [-1.7772e-02,  5.5986e-02,  4.0756e-02, -1.2489e-01, -8.5372e-01,
         -5.2073e-01,  3.2339e-02,  7.9590e-01, -3.2529e-01],
        [ 1.3156e-01,  1.1313e-01,  2.7841e-02,  1.9793e-02,  8.6371e-01,
          5.0399e-01, -3.9161e-02,  1.0646e-01,  8.0312e-02],
        [-9.6614e-02,  1.2436e-01, -7.4913e-02, -1.5917e-01, -6.8609e-01,
         -7.2752e-01, -2.0491e-02, -3.8136e-01,  1.7209e-01],
        [ 5.3381e-02,  1.5518e-01,  5.2611e-02, -3.5173e-02,  9.9240e-01,
          1.2306e-01,  1.2814e-01,  4.6558e-01, -7.6158e-02],
        [ 2.5244e-01,  8.4347e-02, -4.0940e-01, -4.9351e-02, -9.4536e-01,
         -3.2602e-01, -1.1401e+00, -3.7587e-01,  1.6452e+00],
        [ 2.5780e-01, -1.5807e-01, -1.0912e-01,  5.0225e-02,  3.6717e-01,
         -9.3015e-01, -2.0676e-01,  3.2349e-01, -2.6042e-01],
        [-1.7057e-01, -2.5330e-01,  1.0561e-01,  2.2011e-01,  2.0264e-01,
         -9.7925e-01, -2.7661e-01, -7.8458e-01,  5.1177e-01],
        [ 4.8916e-02, -1.0787e-01, -5.0131e-02,  1.2707e-01,  9.3071e-01,
         -3.6576e-01,  1.7344e-01,  9.8406e-01, -1.9716e-01],
        [ 2.0202e-01, -3.9029e-03, -8.9125e-02, -1.7311e-01,  5.5159e-01,
         -8.3411e-01, -4.0858e-02, -3.5048e-03,  2.0575e-01],
        [ 2.0809e-01,  1.7872e-01, -5.5922e-02, -7.2710e-02,  9.9367e-01,
          1.1230e-01,  1.1095e-01,  3.2193e-01, -7.3183e-02],
        [ 1.1997e-01, -1.2303e-01, -6.6191e-02,  2.8993e-02,  9.9807e-01,
          6.2107e-02,  2.0943e-02, -6.8947e-01, -4.2546e-02],
        [ 9.4314e-02, -2.0381e-01, -1.2926e-01,  1.8637e-01,  5.5225e-01,
         -8.3368e-01,  2.9412e-01, -8.9692e-01,  5.3850e-01],
        [ 1.3156e-01,  1.1313e-01, -6.3705e-02,  6.6367e-03, -3.4719e-01,
          9.3779e-01, -2.5571e-01, -5.5399e-01,  3.1866e-01],
        [-2.4580e-01,  9.2489e-02,  4.7536e-02, -2.3359e-02, -9.2019e-01,
          3.9148e-01, -2.9157e-01,  2.8959e-02,  3.1105e-01],
        [ 2.4662e-01, -8.7919e-02, -2.9131e-01,  1.0427e-01, -2.7906e-01,
         -9.6027e-01,  5.1581e-01, -8.8904e-01,  1.6501e-01],
        [ 4.1381e-02,  9.9785e-02,  1.3328e-01, -1.9956e-01,  9.7123e-01,
         -2.3813e-01, -1.6613e-01, -1.6541e-01,  5.2801e-01],
        [ 4.9837e-02, -3.2174e-02, -3.3871e-02,  2.2361e-02,  4.5312e-02,
          9.9897e-01,  1.2342e-01, -9.9689e-01, -2.0943e-03],
        [ 4.6537e-02,  2.6297e-01, -3.5891e-02, -5.3864e-02,  1.3673e-01,
          9.9061e-01, -3.2710e-02,  5.7895e-02,  1.1680e-01],
        [ 1.9656e-02,  7.1967e-02,  1.8609e-02, -1.0322e-01, -6.0140e-01,
         -7.9895e-01,  3.1162e-02,  8.7325e-01, -3.4123e-01],
        [-5.9224e-02, -1.9975e-01,  9.1893e-02,  1.6842e-01,  6.4324e-01,
          7.6567e-01,  3.6364e-01, -9.6045e-01, -9.9280e-01],
        [ 4.6537e-02,  2.6297e-01, -9.1370e-02, -2.7300e-01, -1.4171e-01,
          9.8991e-01, -4.7941e-01,  9.6689e-01,  1.1510e+00],
        [ 1.5794e-01, -1.6047e-01, -2.7301e-02, -2.8689e-04,  4.5119e-01,
         -8.9243e-01, -2.4893e-01,  1.0593e-01, -7.7573e-02]])

    Q = constraint.getQ(states)

    v = th.tensor([[ 1.1877, -2.3243],
        [ 1.7959, -4.3229],
        [ 0.7542, -1.9867],
        [ 0.9488, -1.2668],
        [ 0.3369, -0.3681],
        [-1.5717,  2.3981],
        [ 2.3537, -2.5683],
        [-1.5644,  3.7083],
        [ 0.7733, -1.5146],
        [ 4.5917, -8.2694],
        [-0.1183, -1.0292],
        [ 1.2631, -2.6133],
        [-0.5344,  1.4256],
        [-2.9314,  5.5788],
        [ 0.4514, -1.0473],
        [ 0.3028, -0.6701],
        [-1.3386,  1.1386],
        [-1.4933,  2.7295],
        [ 4.0325, -7.6104],
        [-0.7822,  2.7495],
        [-0.0188,  0.5993],
        [-3.4582,  6.0066],
        [ 0.0167,  0.0568],
        [-1.6121,  1.3926],
        [-0.9225,  1.0189],
        [ 0.6311, -0.5272],
        [ 1.2427, -2.7783],
        [ 1.0319, -2.5678],
        [-5.2975, 10.0474],
        [ 1.4269, -2.9111],
        [ 0.3023, -0.9060],
        [-2.8003,  5.5046],
        [ 0.3941, -1.4517],
        [ 1.8764, -3.7361],
        [-2.7421,  4.9254],
        [-0.7130,  0.3959],
        [ 0.9533, -0.9312],
        [ 0.5112, -1.0822],
        [ 2.9078, -5.0902],
        [ 0.8757, -2.0521],
        [ 3.8278, -7.8939],
        [ 1.2113, -2.0263],
        [-2.8169,  5.3518],
        [ 0.8417, -1.0173],
        [-3.6530,  5.9265],
        [-5.9884, 11.9783],
        [-3.8574,  9.2997],
        [ 1.2505, -1.8271],
        [-0.9896,  2.3350],
        [ 3.4117, -4.8462],
        [-0.1826,  1.3147],
        [-0.7548,  1.0839],
        [-1.2892,  2.9177],
        [-2.1583,  3.2695],
        [-2.7347,  5.7706],
        [-0.6775,  1.0023],
        [ 0.5251, -1.4952],
        [-0.0960,  0.5027],
        [ 0.4441, -1.2032],
        [ 0.5062, -1.0083],
        [ 2.8411, -7.2339],
        [ 0.2819, -2.3598],
        [ 2.6288, -4.4024],
        [-2.0797,  3.3121],
        [ 0.9550, -2.2754],
        [-1.2370,  0.9994],
        [ 2.3387, -3.4464],
        [-2.7986,  5.9041],
        [-1.1930,  2.0790],
        [ 2.5329, -4.1267],
        [ 2.1468, -3.7458],
        [-0.2907,  1.5725],
        [ 2.2964, -4.7565],
        [-6.6629, 12.4310],
        [ 1.6675, -3.2404],
        [ 1.9704, -4.1947],
        [ 0.3274, -0.3166],
        [-4.1403,  8.6956],
        [-1.8100,  3.6279],
        [ 1.1904, -2.6021],
        [-1.3071,  1.7721],
        [ 0.8844, -1.8934],
        [ 1.8460, -3.0603],
        [-2.9637,  6.1326],
        [ 2.1313, -3.7318],
        [-3.3370,  5.8759],
        [ 0.0935,  0.0552],
        [ 0.8720, -2.2909],
        [-0.8439,  2.3420],
        [-1.0208,  0.9889],
        [ 0.3767, -0.4332],
        [-0.0614,  0.7950],
        [ 3.1372, -5.7051],
        [-1.2770,  3.3321],
        [-1.0459,  1.6059],
        [ 0.3424, -0.7144],
        [-0.5434,  2.0249],
        [-3.5058,  5.6909],
        [-4.1882,  7.5286],
        [-5.5352, 11.1384]])
    
    value = (v[:,:,None]*Q*v[:,None,:]).sum(dim=2).sum(dim=1)
    L = th.sqrt((value+1e-9)/constraint.max_M)
    print(value, L)
    