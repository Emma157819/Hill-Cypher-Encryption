#include <iostream>
#include <cmath>
using namespace std;
int main(){
    int distance;
    int yards;
    int miles;
    int feet;

    cout<<" Hello, Please enter your distance in feet; ";
    cin>>distance;

     if(5280<=distance){
         miles=distance/5280;
         if(remainder(round(distance),5280)>3){
            yards= remainder(round(distance),5280)/3;
            if(remainder(remainder(round(distance),5280),3)>0){
                feet=remainder(remainder(round(distance),5280),3);
            }
         }
         cout<<"Your distance is "<<miles<<" mile(s) "<<yards<<" yard(s) "<<feet<<" foot/feet.";
    }

   
    else if(3<round(distance)<5279){
        yards=round(distance)/3;
        if(remainder(round(distance),3)>0){
        feet=remainder(round(distance),3);
        }
        cout<<"Your distance is "<<yards<<" yard(s) and "<<feet<<" feet(s)";
    }
     else if(round(distance)<3){
        cout<<"Your distance is "<<round(distance)<<" feet";
    }

    
    









    return 0;
}