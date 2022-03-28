#include <stdio.h>
#include <stdlib.h>

#define END_OF_LINE 1;
#define NO_END_OF_LINE 0;
#define END_OF_FILE 2;
#define ALLOC_SIZE 15;
// variable
// it is use to extend capacity

typedef struct {
    char *line;
    int size;
    int capacity;
} str_line;

void init_line(str_line *my_line);
void realloc_line(str_line *my_line);
void free_line(str_line *my_line);
int read_line(str_line *my_line, FILE *f);

int main(int argc, char *argv[])
{
    str_line line;
    init_line(&line);
    read_line(&line, stdin);
    printf("%s\n", line.line);
    free_line(&line);
    return 0;
}

void init_line(str_line *my_line) // alloc space for line
{
    my_line->line = (char *)malloc(sizeof(char));
    my_line->size = 0;
    my_line->capacity = 1;
    my_line->line[0] = '\0';
}

void realloc_line(str_line *my_line) // extend allocated space for line
{
    my_line->capacity += ALLOC_SIZE;
    my_line->line = realloc(my_line->line, my_line->capacity * sizeof(char));
}

void free_line(str_line *my_line) // free line
{
    if (my_line->line != NULL) {
        free(my_line->line);
    }
}

int read_line(str_line *my_line, FILE *f)
{
    int last_line = NO_END_OF_LINE;
    if (my_line->size + 2 >= my_line->capacity) {
        realloc_line(my_line);
    }
    while (!last_line) {
        char x = fgetc(f);
        switch (x) {
        case '\n':
            last_line = END_OF_LINE;
            break;
        case EOF:
            last_line = END_OF_FILE;
            break;
        default:
            my_line->line[my_line->size++] = x;
            break;
        }
    }
    my_line->line[my_line->size++] = '\0';
    return last_line;
}
