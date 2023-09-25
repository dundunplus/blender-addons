# SPDX-FileCopyrightText: 2018-2022 The glTF-Blender-IO authors
#
# SPDX-License-Identifier: Apache-2.0

import bpy
from .....io.com.gltf2_io_extensions import Extension
from ....exp import gltf2_blender_get
from ...material import gltf2_blender_gather_texture_info


def export_sheen(blender_material, export_settings):
    sheen_extension = {}

    sheenColor_socket = gltf2_blender_get.get_socket(blender_material, "sheenColor")
    sheenRoughness_socket = gltf2_blender_get.get_socket(blender_material, "sheenRoughness")

    if sheenColor_socket is None or sheenRoughness_socket is None:
        return None, {}

    uvmap_infos = {}

    sheenColor_non_linked = isinstance(sheenColor_socket, bpy.types.NodeSocket) and not sheenColor_socket.is_linked
    sheenRoughness_non_linked = isinstance(sheenRoughness_socket, bpy.types.NodeSocket) and not sheenRoughness_socket.is_linked

    if sheenColor_non_linked is True:
        color = sheenColor_socket.default_value[:3]
        if color != (0.0, 0.0, 0.0):
            sheen_extension['sheenColorFactor'] = color
    else:
        # Factor
        fac = gltf2_blender_get.get_factor_from_socket(sheenColor_socket, kind='RGB')
        if fac is None:
            fac = [1.0, 1.0, 1.0] # Default is 0.0/0.0/0.0, so we need to set it to 1 if no factor
        if fac is not None and fac != [0.0, 0.0, 0.0]:
            sheen_extension['sheenColorFactor'] = fac

        # Texture
        if gltf2_blender_get.has_image_node_from_socket(sheenColor_socket):
            original_sheenColor_texture, uvmap_info, _ = gltf2_blender_gather_texture_info.gather_texture_info(
                sheenColor_socket,
                (sheenColor_socket,),
                (),
                export_settings,
            )
            sheen_extension['sheenColorTexture'] = original_sheenColor_texture
            uvmap_infos.update({'sheenColorTexture': uvmap_info})

    if sheenRoughness_non_linked is True:
        fac = sheenRoughness_socket.default_value
        if fac != 0.0:
            sheen_extension['sheenRoughnessFactor'] = fac
    else:
        # Factor
        fac = gltf2_blender_get.get_factor_from_socket(sheenRoughness_socket, kind='VALUE')
        if fac is None:
            fac = 1.0 # Default is 0.0 so we need to set it to 1.0 if no factor
        if fac is not None and fac != 0.0:
            sheen_extension['sheenRoughnessFactor'] = fac

        # Texture
        if gltf2_blender_get.has_image_node_from_socket(sheenRoughness_socket):
            original_sheenRoughness_texture, uvmap_info , _ = gltf2_blender_gather_texture_info.gather_texture_info(
                sheenRoughness_socket,
                (sheenRoughness_socket,),
                (),
                export_settings,
            )
            sheen_extension['sheenRoughnessTexture'] = original_sheenRoughness_texture
            uvmap_infos.update({'sheenRoughnessTexture': uvmap_info})

    return Extension('KHR_materials_sheen', sheen_extension, False), uvmap_infos
