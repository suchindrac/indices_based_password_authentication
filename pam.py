#!/usr/bin/python

#
# PAM module to perform authentication based on indices
#
import syslog
import random
from M2Crypto import *
from subprocess import call
import base64


import random
from subprocess import call
import os
import string

from random import shuffle

import random, string


#
# These will be required later for designing encryption system to store indices
#

pub_key = "/etc/auth_public_key.pem"
priv_key = "/etc/auth_private_key.pem"

priv = RSA.load_key(priv_key)
pub = RSA.load_pub_key(pub_key)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

#
# This is in design
#
def get_indices(user_in):
  syslog.syslog("pamd: Getting indices for user %s" % (user_in))
  fd = open('/etc/user_indices', 'r')
  syslog.syslog("pamd: Reading file")
  encoded_data = fd.read()
  syslog.syslog("pamd: Decoding and decrypting ...")
  decoded_data = base64.b64decode(encoded_data)
  decrypted_data = priv.private_decrypt(decoded_data, RSA.pkcs1_oaep_padding)
  user_dict = {}
  for line in decrypted_data.split("\n"):
    try:
      (user, indices_cs) = line.split("=")
    except:
      continue
    user = user.strip()
    indices_cs = indices_cs.strip()
    user_dict[user] = indices_cs

  try:
      syslog.syslog("pamd: Successfully obtained user indices")
      return user_dict[user_in]
  except:
    return None

def shuffle_word(word):
  word = list(word)
  shuffle(word)
  return ''.join(word)

def local_auth(pamh, flags, argv):
  syslog.syslog("pamd: Start local authentication")

  user = pamh.get_user()

  rand_num = randomword(50)
  check_rand = ""
  if indices_cs != "":
    for index in indices_list:
      index_int = int(index, 10)
      check_rand = check_rand + rand_num[index_int]

  if pamh.authtok == None:
    syslog.syslog("pamd: Got no password in authtok - trying through conversation")
  passmsg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Select characters from: %s" % (str(rand_num)))
  rsp = pamh.conversation(passmsg)
  pamh.authtok = rsp.resp

#
# ... Add some more verifications if you want :)
#

  if (pamh.authtok == check_rand):

#
# Add more conditions if you want :)
#
    return pamh.PAM_SUCCESS
  else:
    return pamh.PAM_AUTH_ERR

def pam_sm_authenticate(pamh, flags, argv):
  syslog.syslog("pamd: Start index based authentication for service %s" % (pamh.service))
  if pamh.service == "unity":
    syslog.syslog("pamd: Processing authentication for unity service")
    return_value = local_auth(pamh, flags, argv)
    return return_value

  syslog.syslog("pamd: Getting username")
  user = pamh.get_user()
  syslog.syslog("pamd: Calling get_indices(%s)" % (user))
  indices_cs = get_indices(user)
  indices_list = []
  if indices_cs != "":
    indices_list = indices_cs.split(",")
  else:
    return pamh.PAM_AUTH_ERR

  syslog.syslog("pamd: Creating random word")
  rand_num = randomword(50)
  
  syslog.syslog("pamd: Constructing password from random string based on indices of user")
  check_rand = ""
  if indices_cs != "":
    for index in indices_list:
      index_int = int(index, 10)
      check_rand = check_rand + rand_num[index_int]

  if pamh.authtok == None:
    syslog.syslog("pamd: Got no password in authtok - trying through conversation")
  syslog.syslog("pamd: Showing random string for getting characters at indices")
  passmsg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Select characters from: %s" % (str(rand_num)))
  rsp = pamh.conversation(passmsg)
  pamh.authtok = rsp.resp

#
# ... Add some more verifications if you want :)
#
  syslog.syslog("pamd: Checking for characters returned by user vs. password constructed earlier using user indices")
  if (pamh.authtok == check_rand):

#
# Add more conditions if you want :)
#
    return pamh.PAM_SUCCESS
  else:
    return pamh.PAM_AUTH_ERR

def pam_sm_setcred(pamh, flags, argv):
  return pamh.PAM_SUCCESS

