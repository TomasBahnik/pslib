#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cirque.h"

int main(void)
{
    cirque *queue;
    char buf[16];
    unsigned int f;
    const unsigned int max = 32;
    const unsigned int limit = 16;

    queue = cirque_create();
    for (f = 0; f < max; f++) {
        sprintf(buf, "Item %d", f);
        if (f >= limit) {
            /* Start removing at limit to show the queue doesn't keep growing */
            char *data = cirque_remove(queue);
            printf("Removed %s\n", data);
            free(data);
        }
        printf("Inserting %s\n", buf);
        cirque_insert(queue, strdup(buf));
    }
    cirque_for_each(queue, (cirque_forfn)puts);
    printf("Size is %d (should be %d)\n", queue->size, limit);
    cirque_for_each(queue, free);
    cirque_delete(queue);

    return 0;
}