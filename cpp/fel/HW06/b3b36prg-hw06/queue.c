#include "queue.h"

queue_t *create_queue(int capacity)
{
    queue_t *queue = (queue_t *)malloc(sizeof(queue_t));
    queue->size = capacity;
    queue->array = malloc(sizeof(void *) * queue->size); // allocated array
    queue->num_entries = 0;                              // empty queue
    queue->head = 0;
    queue->tail = 0;
    return queue;
}

void delete_queue(queue_t *queue)
{
    if (queue) {
        free(queue->array);
        free(queue);
    }
}

bool push_to_queue(queue_t *queue, void *data)
{
    if (is_full(queue)) {
        return false;
    }
    queue->array[queue->tail] = data;
    queue->num_entries++;
    queue->tail = (queue->tail + 1) % queue->size;
    return true;
}

void *pop_from_queue(queue_t *queue)
{
    void *result = NULL;

    if (!is_empty(queue)) {
        result = queue->array[queue->head];
        queue->head = (queue->head + 1) % queue->size;
        queue->num_entries--;
    }
    return result;
}

void *get_from_queue(queue_t *queue, int idx)
{

    if (idx >= 0) {

        return queue->array[idx];
    }
    return NULL;
}

int get_queue_size(queue_t *queue) { return queue->num_entries; }

int is_full(queue_t *queue) { return (queue->num_entries == queue->size); }

int is_empty(queue_t *queue) { return (queue->num_entries == 0); }
