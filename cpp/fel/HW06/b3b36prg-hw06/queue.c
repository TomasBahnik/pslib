#include "queue.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

enum { QUEUE_EMPTY, INT_MIN };

// queue_t *create_queue(int capacity)
// {
//     queue_t *queue = (queue_t *)malloc(sizeof(queue_t));
//     queue->size = capacity;
//     queue->array = malloc(sizeof(int) * queue->size);
//     queue->num_entries = 0; // empty
//     queue->head = 0;
//     queue->tail = 0;
//     return queue;
// }

void create_queue(queue_t *queue, int capacity)
{
    queue->size = capacity;
    queue->array = malloc(sizeof(int) * 2 * queue->size);
    queue->num_entries = 0; // empty
    queue->head = 0;
    queue->tail = 0;
}

void delete_queue(queue_t *queue)
{
    free(queue->array);
    printf("delete queue\n");
}

bool push_to_queue(queue_t *queue, int data)
{
    if (is_full(queue)) {
        // fprintf(stderr, "queue is overflow !");
        return false;
    }
    // queue->head = queue->tail = 0;
    queue->array[queue->tail] = data;
    queue->num_entries++;
    queue->tail = (queue->tail + 1) % queue->size;

    printf("push to queue\n");
    // printf("%d\n", data);
    return true;
}

int pop_from_queue(queue_t *queue)
{
    int result;

    if (is_empty(queue)) {
        // fprintf(stderr, "queue is empty !");
        return QUEUE_EMPTY;
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

int main()
{
    queue_t q1;

    create_queue(&q1, 3); // first parametr is name of queue
                          // second parametr is lenght of queue

    push_to_queue(&q1, 58); // add 58
    push_to_queue(&q1, 8);  // add 8
    push_to_queue(&q1, 54); // add 54

    int t;
    while ((t = pop_from_queue(&q1)) != QUEUE_EMPTY) {
        printf("t = %d\n", t); // poping elements while queue isn't empty
    }

    delete_queue(&q1); // free queue
}
