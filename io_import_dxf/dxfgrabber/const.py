# SPDX-FileCopyrightText: 2012 Manfred Moitzi (mozman)
#
# SPDX-License-Identifier: MIT

# Purpose: constant values
# Created: 21.07.2012, taken from my ezdxf project

from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

ENV_CYTHON = 'DXFGRABBER_CYTHON'

BYBLOCK = 0
BYLAYER = 256

XTYPE_NONE = 0
XTYPE_2D = 1
XTYPE_3D = 2
XTYPE_2D_3D = 3

acadrelease = {
    'AC1009': 'R12',
    'AC1012': 'R13',
    'AC1014': 'R14',
    'AC1015': 'R2000',
    'AC1018': 'R2004',
    'AC1021': 'R2007',
    'AC1024': 'R2010',
}

dxfversion = {
    acad: dxf for dxf, acad in acadrelease.items()
}

# Entity: Polyline, Polymesh
# 70 flags
POLYLINE_CLOSED = 1
POLYLINE_MESH_CLOSED_M_DIRECTION = POLYLINE_CLOSED
POLYLINE_CURVE_FIT_VERTICES_ADDED = 2
POLYLINE_SPLINE_FIT_VERTICES_ADDED = 4
POLYLINE_3D_POLYLINE = 8
POLYLINE_3D_POLYMESH = 16
POLYLINE_MESH_CLOSED_N_DIRECTION = 32
POLYLINE_POLYFACE = 64
POLYLINE_GENERATE_LINETYPE_PATTERN =128

# Entity: Polymesh
# 75 surface smooth type
POLYMESH_NO_SMOOTH = 0
POLYMESH_QUADRIC_BSPLINE = 5
POLYMESH_CUBIC_BSPLINE = 6
POLYMESH_BEZIER_SURFACE = 8

#Entity: Vertex
# 70 flags
VERTEXNAMES = ('vtx0', 'vtx1', 'vtx2', 'vtx3')
VTX_EXTRA_VERTEX_CREATED = 1 ## Extra vertex created by curve-fitting
VTX_CURVE_FIT_TANGENT = 2    ## Curve-fit tangent defined for this vertex.
## A curve-fit tangent direction of 0 may be omitted from the DXF output, but is
## significant if this bit is set.
## 4 = unused, never set in dxf files
VTX_SPLINE_VERTEX_CREATED = 8 ##Spline vertex created by spline-fitting
VTX_SPLINE_FRAME_CONTROL_POINT = 16
VTX_3D_POLYLINE_VERTEX = 32
VTX_3D_POLYGON_MESH_VERTEX = 64
VTX_3D_POLYFACE_MESH_VERTEX = 128

VERTEX_FLAGS = {
    'polyline2d': 0,
    'polyline3d': VTX_3D_POLYLINE_VERTEX,
    'polymesh': VTX_3D_POLYGON_MESH_VERTEX,
    'polyface': VTX_3D_POLYGON_MESH_VERTEX | VTX_3D_POLYFACE_MESH_VERTEX,
}
POLYLINE_FLAGS = {
    'polyline2d': 0,
    'polyline3d': POLYLINE_3D_POLYLINE,
    'polymesh': POLYLINE_3D_POLYMESH,
    'polyface': POLYLINE_POLYFACE,
}

#---block-type flags (bit coded values, may be combined):
# Entity: BLOCK
# 70 flags
BLK_ANONYMOUS = 1                # This is an anonymous block generated by hatching, associative dimensioning, other internal operations, or an application
BLK_NON_CONSTANT_ATTRIBUTES = 2  # This block has non-constant attribute definitions (this bit is not set if the block has any attribute definitions that are constant, or has no attribute definitions at all)
BLK_XREF = 4                     # This block is an external reference (xref)
BLK_XREF_OVERLAY = 8             # This block is an xref overlay
BLK_EXTERNAL = 16                # This block is externally dependent
BLK_RESOLVED = 32                # This is a resolved external reference, or dependent of an external reference (ignored on input)
BLK_REFERENCED = 64              # This definition is a referenced external reference (ignored on input)

LWPOLYLINE_CLOSED = 1
LWPOLYLINE_PLINEGEN = 128

SPLINE_CLOSED = 1
SPLINE_PERIODIC = 2
SPLINE_RATIONAL = 4
SPLINE_PLANAR = 8
SPLINE_LINEAR = 16  # planar bit is also set

MTEXT_TOP_LEFT = 1
MTEXT_TOP_CENTER = 2
MTEXT_TOP_RIGHT = 3
MTEXT_MIDDLE_LEFT = 4
MTEXT_MIDDLE_CENTER = 5
MTEXT_MIDDLE_RIGHT = 6
MTEXT_BOTTOM_LEFT = 7
MTEXT_BOTTOM_CENTER = 8
MTEXT_BOTTOM_RIGHT = 9

MTEXT_LEFT_TO_RIGHT = 1
MTEXT_TOP_TO_BOTTOM = 2
MTEXT_BY_STYLE = 5
