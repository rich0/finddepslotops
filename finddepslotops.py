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
import os
import portage

cpv=sys.argv[1]
#print cpv

porttree = portage.db[portage.root]['porttree']
depstr = (porttree.dbapi.aux_get(cpv, ["RDEPEND"])[0])
uselist = (porttree.dbapi.aux_get(cpv, ["IUSE"])[0])
#print uselist
#print depstr
#print
cleandeps = portage.dep.use_reduce(depstr,uselist)
#print cleandeps


for indep in portage.dep.flatten(cleandeps):
    if portage.dep.isvalidatom(indep):
        #print indep
        allavail=porttree.dep_match(indep)
        #print allavail
        for inallavail in portage.dep.flatten(allavail):
            #print inallavail
            slot=(porttree.dbapi.aux_get(inallavail, ["SLOT"])[0])
            if slot.find("/")>0:
                print inallavail + " - " + slot
            
        #print