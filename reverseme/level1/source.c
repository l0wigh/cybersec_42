#include <stdio.h>
#include <string.h>

int main(void)
{
	char real_pass[11] = "1953718111";
	char user_pass[11];

	printf("Please enter key: ");
	scanf("%s", user_pass);
	if (strcmp(user_pass, real_pass) == 0)
		printf("Good job.\n");
	else
		printf("Nope.\n");
	return 0;
}
