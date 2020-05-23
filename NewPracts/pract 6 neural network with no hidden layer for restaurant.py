
import numpy as np
def activfun_sigmoid(x,deriv=False): # sigmoid function
    if(deriv==True):
        return x*(1-x)  #g'(z) Pg 727   
    return 1/(1+np.exp(-x))  #Log(z) Pg 725
    
#input data from hotel.csv with 4 feature columns & first 8 rows, 1-True, 0-False    
X = np.array([  [1,1,0,1],
                [0,0,0,0],
                [0,1,1,1],
                [1,1,1,1] ,
                [0,1,0,1],
                [0,1,0,0],
                [1,0,0,1],
                [0,1,0,0] ])

# result column, wait -> 0, Leave -> 1
y = np.array([[0,0,1,0,1,0,1,0]]).T

np.random.seed(1) #add this line if you want same output in multliple executions
# initialize weights randomly with values between -1 to 1 with mean 0
w0 = 2*np.random.random((4,1)) - 1
#OR you may just set them to random values
#w0 = np.random.random((4,1)) 
print("initial weights - \n", w0)
for n in range(1000):
    l_input = X  # x
    
    #feed forward
    l_output = activfun_sigmoid(l_input.dot(w0)) #h(x)

    #Error calculation  
    l_output_error = y - l_output #(y-h(x)) 
    l_output_delta = l_output_error * activfun_sigmoid(l_output,True) # (y-h(x))  * ( h(x)*(1-h(x)))         
    
    #Backpropagation and updating w   
    w0 = w0 + 2*l_input.T.dot(l_output_delta) # Eqn 18.8 Pg-727 where alpha is 2

print("final weights - \n", w0)
print( "Output After Training:")
print (l_output)
print ("Loss: \n" + str(np.mean(np.square(y - l_output))))
