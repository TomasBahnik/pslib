#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define INT_STR_LEN 10

// [a-z_A-Z]
char *read_input_message(int *str_len);
char rotate(char original, int offset);
void shift(const char *src, char *dst, int offset);
int compare(const char *str1, const char *str2);
void print_error(int error);

// only for test
void print_str(char *str, int len);
void print_str_rot(char *str_rot, int len);

enum { ERROR_INPUT = 100, ERROR_LENGHT = 101 };
const char *const error_str_input = "Error: Chybny vstup!";
const char *const error_str_lenght = "Error: Chybna delka vstupu!";

int main(int argc, char *argv[])
{ //
    int ret = EXIT_SUCCESS;
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

    // if (ret == EXIT_SUCCESS) {
    //     printf("Input enc message size %d\n", str_enc_len);
    //     print_str(str_enc, str_enc_len);

    //     printf("\nInput message size %d\n", str_len);
    //     print_str(str, str_len);
    // }

    // TODO - write for cyclus
    // a-zA-Z
    // char c = getchar();
    int counter = 0;
    char c;
    char str_rot[str_enc_len];
    for (int i = 'a'; i <= 'z'; ++i) {
        c = str_enc[counter];
        str_rot[counter] = c + 1;
        counter++;
        if (c == 0)
            break;
        printf("c = %d; i = %d; counter = %d\n", c, i, counter);
    }
    print_str(str_enc, str_enc_len);
    print_str_rot(str_rot, str_enc_len);
    // char c = 'a';
    // for (int i = 'a'; i <= 'z'; ++i) {
    //     printf("i: %d - %c ---> %c\n", i, c, c + (i - c));
    // }

    // for (int i = 0; i <= str_enc_len; ++i) {
    //     int a;
    //     a = getchar();
    //     printf("%d\n", a);
    // }

    // TODO - check if print errors
    // print_error(ret);

    free(str_enc);
    free(str);
    free(str_tmp);

    return ret;
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
            if (!((a >= 'a' && a <= 'z') ||
                  (a >= 'A' && a <= 'Z'))) { // input out of range
                free(str);
                str = NULL;
                len = 0;
                break;
            }

            if (capacity == len) { // reallocate
                char *tmp = realloc(str, capacity * 2);
                if (tmp == NULL) {
                    fprintf(stderr, "ERROR REALLOC\n");
                    free(str);
                    str = NULL;
                    len = 0;
                    break;
                }
                capacity *= 2;
                str = tmp;
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

void print_str(char *str, int len)
{
    if (str) {
        for (int i = 0; i < len; ++i) {
            putchar(str[i]);
        }
        putchar('\n');
    }
}
void print_str_rot(char *str_rot, int len)
{
    if (str_rot) {
        for (int i = 0; i < len; ++i) {
            putchar(str_rot[i]);
        }
        putchar('\n');
    }
}

void print_error(int error)
{
    switch (error) {
    case ERROR_INPUT:
        fprintf(stderr, "%s\n", error_str_input);
        break;

    case ERROR_LENGHT:
        fprintf(stderr, "%s\n", error_str_lenght);
        break;
    }
}