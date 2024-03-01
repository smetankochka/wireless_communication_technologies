#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BLOCK_SIZE 256

int decoder(FILE *r_fifo, FILE *w_fifo, FILE *tracklog) {
    char buf[BLOCK_SIZE];
    char packets[256][BLOCK_SIZE];
    int number_list[256] = {0};
    int count = -1;

    while (true) {
        count += 1;
        int bytes_read = fread(buf, sizeof(char), BLOCK_SIZE, r_fifo);
        if (bytes_read <= 0) break;

        int number = buf[0];

        if (number_list[number] == 0) {
            number_list[number] = 1;
        }

        memmove(buf, buf + 1, bytes_read - 1); // Remove the first byte and shift the rest
        for (int i = 0; i < bytes_read - 1; ++i) {
            if (buf[i] == ';') {
                memmove(buf + i, buf + i + 1, bytes_read - i - 1); // Remove semicolon by shifting elements
                bytes_read -= 1;
            }
        }

        // Copy the processed packet to the packets array
        memcpy(packets[number], buf, bytes_read);
    }

    for (int i = 0; i < 256; ++i) {
        if (number_list[i] == 1) {
            fwrite(packets[i], sizeof(char), BLOCK_SIZE, w_fifo);
        }
    }

    return 0;
}
