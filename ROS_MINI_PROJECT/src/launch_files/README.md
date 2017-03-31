Steps for getting the pioneer running on gazebo

1. use rosdep to install dependencies. cd to your catkin_ws  and run the following command.
rosdep install --from-paths src --ignore-src --rosdistro=indigo -y

2. Launch /launch/mini_project.launch to bringup the gazebo environment.

