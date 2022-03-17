#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INT_STR_LEN 10

// [a-z_A-Z]
char *read_input_message(int *str_len);
void rotate(char original[], int len_org);
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
{
    int ret = EXIT_SUCCESS;
    char *str_enc, *str, *str_rot;
    int str_enc_len, str_len, str_tmp_len;

    str_enc = str = str_rot = NULL;
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

    // TODO add comapere function

    int counter = 0;
    int match = 0;
    char best_match[str_enc_len];
    char *str_tmp = malloc(str_enc_len * sizeof(char));
    for (int i = 0; i < str_len; ++i) {
        str_tmp[i] = str_enc[i];
    }
    if (str_tmp == NULL) {
        fprintf(stderr, "ERROR MALLOC\n");
        exit(-1);
    }
    for (int i = 0; i < 57; ++i) {
        for (int j = 0; j < str_enc_len; ++j) {
            if (str_tmp[j] == str[j])
                counter++;
            // printf("encode = %d; original = %d\n", str_tmp[j], str[j]);
            // printf("counter = %d; unity = %d\n", counter, match);
        }
        if (match < counter) {
            match = counter;
            counter = 0;
            memset(best_match, 0, str_enc_len);
            for (int k = 0; str_tmp[k] != '0'; ++k) {
                best_match[k] = str_tmp[k];
                printf("k = %d\n", k);
                printf("%d\n", str_tmp[10]);
            }
        } else
            counter = 0;
        rotate(str_tmp, str_enc_len);
        printf("%s\n", str_tmp);
    }
    printf("%s\n", best_match);
    free(str_tmp);

    // TODO - check if print errors
    // print_error(ret);

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

void rotate(char original[], int len_org)
{
    char c;
    for (int i = 0; i < len_org; ++i) {
        c = original[i];
        if (c == 0)
            break;
        if (c == 'Z')
            c = 'a' - 1;
        if (c == 'z')
            c = 'A' - 1;
        original[i] = c + 1;
    }
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
