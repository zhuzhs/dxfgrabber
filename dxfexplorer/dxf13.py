#!/usr/bin/env python
#coding:utf-8
# Purpose: DXF13 tag wrapper
# Created: 21.07.2012, taken from my ezdxf project
# Copyright (C) 2012, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"


from . import dxf12
from .genericwrapper import GenericWrapper
from .dxfattr import DXFAttr, DXFAttributes, DefSubclass
from . import const


none_subclass = DefSubclass(None, {
        'handle': DXFAttr(5, None),
        'block_record': DXFAttr(330, None), # Soft-pointer ID/handle to owner BLOCK_RECORD object
    })

entity_subclass = DefSubclass('AcDbEntity', {
    'paperspace': DXFAttr(67, None), # 0 .. modelspace, 1 .. paperspace, default is 0
    'layer': DXFAttr(8, None), # layername as string, default is '0'
    'linetype': DXFAttr(6, None), # linetype as string, special names BYLAYER/BYBLOCK, default is BYLAYER
    'ltscale': DXFAttr(48, None), # linetype scale, default is 1.0
    'invisible': DXFAttr(60, None), # invisible .. 1, visible .. 0, default is 0
    'color': DXFAttr(62, None),# dxf color index, 0 .. BYBLOCK, 256 .. BYLAYER, default is 256
    })

line_subclass = DefSubclass('AcDbLine', {
        'start': DXFAttr(10, 'Point2D/3D'),
        'end': DXFAttr(11, 'Point2D/3D'),
        'thickness': DXFAttr(39, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })

class Line(dxf12.Line):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, line_subclass)

point_subclass = DefSubclass('AcDbPoint', {
        'point': DXFAttr(10, 'Point2D/3D'),
        'thickness': DXFAttr(39, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })


class Point(dxf12.Point):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, point_subclass)


circle_subclass = DefSubclass('AcDbCircle', {
        'center': DXFAttr(10, 'Point2D/3D'),
        'radius': DXFAttr(40, None),
        'thickness': DXFAttr(39, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })

class Circle(dxf12.Circle):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, circle_subclass)


arc_subclass = (
    DefSubclass('AcDbCircle', {
        'center': DXFAttr(10, 'Point2D/3D'),
        'radius': DXFAttr(40, None),
        'thickness': DXFAttr(39, None),
        }),
    DefSubclass('AcDbArc', {
        'startangle': DXFAttr(50, None),
        'endangle': DXFAttr(51, None),
        'extrusion': DXFAttr(210, 'Point3D'),
        }),
    )

class Arc(dxf12.Arc):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, *arc_subclass)


trace_subclass = DefSubclass('AcDbTrace', {
        'vtx0' : DXFAttr(10,'Point2D/3D'),
        'vtx1' : DXFAttr(11, 'Point2D/3D'),
        'vtx2' : DXFAttr(12, 'Point2D/3D'),
        'vtx3' : DXFAttr(13, 'Point2D/3D'),
        'thickness': DXFAttr(39, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })

class Trace(dxf12.Trace):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, trace_subclass)


Solid = Trace


face_subclass = DefSubclass('AcDbFace', {
        'vtx0' : DXFAttr(10,'Point2D/3D'),
        'vtx1' : DXFAttr(11, 'Point2D/3D'),
        'vtx2' : DXFAttr(12, 'Point2D/3D'),
        'vtx3' : DXFAttr(13, 'Point2D/3D'),
        'invisible_edge': DXFAttr(70, None),
    })

class Face(dxf12.Face):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, face_subclass)


text_subclass =  (
    DefSubclass('AcDbText', {
        'insert': DXFAttr(10, 'Point2D/3D'),
        'height': DXFAttr(40, None),
        'text': DXFAttr(1, None),
        'rotation': DXFAttr(50, None), # in degrees (circle = 360deg)
        'oblique': DXFAttr(51, None), # in degrees, vertical = 0deg
        'style': DXFAttr(7, None), # text style
        'width': DXFAttr(41, None), # width FACTOR!
        'textgenerationflag': DXFAttr(71, None), # 2 = backward (mirr-x), 4 = upside down (mirr-y)
        'halign': DXFAttr(72, None), # horizontal justification
        'alignpoint': DXFAttr(11, 'Point2D/3D'),
        'thickness': DXFAttr(39, None),
        'extrusion': DXFAttr(210, 'Point3D'),
        }),
    DefSubclass('AcDbText', { 'valign': DXFAttr(73, None) }))

class Text(dxf12.Text):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, *text_subclass)

polyline_subclass = DefSubclass('AcDb2dPolyline', {
        'elevation': DXFAttr(10, 'Point3D'),
        'flags': DXFAttr(70, None),
        'defaultstartwidth': DXFAttr(40, None),
        'defaultendwidth': DXFAttr(41, None),
        'mcount': DXFAttr(71, None),
        'ncount': DXFAttr(72, None),
        'msmoothdensity': DXFAttr(73, None),
        'nsmoothdensity': DXFAttr(74, None),
        'smoothtype': DXFAttr(75, None),
        'thickness': DXFAttr(39, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })

class Polyline(dxf12.Polyline):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, polyline_subclass)


