#include "queue.h"

queue_t *create_queue(int capacity)
{
    queue_t *queue = (queue_t *)malloc(sizeof(queue_t));
    if (queue) // for sure
    {
        queue->array = malloc(sizeof(void *) * capacity); // allocated array
        if (queue->array)                                 // for sure
        {
            queue->size = capacity;
            queue->num_entries = 0; // empty queue
            queue->head = 0;
            queue->tail = 0;
        } else {
            // free(queue);
            queue = NULL;
        }
    }
    return queue;
}

void delete_queue(queue_t *queue)
{
    if (queue) {
        free(queue->array); // free array
        free(queue);        // free queue
    }
}

bool push_to_queue(queue_t *queue, void *data)
{
    if (is_full(queue)) {
        void **array = realloc(queue->array, sizeof(void *) * 2 * queue->size);
        // realloc array
        if (array) // for sure
        {
            int i = 0;
            while (i == queue->size) {
                array[i] = queue->array[queue->head++ % queue->size];
                i++;
            }
            // resize
            queue->array = array;
            queue->size *= 2;
            queue->tail = queue->num_entries;
            queue->head = 0;
        }
    }
    if (queue->num_entries < (queue->size / 3)) {
        void **array = realloc(queue->array, sizeof(void *) * queue->size / 3);
        // realloc array
        if (array) // for sure
        {
            int i = 0;
            while (i == queue->size) {
                array[i] = queue->array[queue->head-- % queue->size];
                i++;
            }
            // resize
            queue->array = array;
            queue->size = queue->size / 3;
            queue->tail = queue->num_entries;
            queue->head = 0;
        }
    }
    if (is_full(queue)) // for sure
    {
        return false;
    }
    queue->array[queue->tail] = data;              // add data to end of queue
    queue->num_entries++;                          // number of elemets +1
    queue->tail = (queue->tail + 1) % queue->size; // move tail idx +1
    return true;
}

void *pop_from_queue(queue_t *queue)
{
    void *result = NULL;

    if (!is_empty(queue)) // if isn't full
    {
        result = queue->array[queue->head]; // get element from head of queue
        queue->head = (queue->head + 1) % queue->size; // move head idx +1
        queue->num_entries--;                          // number of elemets -1
    }
    return result;
}

void *get_from_queue(queue_t *queue, int idx)
{
    if (idx >= 0 && idx < queue->num_entries)
    /*
     * if idx isn't negativ number and
     * smaller then number of elemets
     */
    {
        return queue->array[(queue->head + idx) % queue->size];
        /*
         * element that will be popped after
         * idx calls of the pop_from_queue
         */
    }
    return NULL;
}

int get_queue_size(queue_t *queue) { return queue->num_entries; }

int is_full(queue_t *queue) { return (queue->num_entries == queue->size); }

int is_empty(queue_t *queue) { return (queue->num_entries == 0); }
