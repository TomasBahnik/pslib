#ifndef __QUEUE_H__
#define __QUEUE_H__

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

/* Queue structure which holds all necessary data */
typedef struct {
    int head;
    int tail;
    int size;
    int num_entries;
    void **array;
} queue_t;

/* creates a new queue with a given size */
// queue_t *create_queue(int capacity);
void create_queue(queue_t *queue, int capacity);

/* deletes the queue and all allocated memory */
void delete_queue(queue_t *queue);

/*
 * inserts a reference to the element into the queue
 * returns: true on success; false otherwise
 */
bool push_to_queue(queue_t *queue, int data);

/*
 * gets the first element from the queue and removes it from the queue
 * returns: the first element on success; NULL otherwise
 */
int pop_from_queue(queue_t *queue);

/*
 * gets idx-th element from the queue, i.e., it returns the element that
 * will be popped after idx calls of the pop_from_queue()
 * returns: the idx-th element on success; NULL otherwise
 */
void *get_from_queue(queue_t *queue, int idx);

/* gets number of stored elements */
int get_queue_size(queue_t *queue);

int is_full(queue_t *q);

int is_empty(queue_t *q);

#endif /* __QUEUE_H__ */
