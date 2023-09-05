# mesh_collision_loss
# Implementation principle:
1. Here, collisions between different meshes are transformed into collisions between a group of point clouds and meshes.
2. Secondly, the distance between points and faces is converted into the distance between the point and the center point of the face.
3. This operation is simple, fast, and experimental results show effectiveness.

#Experimental result
![Experimental](https://github.com/huang229/mesh_collision_loss/assets/29627190/f9ab3708-b425-4d12-a484-a43a742f676b)

