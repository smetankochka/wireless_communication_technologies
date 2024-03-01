#include <stdio.h>
#include <stdlib.h>
#define BLOCK_SIZE 256
#include <string.h>

int encoder(FILE *r_fifo, FILE *w_fifo) {
    char buf[BLOCK_SIZE + 1];
    int num = 0;

    while (true) {
        int bytes_read = fread(buf + 1, sizeof(char), BLOCK_SIZE, r_fifo);
        if (bytes_read <= 0) break;

        buf[0] = num;
        num++;

        if (bytes_read < BLOCK_SIZE) {
            memset(buf + 1 + bytes_read, ';', BLOCK_SIZE - bytes_read);
            bytes_read = BLOCK_SIZE;
        }

        fwrite(buf, sizeof(char), bytes_read, w_fifo);
    }

    return 0;
}
