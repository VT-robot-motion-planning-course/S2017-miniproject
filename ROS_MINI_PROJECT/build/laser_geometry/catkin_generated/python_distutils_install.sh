#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/aravind/ROS_MINI_PROJECT/src/laser_geometry"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/aravind/ROS_MINI_PROJECT/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/aravind/ROS_MINI_PROJECT/install/lib/python2.7/dist-packages:/home/aravind/ROS_MINI_PROJECT/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/aravind/ROS_MINI_PROJECT/build" \
    "/usr/bin/python" \
    "/home/aravind/ROS_MINI_PROJECT/src/laser_geometry/setup.py" \
    build --build-base "/home/aravind/ROS_MINI_PROJECT/build/laser_geometry" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/aravind/ROS_MINI_PROJECT/install" --install-scripts="/home/aravind/ROS_MINI_PROJECT/install/bin"
