
namespace RoboArmCalculations{
    using System;
    public class RACalc {
        private const float PI = 3.141592653589793f;
        private float binPow(float b, int e) {
            float result = 1;                     // default result 1, num^0 = 1
            while (e > 0) {                     // For non-zero, non-negative 'e'...
                if (e % 2 == 1){ result *= b; } // Multiply result by the b if 'e' is odd
                e >>= 1;                        // Left shift e by 1 bit
                b *= b;                         // Square the base
            }
            return result;
        }

        private int quickFac(int n){
            int sum = n;
            int nfac = n;
            for (int i = n - 2; i > 1; i-=2) {
                sum += i;
                nfac *= sum;
            }
            if (n % 2 != 0) {  nfac *= n / 2 + 1; }
            if(nfac == 0){ return 1; }
            return nfac;
        }

        public float asinApprox(float z){
            float aSin1 = 0.5f/3 * (float)binPow(z, 3);
            float aSin2 = 0.075f * (float)binPow(z, 5);
            float aSin3 = (float)5/112 * (float)binPow(z, 7);
            float aSin4 = (float)35/1152 * (float)binPow(z, 9);
            float aSin = z + aSin1 + aSin2 + aSin3 * aSin4;
            return aSin;
        }

        public float acosApprox(float z){
            float aSin = asinApprox(z);
            return (PI/2 - aSin);
        }

        public float atanApprox(float z){
            float aTan1 = binPow(z,3)/3; 
            float aTan2 = binPow(z,5)/5; 
            float aTan3 = binPow(z,7)/7; 
            float aTan4 = binPow(z,9)/9; 
            float aTan5 = binPow(z,11)/11; 
            float aTan6 = binPow(z,13)/13; 
            return (z - aTan1 + aTan2 - aTan3 + aTan4 - aTan5 + aTan6);
        }

        public float calcSqrt(float x){
            int i = 0;
            while ((i*i) <= x){
                i++;
            }
            i--;
            float d = x - i*i;
            float p = d / (2*i);
            float a = i + p;
            return a - (p * p) / (2 * a);
        }
        

        public double calcDistance(float pix, float piy, float pfx, float pfy){
            float dist = binPow((pfx - pix), 2) + binPow(pfy - piy, 2);
            return calcSqrt(dist);
        }
        public double roundTo(double num, double baseN){
            return baseN * (int)(num / baseN);
        }

        public Tuple<int,int> calculateJointAngles(int armLength, float distance){
            if(distance >= (int)(armLength * 2)){ return Tuple.Create(0, 180); }
            if(distance <= 0 ){ return Tuple.Create(90, 0); }

            float distSqrd = binPow(distance,2);
            int servoShoulderAngle = (int)(acosApprox( (float)(distSqrd / (2 * armLength * distance)) ) * 180/PI);
            int servoElbowAngle = (int)(180 - (servoShoulderAngle * 2));
            return Tuple.Create(servoShoulderAngle, servoElbowAngle);
        }

        public double calculateBaseAngle(double scrW, double scrH, double pntX, double pntY){
            int normPX = (int)roundTo(pntX - scrW / 2, 1);
            int normPY = (int)roundTo(scrH - pntY, 1);

            double angle = roundTo(atanApprox(normPX / normPY), 1.8);
            if(angle <= -90){ return -90; }
            else if(angle >= 90){ return 90; }
            return angle;
        }
    }
}