#include <stdio.h>
#include <stdlib.h>

// variable
// it is use to extend capacity
#define ALLOC_SIZE 15

// constants for read_line function
#define NO_END_OF_LINE 0
#define END_OF_LINE 1
#define END_OF_FILE 2

// constants for find_str function
#define FIND 1
#define NO_FIND 0

typedef struct {
    char *line;
    int size;
    int capacity;
} str_line;

// enum { NO_END_OF_LINE = 0, END_OF_LINE = 1, END_OF_FILE = 2 };

void init_line(str_line *my_line);
void realloc_line(str_line *my_line);
void free_line(str_line *my_line);
int read_line(str_line *my_line, FILE *f);
void open_file(FILE **f, char *name_file);
void close_file(FILE **f);
int find_str(str_line my_line, char *pattern);
int len_str(char *my_str);

int main(int argc, char *argv[])
{
    str_line line;
    FILE *f;
    open_file(&f, argv[2]);
    int finish_read = NO_END_OF_LINE;
    while (finish_read != END_OF_FILE) {
        init_line(&line);
        finish_read = read_line(&line, f);
        if (find_str(line, argv[1]))
            printf("%s\n", line.line);
        free_line(&line);
    }
    close_file(&f);
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
    while (!last_line) {
        char x = fgetc(f);
        if (my_line->size + 2 >= my_line->capacity) {
            realloc_line(my_line);
        }
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

void open_file(FILE **f, char *name_file)
{
    *f = fopen(name_file, "r");
    if (*f == NULL)
        exit(1);
}

void close_file(FILE **f)
{
    if (fclose(*f) == EOF)
        exit(1);
}

int find_str(str_line my_line, char *pattern)
{
    int len = len_str(pattern);
    if (len == 0)
        return FIND;
    int i = 0;
    while (my_line.line[i]) {
        if (my_line.line[i] == pattern[0]) {
            int j = 1;
            while (j < len && i + j < my_line.size &&
                   my_line.line[i + j] == pattern[j])
                j++;
            if (j == len)
                return FIND;
        }
    }
    i++;
    return NO_FIND;
}

int len_str(char *my_str)
{
    int tmp = 0;
    while (my_str[tmp])
        tmp++;
    return tmp;
}
