#!/usr/bin/env python

#
# Copyright 2019 Autodesk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
    Helper functions regarding USD that will be used throughout the test.
"""

import mayaUsd.ufe
import mayaUsd.lib
import mayaUsd_createStageWithNewLayer

import ufe
import ufeUtils

from pxr import Usd, UsdGeom, Gf

usdSeparator = '/'


def createUfePathSegment(usdPath):
    """
        Create an UFE path from a given usd path.
        Args:
            usdPath (str): The usd path to use
        Returns :
            PathSegment of the given usdPath
    """
    return ufe.PathSegment(usdPath, mayaUsd.ufe.getUsdRunTimeId(), usdSeparator)

def getPrimFromSceneItem(item):
    if ufeUtils.ufeFeatureSetVersion() >= 2:
        rawItem = item.getRawAddress()
        prim = mayaUsd.ufe.getPrimFromRawItem(rawItem)
        return prim
    else:
        return Usd.Prim()

def createAnimatedHierarchy(stage):
    """
    Create simple hierarchy in the stage:
    /ParentA
        /Sphere
        /Cube
    /ParenB
    
    Entire ParentA hierarchy will receive time samples on translate for time 1 and 100
    """
    parentA = "/ParentA"
    parentB = "/ParentB"
    childSphere = "/ParentA/Sphere"
    childCube = "/ParentA/Cube"
    
    parentPrimA = stage.DefinePrim(parentA, 'Xform')
    parentPrimB = stage.DefinePrim(parentB, 'Xform')
    childPrimSphere = stage.DefinePrim(childSphere, 'Sphere')
    childPrimCube = stage.DefinePrim(childCube, 'Cube')
    
    UsdGeom.XformCommonAPI(parentPrimA).SetRotate((0,0,0))
    UsdGeom.XformCommonAPI(parentPrimB).SetTranslate((1,10,0))
    
    time1 = Usd.TimeCode(1.)
    UsdGeom.XformCommonAPI(parentPrimA).SetTranslate((0,0,0),time1)
    UsdGeom.XformCommonAPI(childPrimSphere).SetTranslate((5,0,0),time1)
    UsdGeom.XformCommonAPI(childPrimCube).SetTranslate((0,0,5),time1)
    
    time2 = Usd.TimeCode(100.)
    UsdGeom.XformCommonAPI(parentPrimA).SetTranslate((0,5,0),time2)
    UsdGeom.XformCommonAPI(childPrimSphere).SetTranslate((-5,0,0),time2)
    UsdGeom.XformCommonAPI(childPrimCube).SetTranslate((0,0,-5),time2)

def createSimpleXformScene():
    '''Create a simple scene with a trivial hierarchy:

    A    translation (1, 2, 3)
    |_B  translation (7, 8, 9)

    '''

    psPathStr = mayaUsd_createStageWithNewLayer.createStageWithNewLayer()
    psPath = ufe.PathString.path(psPathStr)
    ps = ufe.Hierarchy.createItem(psPath)
    stage = mayaUsd.lib.GetPrim(psPathStr).GetStage()
    aPrim = stage.DefinePrim('/A', 'Xform')
    aXformable = UsdGeom.Xformable(aPrim)
    aXlateOp = aXformable.AddTranslateOp()
    aXlation = Gf.Vec3d(1, 2, 3)
    aXlateOp.Set(aXlation)
    aUsdUfePathStr = psPathStr + ',/A'
    aUsdUfePath = ufe.PathString.path(aUsdUfePathStr)
    aUsdItem = ufe.Hierarchy.createItem(aUsdUfePath)

    bPrim = stage.DefinePrim('/A/B', 'Xform')
    bXformable = UsdGeom.Xformable(bPrim)
    bXlateOp = bXformable.AddTranslateOp()
    bXlation = Gf.Vec3d(7, 8, 9)
    bXlateOp.Set(bXlation)
    bUsdUfePathStr = aUsdUfePathStr + '/B'
    bUsdUfePath = ufe.PathString.path(bUsdUfePathStr)
    bUsdItem = ufe.Hierarchy.createItem(bUsdUfePath)

    return (ps, aXlateOp, aXlation, aUsdUfePathStr, aUsdUfePath, aUsdItem,
            bXlateOp, bXlation, bUsdUfePathStr, bUsdUfePath, bUsdItem)
