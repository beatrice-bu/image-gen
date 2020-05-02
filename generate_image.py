import bpy
import os
import glob
import random
import math
import mathutils
import uuid

def random_point(center, inner_radius, outer_radius):
    u = random.uniform(0, 1)
    v = random.uniform(0, 1)
    theta = u * 2.0 * math.pi
    phi = math.acos(2.0 * v - 1.0)
    r = random.uniform(inner_radius, outer_radius)
    sinTheta = math.sin(theta)
    cosTheta = math.cos(theta)
    sinPhi = math.sin(phi)
    cosPhi = math.cos(phi)
    x = r * sinPhi * cosTheta
    y = r * sinPhi * sinTheta
    z = r * cosPhi
    return  mathutils.Vector((x, y, z)) + center

def look_at(obj_camera, point):
    print(point)
    loc_camera = obj_camera.location

    print(loc_camera)
    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()


def create_lights():
    lights = []
    center = mathutils.Vector((0, 0, 0))
    for x in range(0, random.randint(1,4)):
        bpy.ops.object.light_add(type='POINT', radius=1.0, location=random_point(center, 3, 15))
        light = bpy.context.selected_objects[0]
        light.data.energy = random.uniform(250.0,2000.0)
        lights.append(bpy.context.selected_objects[0])
    return lights

# The direcetory that contains the models we want to include to label in our data.
model_directory = "models"

models = glob.glob(os.path.join(model_directory, "*.dae"))

# labels =[]
# for model in models:
#     labels.append(os.path.splitext(os.path.basename(model))[0])

# print(labels)

# while( True):
#     test = 5

output_directory = "/Users/dougmatthews/Repos/image-gen/renders"

# The directory that contains backgrounds to use in our data.
background_directory = ""

# Total number of images generated
num_images = 5000

images_per_model = int(num_images / len(models))

print (images_per_model)

count = 0
for model_path in models:
    name = os.path.splitext(os.path.basename(model_path))[0]
    bpy.ops.wm.collada_import(filepath=model_path)

    try: 
        os.mkdir(os.path.join(output_directory, name))
    except:
        print("Directory already exists.")

    # make sure to get all imported objects
    if len(bpy.context.selected_objects) > 1:
        raise Exception("Error", "Image generation expects imported model to only have one object.")

    imported_model = bpy.context.selected_objects[0]
    imported_model.scale = (0.1, 0.1, 0.1)
    print(imported_model)

    mesh = imported_model.data
    for f in mesh.polygons:
        f.use_smooth = True

    lights = []

    # Render images
    for image in range(0, images_per_model):
        
        
        imported_model.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)
        camera = bpy.context.scene.camera
        center = mathutils.Vector((0, 0, 0))

        camera.location = random_point(center, 6, 9)

        point = random_point(center, 0, 1)
        look_at(camera, point)

        if random.uniform(0.0,1.0) < 0.9:
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        else:
            bpy.context.scene.render.engine = 'CYCLES'

        bpy.context.scene.render.image_settings.color_mode ='RGBA'
        bpy.context.scene.render.image_settings.file_format='PNG' 
        bpy.context.scene.render.image_settings.compression = 90

        # Create lights
        bpy.ops.object.select_all(action='DESELECT')
        for light in lights: 
            light.select_set(True)
        bpy.ops.object.delete()
        lights = create_lights()

        
        bpy.context.scene.render.filepath = os.path.join(output_directory, name, f'{str(uuid.uuid1().hex)}.png')
        bpy.ops.render.render(write_still=True)
        print(f"\033[92m{count/num_images}")
        print(f"\033[0m")
        count+=1


        
    # Delete lights and model
    bpy.ops.object.select_all(action='DESELECT')
    for light in lights: 
        light.select_set(True)
    imported_model.select_set(True)
    bpy.ops.object.delete()

