/* Tower of Hanoi using Recursion */

#include <stdio.h>

/* Function declaration */
void hanoi_tower(char peg1, char peg2, char peg3, int n);

/* Function definition */
void hanoi_tower(char peg1, char peg2, char peg3, int n)
{
    if (n <= 0)
    {
        printf("Illegal entry\n");
        return;
    }

    if (n == 1)
    {
        printf("Move Disk from %c to %c\n", peg1, peg3);
        return;
    }

    hanoi_tower(peg1, peg3, peg2, n - 1);
    hanoi_tower(peg1, peg2, peg3, 1);
    hanoi_tower(peg2, peg1, peg3, n - 1);
}

/* Main function */
int main()
{
    int n;
    printf("Input the number of disks: ");
    scanf("%d", &n);

    printf("\nTower of Hanoi for %d disks:\n", n);
    hanoi_tower('X', 'Y', 'Z', n);

    return 0;
}
