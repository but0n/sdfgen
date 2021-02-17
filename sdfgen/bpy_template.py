import bpy
from mathutils import Vector


# resolution = 8
#include


def applyMatrix(obj):
    obj.select_set(True)
    bpy.ops.object.transform_apply()

def getAABB(obj):
    # Apply world matrix
    applyMatrix(obj)

    *xyz, = zip(*[v[:] for v in obj.bound_box])
    aabb_min = [min(v) for v in xyz]
    aabb_max = [max(v) for v in xyz]
    return aabb_min, aabb_max

def sliceObj(obj, z, l):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    print(f' [*] Execute bisect: {z} ~ {z + l}, \tlength: {l}')
    # top
    bpy.ops.mesh.bisect(
        plane_co=(0, 0, z + l),
        plane_no=(0, 0, 1),
        use_fill=True,
        clear_inner=False,
        clear_outer=True,
    )
    bpy.ops.mesh.select_all(action='SELECT')
    # bottom
    bpy.ops.mesh.bisect(
        plane_co=(0, 0, z),
        plane_no=(0, 0, 1),
        use_fill=True,
        clear_inner=True,
        clear_outer=False,
    )
    bpy.ops.object.editmode_toggle()


def camera_fit(target):
    applyMatrix(target)
    ctx = bpy.context
    cam = ctx.scene.camera
    pos, scale = cam.camera_fit_coords(ctx.evaluated_depsgraph_get(), [v for tp in target.bound_box for v in tp])
    cam.matrix_world.translation = pos
    cam.data.ortho_scale = scale



if __name__ == '__main__':
    print(f'Import scene: {scene}')
    bpy.ops.import_scene.gltf(filepath=scene, loglevel=50, import_pack_images=False)

    print('Merge meshes')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()
    bpy.ops.object.select_all(action='DESELECT')



    print(f'Only {len(bpy.data.objects)} objects left')

    target = bpy.data.objects[1]

    # setup material
    target.data.materials.clear()
    target.data.materials.append(bpy.data.materials['pos'])

    aabb = getAABB(target)

    # fix matrix
    *aabb, = zip(*aabb)
    scale = max([2/(y - x) for x, y in aabb])
    print(f'Inverse Scale: {scale}')
    center = [-(x + (y - x) / 2) for x, y in aabb] # FIXME::
    # origin
    target.matrix_world.translation = Vector(center)
    applyMatrix(target)
    # scale (clamp v position  [-1, 1])
    target.scale = Vector([scale] * 3)



    fix_offset = getAABB(target)[0]
    target.matrix_world.translation -= Vector(fix_offset)

    camera_fit(target)

    finalAABB = getAABB(target)

    print('AABB: ')
    print(*[f'\t{v3}\n' for v3 in finalAABB])

    zrange = dict(zip('xyz', zip(*finalAABB)))['z']
    print(f'Z range: {zrange}')

    bottom, top = zrange
    stride = (top - bottom) / resolution

    collection = bpy.context.collection.objects
    bpy.context.scene.collection.objects.unlink(target)

    # Render
    render = bpy.context.scene.render
    render.resolution_x = render.resolution_y = 2048


    for i in range(resolution):
        bpy.context.scene.collection.objects.link(target)
        target.select_set(True)
        # t = target.copy()
        bpy.ops.object.duplicate_move()
        bpy.context.scene.collection.objects.unlink(target)
        t = bpy.data.objects[-1]
        # collection.link(t)
        sliceObj(t, bottom + stride * i, stride)

        render.filepath = f'output_{i}'
        bpy.ops.render.render(write_still=True)

        bpy.context.scene.collection.objects.unlink(t)
