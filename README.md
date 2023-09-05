# mesh_collision_loss
# Implementation principle:
1. Here, collisions between different meshes are transformed into collisions between a group of point clouds and meshes.
2. Secondly, the distance between points and faces is converted into the distance between the point and the center point of the face.
3. This operation is simple, fast, and experimental results show effectiveness.
