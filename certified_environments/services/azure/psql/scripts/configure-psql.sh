#!/bin/bash -e

sudo postgresql-setup initdb

ctx instance runtime-properties master_username postgres

