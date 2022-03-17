#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INT_STR_LEN 10

// [a-z_A-Z]
char *read_input_message(int *str_len);
void rotate(char original[], int len_org);
void compare(char str[], char str_enc[], int str_enc_len);
void print_error(int error);

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

    str_enc = read_input_message(&str_enc_len); // read first row
    if (str_enc) {
        str = read_input_message(&str_len); // read second row
    }
    if (str_enc == NULL || str == NULL) {
        ret = ERROR_INPUT; // exit if input is char from [a-z_A-Z]
    } else if (str_enc_len != str_len) {
        ret = ERROR_LENGHT; // exit if first and second row doesn't have same
                            // lenght
    } else {
        compare(str, str_enc, str_enc_len); // start comparing
    }
    print_error(ret);
    return ret;
}

char *read_input_message(int *str_len)
{
    int capacity = INT_STR_LEN;
    int len = 0;
    char *str = malloc(capacity);
    if (str == NULL) {
        fprintf(stderr, " ERROR MALLOC\n"); // improbable
        exit(-1);
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
    // this function is rotating char array (first input row)
    // it always rotate whole string plus one in ASCII table

    char c;
    for (int i = 0; i < len_org; ++i) {
        c = original[i];
        if (c == 0)
            break;
        if (c == 'Z') // condition for end of big letters in alphabet
            c = 'a' - 1;
        if (c == 'z') // condition for end of small letters in alphabet
            c = 'A' - 1;
        original[i] = c + 1; // rotate array that you call with
    }
}

void compare(char str[], char str_enc[], int str_enc_len)
{
    // this function is comparing letter by letter of our rotated char array
    // with second input row

    int counter = 0;
    int match = 0; // number of matches with input array
    char *best_match = malloc(str_enc_len * sizeof(char));
    char *str_tmp = malloc(str_enc_len * sizeof(char));
    for (int i = 0; i < str_enc_len; ++i) {
        str_tmp[i] = str_enc[i];
    }
    if ((str_tmp == NULL) || (best_match == NULL)) {
        fprintf(stderr, "ERROR MALLOC\n");
        exit(-1);
    }
    for (int i = 0; i < 57; ++i) {
        for (int j = 0; j < str_enc_len; ++j) {
            if (str_tmp[j] == str[j])
                counter++; // counting letter matches with input array
        }
        if (match < counter) {
            match = counter;
            counter = 0;
            memset(best_match, 0, str_enc_len); // everytime it find bigger
                                                // match clear temporary array
            for (int k = 0; k < str_enc_len; ++k) {
                best_match[k] =
                    str_tmp[k]; // then write in word with more matches
            }
        } else {
            counter = 0;
        }
        rotate(str_tmp, str_enc_len); // call rotate function
    }
    printf("%s\n", best_match);
    free(str_tmp);
    free(best_match);
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
        // end switch
    }
}