vertex_subclass = (
    DefSubclass('AcDbVertex', {}), # subclasses[2]
    DefSubclass('AcDb2dVertex', { # subclasses[3]
        'location': DXFAttr(10, 'Point2D/3D'),
        'startwidth': DXFAttr(40, None),
        'endwidth': DXFAttr(41, None),
        'bulge': DXFAttr(42, None),
        'flags': DXFAttr(70, None),
        'tangent': DXFAttr(50, None),
        'vtx0': DXFAttr(71, None),
        'vtx1': DXFAttr(72, None),
        'vtx2': DXFAttr(73, None),
        'vtx3': DXFAttr(74, None),
        })
    )

class Vertex(dxf12.Vertex):
    VTX3D = const.VTX_3D_POLYFACE_MESH_VERTEX | const.VTX_3D_POLYGON_MESH_VERTEX | const.VTX_3D_POLYLINE_VERTEX
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, *vertex_subclass)


class SeqEnd(dxf12.SeqEnd):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass)
    
lwpolyline_subclass = DefSubclass('AcDbPolyline', {
        'elevation': DXFAttr(38, None),
        'flags': DXFAttr(70, None),
        'constwidth': DXFAttr(43, None),
        'count': DXFAttr(90, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })

LWPOINTCODES = (10, 20, 40, 41, 42)
class LWPolyline(GenericWrapper):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, lwpolyline_subclass)
    def __iter__(self):
        subclass = self.tags.subclasses[2] # subclass AcDbPolyline
        point = []
        for tag in subclass:
            if tag.code in LWPOINTCODES:
                if tag.code == 10:
                    if point:
                        yield tuple(point)
                        point = []
                point.append(tag.value)
        if point:
            yield tuple(point)

    def is_closed(self):
        return bool(self.dxf.flags & const.LWPOLYLINE_CLOSED)

    @property
    def points(self):
        for point in self:
            yield (point[0].value, point[1].value)


insert_subclass = DefSubclass('AcDbBlockReference', {
        'attribsfollow': DXFAttr(66, None),
        'name': DXFAttr(2, None),
        'insert': DXFAttr(10, 'Point2D/3D'),
        'xscale': DXFAttr(41, None),
        'yscale': DXFAttr(42, None),
        'zscale': DXFAttr(43, None),
        'rotation': DXFAttr(50, None),
        'colcount': DXFAttr(70, None),
        'rowcount': DXFAttr(71, None),
        'colspacing': DXFAttr(44, None),
        'rowspacing': DXFAttr(45, None),
        'extrusion': DXFAttr(210, 'Point3D'),
    })

class Insert(dxf12.Insert):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, insert_subclass)


attrib_subclass = (
    DefSubclass('AcDbText', {
        'insert': DXFAttr(10, 'Point2D/3D'),
        'thickness': DXFAttr(39, None),
        'height': DXFAttr(40, None),
        'text': DXFAttr(1, None),
        'style': DXFAttr(7, None), # DXF-specs: 'AcDbAttribute'; AutoCAD: 'AcDbText'
        }),
    DefSubclass('AcDbAttribute', {
        'tag': DXFAttr(2, None),
        'flags': DXFAttr(70, None),
        'fieldlength': DXFAttr(73, None),
        'rotation': DXFAttr(50, None),
        'width': DXFAttr(41, None),
        'oblique': DXFAttr(51, None),
        'textgenerationflag': DXFAttr(71, None),
        'halign': DXFAttr(72, None),
        'valign': DXFAttr(74, None),
        'alignpoint': DXFAttr(11, 'Point2D/3D'),
        'extrusion': DXFAttr(210, 'Point3D'),
        })
    )

class Attrib(dxf12.Attrib):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, *attrib_subclass)


ellipse_subclass = DefSubclass('AcDbEllipse', {
        'center': DXFAttr(10, 'Point2D/3D'),
        'majoraxis': DXFAttr(11, 'Point2D/3D'), # relative to the center
        'extrusion': DXFAttr(210, 'Point3D'),
        'ratio': DXFAttr(40, None),
        'startparam': DXFAttr(41, None), # this value is 0.0 for a full ellipse
        'endparam': DXFAttr(42, None), # this value is 2*pi for a full ellipse
    })

class Ellipse(GenericWrapper):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, ellipse_subclass)


ray_subclass = DefSubclass('AcDbRay', {
    'start': DXFAttr(10, 'Point3D'),
    'unitvector': DXFAttr(11, 'Point3D'),
    })

class Ray(GenericWrapper):
    DXFATTRIBS = DXFAttributes(none_subclass, entity_subclass, ray_subclass)