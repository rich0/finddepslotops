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


def findpackagedepslotops(porttree, cpv):
    depstr = porttree.dbapi.aux_get(cpv, ["RDEPEND"])[0]
#    uselist = porttree.dbapi.aux_get(cpv, ["IUSE"])[0] #cleandeps = portage.dep.use_reduce(depstr,uselist)
    cleandeps = portage.dep.paren_reduce(depstr)
    for indep in portage.dep.flatten(cleandeps):
        if (portage.dep.isvalidatom(indep)): # not indep.endswith("=") and
            indepslot = portage.dep.dep_getslot(indep)
            if indepslot == None or not indepslot.endswith("="):
                allavail = porttree.dep_match(indep)
                for inallavail in portage.dep.flatten(allavail):
                    slot = porttree.dbapi.aux_get(inallavail, ["SLOT"])[0]
                    if slot.find("/") > 0:
                        print cpv + " - " + inallavail + " - " + slot



porttree = portage.db[portage.root]['porttree']

if len(sys.argv)>1:
    for cpv in sys.argv[1:]:
        findpackagedepslotops(porttree, cpv)
else:
    for cpv in porttree.dbapi.cpv_all():
        findpackagedepslotops(porttree, cpv)