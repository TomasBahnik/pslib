#include "queue.h"

queue_t *create_queue(int max_size)
{
    queue_t *temp = (queue_t *)malloc(sizeof(queue_t));
    if (temp) {
        temp->data = malloc(max_size * sizeof(void *));
        if (temp->data) {
            temp->head = 0;
            temp->tail = 0;
            temp->max_size = max_size;
            temp->is_full = 0;
        } else {
            free(temp);
            temp = NULL;
        }
    }
    return temp;
}

void delete_queue(queue_t *queue)
{
    if (queue) {
        free(queue->data);
        free(queue);
    }
}

bool push_to_queue(queue_t *queue, void *data)
{
    unsigned int result;
    if (queue->is_full) {
        cirque_resize(queue);
        if (queue->is_full) {
            result = 0;
        }
    }
    if (!queue->is_full) {
        queue->data[queue->tail++] = data;
        if (queue->tail == queue->max_size) {
            queue->tail = 0;
        }
        if (queue->tail == queue->head) {
            queue->is_full = 1;
        }
        result = 1;
    }
    return result;
}

void *pop_from_queue(queue_t *queue)
{
    void *data = NULL;
    if (!cirque_is_empty(queue)) {
        data = queue->data[queue->head];
    }
    return data;
}

void *get_from_queue(queue_t *queue, int idx)
{
    if (queue->head == queue->tail) {
        printf("Queue Underflow!\n");
        return NULL;
    }
    queue->head = (queue->head + 1) % queue->max_size;
    return queue->data[idx];
}

int get_queue_size(queue_t *queue)
{
    printf("get queue size\n");
    return queue->max_size;
}
