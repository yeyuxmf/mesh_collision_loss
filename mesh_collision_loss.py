import logging
import torch
import torch.nn as nn
from pytorch3d.structures import Meshes, Pointclouds
from torch import Tensor
import vtkmodules.all as vtk
import vedo

logger = logging.getLogger(__name__)

LANELET_TAGS_TO_EXCLUDE = ['parking']

def read_stl(file_path):

    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata


def cal_normal(tris):
    p0 = tris[:, 0, :]
    p1 = tris[:, 1, :]
    p2 = tris[:, 2, :]
    v0 = p1 - p0
    v1 = p2 - p1
    normal_ = torch.cross(v0, v1, dim=1)
    normal_ = torch.nn.functional.normalize(normal_, dim=-1)

    return normal_

def cal_sign(points, tris,idxs, normal):

    tris_cenp = torch.mean(tris, dim=1)
    orien = points - tris_cenp[idxs]
    orien = torch.nn.functional.normalize(orien, dim=-1)
    sign_value = torch.sign(torch.sum(torch.mul(normal[idxs], orien), dim=1))

    return sign_value

def cal_faces_distance(points, tris, normal):

    tris_cenp = torch.mean(tris, dim=1)

    points_ = torch.unsqueeze(points, dim=1).expand(-1, tris.shape[0], -1)
    tris_ = torch.unsqueeze(tris_cenp, dim=0).expand(points.shape[0], -1, -1)
    normal_ = torch.unsqueeze(normal, dim=0).expand(points.shape[0], -1, -1)

    orien = points_ - tris_  #n,f,3

    # dist_index_v = torch.min(torch.abs(torch.sum(normal_ * orien, dim=-1)), dim=1)

    dist_index_v = torch.min(torch.sqrt(torch.sum(orien * orien, dim=-1)), dim=1)


    dist_v = dist_index_v[0]
    dist_index = dist_index_v[1]


    return dist_v, dist_index


def point_mesh_face_distance(meshes: Meshes, pcls: Pointclouds) -> Tensor:

    if len(meshes) != len(pcls):
        raise ValueError("meshes and pointclouds must be equal sized batches")
    N = len(meshes)
    # packed representation for pointclouds
    points = pcls.points_packed()  # (P, 3)

    # packed representation for faces
    verts_packed = meshes.verts_packed()
    faces_packed = meshes.faces_packed()
    tris = verts_packed[faces_packed]  # (T, 3, 3)

    normal = cal_normal(tris.detach())
    dist_v, idxs = cal_faces_distance(points, tris, normal)

    sign_value = cal_sign(points.detach(), tris.detach(), idxs.detach(), normal.detach())

    nums = torch.sum(sign_value <= 0)
    if nums>=1:
        point_dist = torch.sum(dist_v * (sign_value<=0))/ torch.sum(sign_value<=0)
    else:
        dist_v = torch.sort(dist_v, descending=False)[0]
        point_dist = torch.sum(dist_v[:10]) / 10 - 0.1

    return point_dist



if __name__ == "__main__":
    mesh_path = "./data/mesh1.stl"
    mesh_path2 = "./data/mesh2.stl"
    # vedo.io.write(mesh1, "./data/mesh2.stl")

    polydata1 = read_stl(mesh_path)
    mesh1_ = vedo.Mesh(polydata1)
    point1 = torch.tensor(mesh1_.points())
    face1 = torch.tensor(mesh1_.cells())

    mesh1 = Meshes(verts=[point1], faces=[face1])

    polydata2 = read_stl(mesh_path2)
    mesh2_ = vedo.Mesh(polydata2)
    point2 = torch.tensor(mesh2_.points())
    face2 = torch.tensor(mesh2_.cells())
    mesh2 = Meshes(verts=[point2], faces=[face2])

    pcls1 = Pointclouds([point1])
    pcls2 = Pointclouds([point2])

    device = torch.device("cuda" if 1 else "cpu")
    deform_verts = torch.full([1, 6], 1.0, device=device, requires_grad=True)
    # The optimizer
    optimizer = torch.optim.Adam([deform_verts], lr=0.1, weight_decay=1e-4)


    mesh1 = mesh1.to(device)
    pcls2 = pcls2.to(device)

    for i in range(200):
        # Initialize optimizer
        optimizer.zero_grad()
        #The purpose here is to move horizontally for easy observation of the effect.
        off = deform_verts[:, :2].expand(point1.shape[0], -1)
        off = torch.cat([off, torch.zeros([off.shape[0], 1]).cuda()], dim=-1)

        new_src_mesh = mesh1.offset_verts(off)


        loss = point_mesh_face_distance(new_src_mesh.to(device), pcls2.to(device))

        loss.backward()
        optimizer.step()

        print("loss %6f" % (loss))
    new_src_mesh = new_src_mesh.detach().cpu()
    mesh1_ = mesh1_.points(new_src_mesh.verts_packed())
    vedo.io.write(mesh1_, "./data/out.stl")

    print("over")




