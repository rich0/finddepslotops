#!/usr/bin/python
# encoding: utf-8
'''
finddepslotops -- Find all package dependencies that support slot operators

@author:     Richard Freeman
        
@copyright:  2013 Richard Freeman. All rights reserved.
        
@license:    GPL-3+

@contact:    rich0@gentoo.org
@deffield    updated: Updated


'''

import sys
import portage
from portage.xml.metadata import MetaDataXML


def findpackagedepslotops(porttree, cpv):
    depstr = porttree.dbapi.aux_get(cpv, ["RDEPEND"])[0]
    cleandeps = portage.dep.paren_reduce(depstr)
    for indep in portage.dep.flatten(cleandeps):
        if (portage.dep.isvalidatom(indep)): 
            indepslot = portage.dep.dep_getslot(indep)
            if indepslot == None or not indepslot.endswith("="):
                allavail = porttree.dep_match(indep)
                for inallavail in portage.dep.flatten(allavail):
                    slot = porttree.dbapi.aux_get(inallavail, ["SLOT"])[0]
                    if slot.find("/") > 0:
                        category, pkgname, version, rev = portage.catpkgsplit(cpv)
                        ebuild, path = porttree.dbapi.findname2(cpv)
                        metxml = path+"/"+category+"/"+pkgname+"/metadata.xml"
                        maints=[]
                        try:
                            pkg_md = MetaDataXML(metxml,"/usr/portage/metadata/herds.xml")
                            for maint in pkg_md.maintainers():
                                maints.append(maint.email)
                        except IOError: pass                        
                        print cpv + " - " + inallavail + " - " + slot + " - " + ', '.join(maints)



porttree = portage.db[portage.root]['porttree']

if len(sys.argv)>1:
    for cpv in sys.argv[1:]:
        findpackagedepslotops(porttree, cpv)
else:
    for cpv in porttree.dbapi.cpv_all():
        findpackagedepslotops(porttree, cpv)
