# mesh_collision_loss

1. This is just a streamlined implementation, you can make appropriate adjustments according to the specific situation.

# Implementation principle:
1. Here, collisions between different meshes are transformed into collisions between a group of point clouds and meshes.
2. Secondly, the distance between points and faces is converted into the distance between the point and the center point of the face.
3. This operation is simple, fast, and experimental results show effectiveness.

# Experimental result
![Experimental](https://github.com/huang229/mesh_collision_loss/assets/29627190/f9ab3708-b425-4d12-a484-a43a742f676b)
![loss](https://github.com/huang229/mesh_collision_loss/assets/29627190/4cd46eaf-7e46-4c96-bab0-9c89e7d9662b)


# Reference
1. https://docs.torchdrivesim.org/en/latest/_modules/torchdrivesim/infractions.html
2. https://github.com/facebookresearch/pytorch3d

   
# Environment
1.python 3.7.0

2.pytorch 11.3.1

3.pytorch3D 0.7.4


# Train
  python ./mesh_collision_loss.py

# License and Citation
1.Without permission, the design concept of this model shall not be used for commercial purposes, profit seeking, etc.

2.If you refer to the design concept of this model for theoretical research and publication of papers on automatic tooth arrangement, please also add a reference.

