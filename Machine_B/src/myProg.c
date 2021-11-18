#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <openssl/md5.h>

void hashFunction(const unsigned char* pw, unsigned char* hashedPW) {
    MD5(pw, sizeof(pw), hashedPW);
}
