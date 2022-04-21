#include "queue.h"

queue_t *create_queue(int capacity)
{
    queue_t *queue = (queue_t *)malloc(sizeof(queue_t));
    queue->size = capacity;
    queue->array = malloc(sizeof(void *) * queue->size);
    queue->num_entries = 0; // empty
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
    // TODO
    printf("get from queue\n");
    return 0;
}

int get_queue_size(queue_t *queue)
{
    // TODO
    printf("get queue size\n");
    return 0;
}
int is_full(queue_t *queue)
{
    return (queue->num_entries == queue->size);
    // if ((queue->tail + 1) % queue->size == queue->head)
    //     return 1;
    // return 0;
}
int is_empty(queue_t *queue)
{
    return (queue->num_entries == 0);
    // if (queue->tail == -1 && queue->head == -1)
    //     return 1;
    // return 0;
}

// int main()
// {
//     queue_t q1;

//     // create_queue(&q1, 3); // first parametr is name of queue
//     // second parametr is lenght of queue
//     create_queue(3);

//     push_to_queue(&q1, 58); // add 58
//     push_to_queue(&q1, 8);  // add 8
//     push_to_queue(&q1, 54); // add 54

//     void *t;
//     while ((t = pop_from_queue(&q1)) != QUEUE_EMPTY) {
//         printf("t = %d\n",
//                (int)t); // poping elements while queue isn't empty
//     }

//     delete_queue(&q1); // free queue
// }
