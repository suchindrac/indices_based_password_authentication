#!/bin/bash

rm -f /etc/user_indices; touch /etc/user_indices
python /etc/rsa_gen_key auth
python /etc/epass
