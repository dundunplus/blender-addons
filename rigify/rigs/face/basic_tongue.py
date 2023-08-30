# SPDX-FileCopyrightText: 2021-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

from itertools import count

from ...utils.naming import make_derived_name
from ...utils.bones import flip_bone, copy_bone_position
from ...utils.layers import ControlLayersOption
from ...utils.misc import map_list

from ...base_rig import stage

from ..chain_rigs import TweakChainRig
from ..widgets import create_jaw_widget


class Rig(TweakChainRig):
    """Basic tongue from the original PitchiPoy face rig."""  # noqa

    min_chain_length = 3

    def initialize(self):
        super().initialize()

        self.bbone_segments = self.params.bbones

    ####################################################
    # BONES

    class CtrlBones(TweakChainRig.CtrlBones):
        master: str                    # Master control.

    class MchBones(TweakChainRig.MchBones):
        follow: list[str]              # Partial follow master bones.

    bones: TweakChainRig.ToplevelBones[
        list[str],
        'Rig.CtrlBones',
        'Rig.MchBones',
        list[str]
    ]

    ####################################################
    # Control chain

    @stage.generate_bones
    def make_control_chain(self):
        org = self.bones.org[0]
        name = self.copy_bone(org, make_derived_name(org, 'ctrl'), parent=True)
        flip_bone(self.obj, name)
        self.bones.ctrl.master = name

    @stage.parent_bones
    def parent_control_chain(self):
        pass

    @stage.configure_bones
    def configure_control_chain(self):
        master = self.bones.ctrl.master

        self.copy_bone_properties(self.bones.org[0], master)

        ControlLayersOption.SKIN_PRIMARY.assign(self.params, self.obj, [master])

    @stage.generate_widgets
    def make_control_widgets(self):
        create_jaw_widget(self.obj, self.bones.ctrl.master)

    ####################################################
    # Mechanism chain

    @stage.generate_bones
    def make_follow_chain(self):
        self.bones.mch.follow = map_list(self.make_mch_follow_bone, count(1), self.bones.org[1:])

    def make_mch_follow_bone(self, _i: int, org: str):
        name = self.copy_bone(org, make_derived_name(org, 'mch'))
        copy_bone_position(self.obj, self.base_bone, name)
        flip_bone(self.obj, name)
        return name

    @stage.parent_bones
    def parent_follow_chain(self):
        for mch in self.bones.mch.follow:
            self.set_bone_parent(mch, self.rig_parent_bone)

    @stage.rig_bones
    def rig_follow_chain(self):
        master = self.bones.ctrl.master
        num_orgs = len(self.bones.org)

        for i, mch in enumerate(self.bones.mch.follow):
            self.make_constraint(mch, 'COPY_TRANSFORMS', master, influence=1-(1+i)/num_orgs)

    ####################################################
    # Tweak chain

    @stage.parent_bones
    def parent_tweak_chain(self):
        ctrl = self.bones.ctrl
        parents = [ctrl.master, *self.bones.mch.follow, self.rig_parent_bone]
        for tweak, main in zip(ctrl.tweak, parents):
            self.set_bone_parent(tweak, main)

    ####################################################
    # SETTINGS

    @classmethod
    def add_parameters(cls, params):
        params.bbones = bpy.props.IntProperty(
            name='B-Bone Segments',
            default=10,
            min=1,
            description='Number of B-Bone segments'
        )

        ControlLayersOption.SKIN_PRIMARY.add_parameters(params)

    @classmethod
    def parameters_ui(cls, layout, params):
        layout.prop(params, 'bbones')

        ControlLayersOption.SKIN_PRIMARY.parameters_ui(layout, params)


def create_sample(obj):
    # generated by rigify.utils.write_metarig
    bpy.ops.object.mode_set(mode='EDIT')
    arm = obj.data

    bones = {}

    bone = arm.edit_bones.new('tongue')
    bone.head = 0.0000, 0.0000, 0.0000
    bone.tail = 0.0000, 0.0161, 0.0074
    bone.roll = 0.0000
    bone.use_connect = False
    bones['tongue'] = bone.name
    bone = arm.edit_bones.new('tongue.001')
    bone.head = 0.0000, 0.0161, 0.0074
    bone.tail = 0.0000, 0.0375, 0.0091
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tongue']]
    bones['tongue.001'] = bone.name
    bone = arm.edit_bones.new('tongue.002')
    bone.head = 0.0000, 0.0375, 0.0091
    bone.tail = 0.0000, 0.0605, -0.0029
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tongue.001']]
    bones['tongue.002'] = bone.name

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['tongue']]
    pbone.rigify_type = 'face.basic_tongue'
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    for b in bones:
        bone = arm.edit_bones[bones[b]]
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        bone.bbone_x = bone.bbone_z = bone.length * 0.05
        arm.edit_bones.active = bone
        if bcoll := arm.collections.active:
            bcoll.assign(bone)

    return bones
