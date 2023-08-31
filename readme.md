# GraceDB-public

## Introduction

The GraceDB Official Client requires member authentications for many functions. The GraceDB-public package uses the official GraceDB API to communicate with the public portion of the database, which is sufficient for most non-member users. The GraceDB-public package is part of the Gravitational Wave SkyMap Stellarium plug-in project. It is used in collecting the list of GraceDB ‘Superevents’ and skymaps attached to them.

## Philosophy

Make as few requests to GraceDB as possible. Store server response in local cache for future inquires. Make minimal assumptions about the sever response content.

## Structure

- GraceDB-public
    - gracedb_public
        grace_configurations.py
        
        shared_configurations.py
        
        local_configurations.py
    
    - dynamic
        
        ~~parse.py~~
        
        cache.py
        
        util.py
        
        ~~log.py~~
        
    - ~~\log~~
        
        
    - ~~\test~~
    - cached_events
        
        local_superevents.json
        
    - ~~_temp~~