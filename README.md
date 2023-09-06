# mesh_collision_loss

1. This is only a simple application, not an accurate calculation. You can make modifications according to your own needs.

# Implementation principle:
1. Here, collisions between different meshes are transformed into collisions between a group of point clouds and meshes.
2. Secondly, the distance between points and faces is converted into the distance between the point and the center point of the face.
3. This operation is simple, fast, and experimental results show effectiveness.

# Visualization Tool Installation Package
链接：https://pan.baidu.com/s/1SMPms9_GoujxcmbTCV0K3Q 
提取码：fiid  
This is a 3D visualization tool that supports visualization of stl files and point cloud txt file formats.

# Experimental result
![Experimental](https://github.com/huang229/mesh_collision_loss/assets/29627190/f9ab3708-b425-4d12-a484-a43a742f676b)
![loss](https://github.com/huang229/mesh_collision_loss/assets/29627190/e2f4aca9-b1fa-42b8-8d51-0f1ca0224dcc)


# Reference
1. https://docs.torchdrivesim.org/en/latest/_modules/torchdrivesim/infractions.html
2. https://github.com/facebookresearch/pytorch3d

   
# Environment
1.python 3.7.0

2.pytorch 11.3.1

3.pytorch3D 0.7.4

4.vedo 2023.4.4


# Train
  python ./mesh_collision_loss.py

# License and Citation
1.Without permission, the design concept of this model shall not be used for commercial purposes, profit seeking, etc.

2.If you refer to the design concept of this model for theoretical research, please also add a reference.

