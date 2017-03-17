Steps for getting the pioneer running on gazebo

1. Make sure Nav Stack and gmapping are installed.

 gmapping: sudo apt-get install ros-indigo-slam-gmapping
 	wiki: http://wiki.ros.org/gmapping

 navstack: sudo apt-get install ros-indigo-navigation
 	wiki: http://wiki.ros.org/navigation

2. Launch /launch/pioneer_gazebo_navigation.launch to bringup the gazebo environment.
3. Launch /pioneer_2dnav/launch/move_base_gmapping.launch to launch move_base and gmapping.
4. Launch /p3dx_description/launch/rviz.launch to launch rviz and visualize the robot
