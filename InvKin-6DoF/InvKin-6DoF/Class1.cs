namespace InvKin_6DoF;
using static System.Math;
public static class AngleClac {
    private const double pi = Math.PI;
    private static double segment_3_x = 0;
    private static double segment_3_y = 0;

    public static double calculateDistance(double[] end_effector_pos, double[] reference_pos){
        double x_difference = end_effector_pos[0] - reference_pos[0];
        double y_difference = end_effector_pos[1] - reference_pos[1];
        double distance = Math.Sqrt( Math.Pow(x_difference, 2) + Math.Pow(y_difference, 2) );
        return distance;
    }

    private static double calcualte_x_segment_3(double end_effector_x, double segment_3_length, double end_effector_orientation){
        return end_effector_x - segment_3_length * Math.Acos(end_effector_orientation);
    }
    private static double calcualte_y_segment_3(double end_effector_y, double segment_3_length, double end_effector_orientation){
        return end_effector_y - segment_3_length * Math.Asin(end_effector_orientation);
    }
    private static double calculate_angle_segment_1(double segment_1_length, double segment_2_length){
        double end_effector_relative_angle = Math.Atan2( segment_3_y, segment_3_x );
        double numerator = Math.Pow(segment_3_x,2) + Math.Pow(segment_3_y,2) + Math.Pow(segment_1_length,2) - Math.Pow(segment_2_length,2);
        double denominator = 2 * segment_1_length * Math.Sqrt( Math.Pow(segment_3_x,2) + Math.Pow(segment_3_y,2) );
        double segment_1_angle = end_effector_relative_angle - Math.Acos( numerator / denominator );
        return segment_1_angle;
    }
    private static double calculate_angle_segment_2(double segment_1_length, double segment_2_length){
        double numerator = Math.Pow(segment_1_length,2) + Math.Pow(segment_2_length,2) - Math.Pow(segment_3_x,2) - Math.Pow(segment_3_y,2);
        double denominator = 2 * segment_1_length * segment_2_length;
        double segment_3_angle = pi - Math.Acos( numerator / denominator );
        return segment_3_angle;
    }
    private static double calculate_angle_segment_3(double end_effector_orientation, double segment_1_angle, double segment_2_angle){
        return end_effector_orientation - segment_1_angle - segment_2_angle;
    }
    private static void calcaulte_angle_base(){

    }
    private static double Rad2Deg(double rad){
        double degrees = rad * 180 / pi;
        return degrees;
    }

    public static double[] getAngles(double[] end_effector_vector, double[] reference_vector, double[] segment_lengths){
        /*
        double[] end_effector_vector = [ end_effector_x, end_effector_y, end_effector_orientation, arm_rotation ]
        double[] reference_vector = [ reference_x, reference_y, reference_rotation ]
        double[] segment_lengths = [ segment_1_length, segment_2_length, segment_3_length ]
        */
        segment_3_x = calcualte_x_segment_3(end_effector_vector[0], segment_lengths[2], end_effector_vector[2]);
        segment_3_y = calcualte_y_segment_3(end_effector_vector[1], segment_lengths[2], end_effector_vector[2]);
        double segment_1_angle = calculate_angle_segment_1(segment_lengths[0], segment_lengths[1]);
        double segment_2_angle = calculate_angle_segment_2(segment_lengths[0], segment_lengths[1]);
        double segment_3_angle = calculate_angle_segment_3(end_effector_vector[2], segment_1_angle, segment_2_angle);
        //double base_angle = calcualte_angle_base();

        double[] angles = new double[3]{Rad2Deg(segment_1_angle), Rad2Deg(segment_2_angle), Rad2Deg(segment_3_angle)};
        return angles;
    }
}
