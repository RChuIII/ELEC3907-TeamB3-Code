namespace CalcLib{
    using System;
    public static class CalculationLibrary{
        public double calcDistance(int pix, int piy, int pfx, int pfy){
            double dist = Math.Pow((pfx - pix), 2) + Math.Pow(pfy - piy, 2);
            return Math.Sqrt(dist);
        }
        public double roundTo(double num, double baseN){
            return baseN * Math.Round(Math.Floor(num / baseN));
        }

        public Tuple<int,int> calculateJointAngles(int armLength, int distance){
            if(distance >= Math.Round((double)armLength * 2)){ return Tuple.Create(0, 180); }
            if(distance <= 0 ){ return Tuple.Create(90, 0); }

            double distSqrd = Math.Pow(distance,2);
            int servoShoulderAngle = (int)Math.Acos( distSqrd / (2 * armLength * distance) );
            int servoElbowAngle = (int)(180 - (servoShoulderAngle * 2));
            return Tuple.Create(servoShoulderAngle, servoElbowAngle);
        }

        public double calculateBaseAngle(Tuple<int,int> scrRes, Tuple<int,int> pointCoords){
            int normPX = pointCoords.Item1 - scrRes.Item1 / 2;
            int normPY = scrRes.Item2 - pointCoords.Item2;

            double angle = roundTo(Math.Atan2(normPX, normPY) * 180/Math.PI, 1.8);
            if(angle <= -90){ return -90; }
            else if(angle >= 90){ return 90; }
            return angle;
        }
    }
}