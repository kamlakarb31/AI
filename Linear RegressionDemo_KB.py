import statistics

class RegressionDemo :
    def __init__(self, a,b,):
        self.x = a #number of hours of study per day
        self.y = b # some value based on function h with w0=1, w1=2        
        self.w0 = 0
        self.w1 = 0
        
    def h(self, w0, w1): # function h as per 18.6.1 univariate linear regression
        hresult= []
        for i in range(0 , len(self.x)):
            hresult.append(w0 + w1*self.x[i]) 
        return hresult

    def checkresult(self, hresult):
        #print(hresult)
        for i in range(0 , len(self.x)) :
            if ( abs(hresult[i] - self.y[i]) >= 10 ) :#this terminating condition is different from book
                return False
        return True
            
    def training(self, w0, w1, alpha):
        i=1

        while True :          
            hresult = self.h(w0,w1)                
            if(self.checkresult(hresult)) :      
                self.w0 = w0
                self.w1 = w1                    
                print("In Attempt number ", i,  ", i got it! I think i have learnt enough: w0-->", self.w0, ", w1-->", self.w1)
                print("My result : ", hresult)
                break

            t0=0
            t1=0
            for j in range(0,len(self.x)) :
                t0 = t0 + (self.y[j] - hresult[j]) 
                t1 = t1 + (self.y[j] - hresult[j]) *self.x[j]
                

            i = i +1      
            w0 = w0 + alpha * t0
            w1 = w1 + alpha * t1
               

            if( i % 10000 ==0):
                print(hresult)
                ans = input("I am exhausted, tried 10000 iterations! should i stop(y)? ")
                if(ans=='y'):
                    break
            
        
        
a = [18.5, 16, 17, 20, 15, 19, 18, 15.5, 19.3] # Length of palm in cm
b = [188, 167, 171, 180, 154, 177, 170, 167, 185] # Height of person in cm
p = RegressionDemo(a,b)
print("Length of palm(in cm)=", p.x)
print("height (in cm)=", p.y)



print("\ntrying with w0=10, w1=20, alpha=0.0004 -->")
p.training(10, 20, 0.0004)
print( "Harshal's height is = ", (p.w0 + p.w1*19)) # 19 is harshal's length of palm, we are trying to predict his height based on our model


print("\ntrying with w0=50, w1=2, alpha=0.00035 -->")
p.training(50, 2, 0.00035)
print( "Harshal's height is = ", (p.w0 + p.w1*19))  # 19 is harshal's length of palm, we are trying to predict his height based on our model



'''
mydata <- data.frame( palm=c(18.5, 16, 17, 20, 15, 19, 18, 15.5, 19.3),
                      height=c(188, 167, 171, 180, 154, 177, 170, 167, 185)
                      )
shapiro.test(mydata$palm)
mymodel <- lm(height~palm,data = mydata)
print(mymodel)
summary(mymodel)

png(file = "linearregression.png")
plot(mydata$palm,mydata$height,col = "blue",main = "Height & palm length Regression",
     abline(lm(height~palm,data = mydata)),cex = 1.3,pch = 10,xlab = "palm length",ylab = "Height in cm")
dev.off()

mydata$fitted <- fitted(mymodel)
mydata

newdata <- data.frame( palm=c(19),
                       height=c(182)
)
newdata$pred<-predict(mymodel,newdata)  
newdata

'''






