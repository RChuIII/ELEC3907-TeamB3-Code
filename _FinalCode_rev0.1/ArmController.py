"""
Required Modules:
    //-> Write calibration code for accelerometer
    //-> Read Accelerometer data from bluetooth device
    //-> Clean up the maths code
    //-> write a better python main program.
    ->Thursday-> Integrate accelerometer and bluetooth moduels
    -> Accelerometer to maths(
"""

"""
Arm-Glove System
    -> Glove(arduino nano) sends signal via bluetooth
        -> Sent signals:
            -> [glove_XTilt, glove_YTilt, axis_mode, claw_acutation, claw_rotation]
            -> [analog, analog, digital, analog, digital]

    -> Raspberry PI recieves data
    -> Raspberry PI parses data
        -> Takes glove_XTilt, golve_YTilt, and axis_mode to calculate position
        -> Takes claw_rotation to determine if 0_deg or 90_deg rotation

    -> Raspberry PI sends data to arduino Mega
        -> [stepper_pos, servo_sh_pos, servo_el_pos, servo_wr_pos, servo_cr_pos, servo_cl_pos]
        -> Stepper position, shoulder position, elbow position, wrist position, claw rotation, claw grip

    -> Arduino Mega sends data to servo/stepper drivers
    
    -> Arduino mega sends feedback information
        -> proximity sensor stop signal
        -> claw proximity sensor (obj within claw grip)
"""