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

// errors
#define ERROR_OK 0
#define ERROR_PAT 1

// structure
typedef struct {
    char *line;
    int size;
    int capacity;
} str_line;

// functions
void init_line(str_line *my_line);
void realloc_line(str_line *my_line);
void free_line(str_line *my_line);
int read_line(str_line *my_line, FILE *f);
void open_file(FILE **f, char *name_file);
void close_file(FILE **f);
int find_str(str_line my_line, char *pattern);
int len_str(char *my_str);
void print_error(int error);

int main(int argc, char *argv[])
{
    str_line line;
    FILE *f;
    int ret = ERROR_OK;
    int count = 0;
    open_file(&f, argv[2]);
    int finish_read = NO_END_OF_LINE;
    while (finish_read != END_OF_FILE) // end if is EOF(end of file)
    {
        init_line(&line);
        finish_read = read_line(&line, f); // read every line in FILE
        if (find_str(line, argv[1])) {     // if fce find_str find match
            printf("%s\n", line.line);     //---> print line
            count++;
        }
        free_line(&line);
    }
    if (count == 0)
        ret = ERROR_PAT;
    close_file(&f);
    print_error(ret);
    return ret;
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
            realloc_line(my_line); // realloc
        }
        switch (x) {
        case '\n': // at end of every line
            last_line = END_OF_LINE;
            break;
        case EOF: // at end of FILE
            last_line = END_OF_FILE;
            break;
        default:
            my_line->line[my_line->size++] = x;
            break;
        }
        // end of switch
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

// find pattern in FILE
int find_str(str_line my_line, char *pattern)
{
    int len = len_str(pattern);
    if (len == 0)
        return FIND;
    int i = 0;
    while (my_line.line[i]) {
        if (my_line.line[i] == pattern[0]) // check all letters in line with
                                           // first letter in pattern
        {
            int j = 1;
            while (j < len && i + j < my_line.size &&
                   my_line.line[i + j] == pattern[j])
                j++;
            if (j == len)
                return FIND;
        }
        i++;
    }
    return NO_FIND;
}

// count len of pattern
int len_str(char *my_str)
{
    int tmp = 0;
    while (my_str[tmp])
        tmp++;
    return tmp;
}

void print_error(int error)
{
    switch (error) {
    case ERROR_OK:
        fprintf(stderr, "ERROR_OK\n");
        break;

    case ERROR_PAT:
        fprintf(stderr, "PATTERN NOT FOUND IN FILE\n");
        break;
        // end switch
    }
}
