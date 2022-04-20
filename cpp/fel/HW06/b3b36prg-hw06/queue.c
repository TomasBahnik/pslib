#include "queue.h"
#include <stdio.h>

enum { ERROR_OUTPUT = 101, OK = 1 };

queue_t *create_queue(int capacity)
{
    queue_t *queue = (queue_t *)malloc(sizeof(queue_t));
    queue->size = capacity;
    // queue->array = malloc(sizeof(int) * queue->size);
    queue->num_entries = 0; // empty
    queue->head = 0;
    queue->tail = 0;
    return queue;
}

void delete_queue(queue_t *queue)
{
    free(queue->array);
    printf("delete queue");
}

bool push_to_queue(queue_t *queue, void *data)
{
    if (is_full(queue)) {
        fprintf(stderr, "queue is overflow !");
        return false;
    } else {
        queue->head = queue->tail = 0;
        queue->array[queue->tail] = data;
        queue->tail = (queue->tail + 1) % queue->size;
        queue->num_entries++;
    }

    printf("push to queue\n");
    printf("%d\n", data);
    return true;
}

void *pop_from_queue(queue_t *queue)
{
    int result;

    if (is_empty(queue)) {
        fprintf(stderr, "queue is empty !");
        // return 1;
    }
    result = queue->array[queue->head];
    queue->head = (queue->head + 1) % queue->size;
    queue->num_entries--;
    printf("pop from queue\n");
    return result;
}

void *get_from_queue(queue_t *queue, int idx)
{
    printf("get from queue\n");
    return 0;
}

int get_queue_size(queue_t *queue)
{
    printf("get queue size\n");
    return 0;
}
int is_full(queue_t *queue)
{
    if ((queue->tail + 1) % queue->size == queue->head)
        return 1;
    return 0;
}
int is_empty(queue_t *queue)
{
    if (queue->tail == -1 && queue->head == -1)
        return 1;
    return 0;
}
