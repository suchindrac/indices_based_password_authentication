This PAM module uses indices as user passwords instead of character strings. The following is how it works:


. Authentication software (Bob) asks user for username
. User (Alice) supplies username
. Authentication software checks for the indices that Alice has marked as her password
. Authentication software creates a random string of 50 characters and shows it to Alice. It asks her to supply the characters at the indices that the she has marked as her password
. Alice selects the characters from the random string, which fall under the indices that she has selected as password (counting from index 0)
. The authentication software calculates the password by concatenating the letters at the indices mentioned by user
. Then it compares the indices supplied by Alice with the calculated password
. If both match, then the user is let in, otherwise authentication is denied

There are two basic requirements that are needed to ensure that the above mechanism is at-least partially secure:

. Requirement 1: User indices should be stored securely on file system
. Requirement 2: It should be possible to securely verify for user indices (as described in the above steps)

These two are met by the following scripts:

. Requirement 1 is handled by the scripts: rsa_gen_key and epass
. Requirement 2 is handled by pam.py

The installation procedure is given in INSTALL.txt
