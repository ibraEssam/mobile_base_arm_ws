ARG FROM_IMAGE=osrf/ros:jazzy-desktop-full
FROM ${FROM_IMAGE}

# Delete default user
RUN userdel ubuntu


COPY src ./src
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    apt-get update && rosdep install -q -y \
    --from-paths src \
    --ignore-src \
    && rm -rf /var/lib/apt/lists/*
RUN rm -rf src

# install developer dependencies
RUN apt-get update && \
    apt-get install -y \
    bash-completion \
    gdb \
    clang-format \
    clangd \
    bear \
    python3-pip \
    wget \
    sudo && \
    pip3 install --break-system-packages \
    bottle \
    glances

# install moveit2
RUN apt-get update && \
    apt-get install -y \
    ros-jazzy-moveit \ 
    ros-jazzy-rmw-cyclonedds-cpp


# Downgrade rviz_constraints to 0.3.0 to avoid compatibility issues with moveit2 https://github.com/moveit/moveit2/issues/3546
RUN wget http://snapshots.ros.org/jazzy/2025-05-23/ubuntu/pool/main/r/ros-jazzy-rviz-common/ros-jazzy-rviz-common_14.1.11-1noble.20250520.201719_amd64.deb && \
    dpkg -i ros-jazzy-rviz-common_14.1.11-1noble.20250520.201719_amd64.deb && \
    rm ros-jazzy-rviz-common_14.1.11-1noble.20250520.201719_amd64.deb

# Create user matching host system user to avoid permission issues
ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USERNAME=dev

RUN groupadd -g ${GROUP_ID} ${USERNAME} || true && \
    useradd -l -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


# Source ROS setup script in .bashrc
RUN echo "source /opt/ros/jazzy/setup.bash" >> /home/${USERNAME}/.bashrc
# make cyclonedds the default RMW implementation
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /home/${USERNAME}/.bashrc

# Switch to the new user
USER ${USERNAME}
WORKDIR /home/${USERNAME}
