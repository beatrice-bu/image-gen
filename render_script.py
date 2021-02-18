# Run as: blender -b <filename> -P <this_script> -- <image_path>
import bpy
import sys
import os

# Assume the last argument is image path
imagePath = sys.argv[-1]

if not os.path.exists(imagePath):
    # Assume object, material and texture name (and settings) are valid
    # charObj = bpy.data.objects['Camera']
    #   charMat = charObj.material_slots['char01Mat'].material
    #   charTex = charMat.texture_slots['char01Tex'].texture
    #   charTex.image.filepath = imagePath
    print(f'Path to texture: {imagePath}')
    # Render to separate file, identified by texture file
    print(f'image basename {bpy.path.basename(imagePath)}')
    
    imageBaseName = bpy.path.basename(imagePath)
    
    bpy.context.scene.render.filepath = ''
    print(f'directory: {bpy.context.scene.render.filepath + imageBaseName}')
    bpy.context.scene.render.filepath = imageBaseName

    # Render still image, automatically write to output path
    bpy.ops.render.render(write_still=True)
else:
    print("Missing Image:", imagePath)