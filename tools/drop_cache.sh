#!/bin/sh -v

sync
echo 3 > /proc/sys/vm/drop_caches
