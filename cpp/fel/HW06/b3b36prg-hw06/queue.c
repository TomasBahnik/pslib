#include "queue.h"

queue_t *create_queue(int capacity)
{
    queue_t *temp = (queue_t *)malloc(sizeof(queue_t));
    if (temp) {
        temp->data = malloc(capacity * sizeof(void *));
        if (temp->data) {
            temp->head = 0;
            temp->tail = 0;
            temp->max_size = capacity;
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

static void queue_resize(queue_t *queue)
{
    void **temp = malloc(queue->max_size * 2 * sizeof(void *));
    if (temp) {
        unsigned int i = 0;
        unsigned int h = queue->head;
        do {
            temp[i] = queue->data[h++];
            if (h == queue->max_size) {
                h = 0;
            }
            i++;
        } while (h != queue->tail);
        free(queue->data);
        queue->data = temp;
        queue->head = 0;
        queue->tail = queue->max_size;
        queue->max_size *= 2;
        queue->is_full = 0;
    }
}

static unsigned int queue_is_empty(const queue_t *queue)
{
    return (queue->head == queue->tail) && !queue->is_full;
}

bool push_to_queue(queue_t *queue, void *data)
{
    unsigned int result;
    if (queue->is_full) {
        queue_resize(queue);
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
// pop = remove, peek is not in header
void *pop_from_queue(queue_t *queue)
{
    void *data = NULL;
    if (!queue_is_empty(queue)) {
        if (queue->is_full) {
            queue->is_full = 0;
        }
        data = queue->data[queue->head++];
        if (queue->head == queue->max_size) {
            queue->head = 0;
        }
    }
    return data;
}

void *get_from_queue(queue_t *queue, int idx)
{
    if (queue->head == queue->tail) {
        return NULL;
    }
    queue->head = (queue->head + 1) % queue->max_size;
    return queue->data[queue->head - idx];
}

int get_queue_size(queue_t *queue)
{
    unsigned int count;
    if (queue_is_empty(queue)) {
        count = 0;
    } else if (queue->is_full) {
        count = queue->max_size;
    } else if (queue->tail > queue->head) {
        count = queue->tail - queue->head;
    } else {
        count = queue->max_size - queue->head;
        if (queue->tail > 0) {
            count += queue->tail - 1;
        }
    }
    return count;
}
