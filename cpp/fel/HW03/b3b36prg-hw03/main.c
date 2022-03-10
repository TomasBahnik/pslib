#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define INT_STR_LEN 10

// [a-z_A-Z]
char *read_input_message(int *str_len);
char rotate(char original, int offset);
void shift(const char *src, char *dst, int offset);
int compare(const char *str1, const char *str2);

enum { ERROR_INPUT = 100, ERROR_LENGHT = 101 };
const char *const error_str_input = "Error: Chybny vstup!";
const char *const error_str_lenght = "Error: Chybna delka vstupu!";

int main(int argc, char *argv[])
{ //
    int ret;
    char *str_enc, *str, *str_tmp;
    int str_enc_len, str_len, str_tmp_len;

    str_enc = str = str_tmp = NULL;
    str_enc_len = str_len = str_tmp_len = 0;

    str_enc = read_input_message(&str_enc_len);
    if (str_enc) {
        str = read_input_message(&str_len);
    }
    if (str_enc == NULL || str == NULL) {
        ret = ERROR_INPUT;
    } else if (str_enc_len != str_len) {
        ret = ERROR_LENGHT;
    }

    switch (ret) {
    case ERROR_INPUT:
        fprintf(stderr, "%s\n", error_str_input);
        break;

    case ERROR_LENGHT:
        fprintf(stderr, "%s\n", error_str_lenght);
        break;
    }

    free(str_enc);
    free(str);
    free(str_tmp);

    return 0;
}

char *read_input_message(int *str_len)
{
    int capacity = INT_STR_LEN;
    int len = 0;
    char *str = malloc(capacity);
    if (str == NULL) {
        fprintf(stderr, " ERROR MALLOC\n"); // improbable
    } else {
        int a;
        while ((a = getchar()) != EOF && a != '\n') {
            if (capacity == len) { // reallocate
                char *tmp = realloc(str, capacity * 2);
                if (tmp == NULL) {
                    free(str);
                    str = NULL;
                    len = 0;
                    break;
                }
            }
            str[len++] = a;
        }
    }
    *str_len = len;
    return str;
}

char rotate(char original, int offset)
{
    //
    return 0;
}

void shift(const char *src, char *dst, int offset)
{
    //
}

int compare(const char *str1, const char *str2)
{
    //
    return 0;
}
