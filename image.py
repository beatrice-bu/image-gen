# Run as: blender -b <filename> -P <this_script> -- <image_path>
import bpy, sys, os

# Assume the last argument is image path
imagePath = sys.argv[-1]

if os.path.exists(imagePath):
    # Assume object, material and texture name (and settings) are valid
    charObj = bpy.data.objects['Char01']
    charMat = charObj.material_slots['Char01Mat'].material
    charTex = charMat.texture_slots['Char01Tex'].texture
    charTex.image.filepath = imagePath

    # Render to separate file, identified by texture file
    imageBaseName = bpy.path.basename(imagePath)
    bpy.context.scene.render.filepath += '-' + imageBaseName

    # Render still image, automatically write to output path
    bpy.ops.render.render(write_still=True)
else:
    print("Missing Image:", imagePath)