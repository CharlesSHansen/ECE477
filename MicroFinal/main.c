//*****************************************************************************
//
// MSP432 main.c template - Empty main
//
//****************************************************************************

#include "msp432p401r.h"
#include "stdint.h"
#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "msp_compatibility.h"
//#include "msp.h"
#define THRESHHOLD 3000
#define WAIT_TIME 6
#define NVIC_EN0_R              0xE000E100

// Function Prototypes
void rotate_f(void);         //Forward run funtion
void rotate_b(void);         //Backward run function
void breaks(void);         //Motor stop function
void delay(void);           //Some delay
void printCurrents(void);
void clearInterrupt(uint64_t);
uint64_t getStatus();


volatile uint16_t CupPrevious[10];
volatile uint16_t CupCurrent[10];
volatile uint16_t CupPosition[10];
volatile uint16_t BallIn[10];
volatile int readFlag = 0;
volatile int firstRead = 1;
volatile int hehe = 0;
volatile int counter = 0;

void main()
{

    P1->DIR |= BIT0;
        P1->OUT |= BIT0;
    //DIR - 0 for output, 1 for input

    volatile unsigned int i;
    WDTCTL = WDTPW | WDTHOLD;                 // Stop WDT Interrupt

    __enable_irq(); // Enable interrupts

    //******** TIMER CONFIG ************************************************
    //**********************************************************************

    TIMER_A0->CCTL[0] = TIMER_A_CCTLN_CCIE; // TACCR0 interrupt enabled
    TIMER_A0->CCR[0] = 62500;
    TIMER_A0->CTL = TIMER_A_CTL_SSEL__SMCLK | TIMER_A_CTL_MC__UP | TIMER_A_CTL_ID__8;
    NVIC->ISER[0] = 1 << ((TA0_0_IRQn) & 31);

    //**********************************************************************
    //**********************************************************************

    //********* ADC 14 INTERRUPT CONFIG ************************************
    //**********************************************************************

    //IR SENSORS
    /*  CUP0 - P6.0
        CUP1 - P4.1
        CUP2 - P4.3
        CUP3 - P4.6
        CUP4 - P6.1
        CUP5 - P4.0
        CUP6 - P4.2
        CUP7 - P4.4
        CUP8 - P4.5
        CUP9 - P4.7*/

    //P4 Mask for ADC14 On (pins 0,1,2,3,4,5,6,7)
    P4SEL1 &= 0x00;
    P4SEL0 &= 0x00;
    P4SEL1 |= BIT0 | BIT1 | BIT2 | BIT3 | BIT4 |BIT5 | BIT6 | BIT7;
    P4SEL0 |= BIT0 | BIT1 | BIT2 | BIT3 | BIT4 |BIT5 | BIT6 | BIT7;
    //P6 Mask for ADC14 On (pins 0,1)
    P6SEL1 &= 0x00;
    P6SEL0 &= 0x00;
    P6SEL1 |= BIT0 | BIT1;
    P6SEL0 |= BIT0 | BIT1;

    // Enable ADC interrupt in NVIC module
    NVIC->ISER[0] = 1 << ((ADC14_IRQn) & 31);

    // Turn on ADC14, set multi conversion, no repeat mode
    ADC14->CTL0 = ADC14_CTL0_ON |
                    ADC14_CTL0_SSEL__MCLK |
                    ADC14_CTL0_DIV__1 |
                    ADC14_CTL0_PDIV__1 |
                    ADC14_CTL0_SHP |
                    ADC14_CTL0_MSC |

                    ADC14_CTL0_CONSEQ_1;
    //Configure each channel
    ADC14->MCTL[0] = ADC14_MCTLN_INCH_15;   //Channel A15
    ADC14->MCTL[1] = ADC14_MCTLN_INCH_12;   //Channel A12
    ADC14->MCTL[2] = ADC14_MCTLN_INCH_10;   //Channel A10
    ADC14->MCTL[3] = ADC14_MCTLN_INCH_7;    //Channel A7
    ADC14->MCTL[4] = ADC14_MCTLN_INCH_14;   //Channel A14
    ADC14->MCTL[5] = ADC14_MCTLN_INCH_13;   //Channel A13
    ADC14->MCTL[6] = ADC14_MCTLN_INCH_11;   //Channel A11
    ADC14->MCTL[7] = ADC14_MCTLN_INCH_9;    //Channel A9
    ADC14->MCTL[8] = ADC14_MCTLN_INCH_8;    //Channel A8
    ADC14->MCTL[9] = ADC14_MCTLN_INCH_6 | ADC14_MCTLN_EOS; //Channel A6 and end stream

    uint32_t stat = ADC14_IER0_IE6 & 0xFFFFFFFF;
    ADC14->IER0 |= stat;
    stat = (ADC14_IER0_IE6 << 32);
    ADC14->IER1 |= (stat);

    SCB->SCR &= ~SCB_SCR_SLEEPONEXIT_Msk;   // Wake up on exit from ISR
    HWREG32(NVIC_EN0_R) = 0x01000000;

    //***********************************************************************
    //***********************************************************************



    P2->OUT &= ~BIT5;
    P2->DIR |= BIT5;

    P1->OUT &= ~BIT0;                       // Clear LED to start
    P1->DIR |= BIT0;                        // Set P1.0/LED to output

    for (i = 0; i<10; i++) {
        CupPrevious[i] = 0;
        CupCurrent[i] = 0;
        CupPosition[i] = 1;
        BallIn[i] = 0;
    }

    unsigned int diff;
    //ADC14->CTL0 |= ADC14_CTL0_ENC | ADC14_CTL0_SC;
    //__sleep();
    while (1)
    {
        if (readFlag == 1) { //NEW VALUE
            readFlag = 0;
            printDiffs();
            CupPrevious[0] = CupCurrent[0];
            /*
            for(i = 0; i< 1; i++){
                diff = abs(CupCurrent[i] - CupPrevious[i]);
                if ((diff > THRESHHOLD)) {// & CupPosition[i] == 1){
                    if(BallIn[i] == 0) {
                        BallIn[i] = 1;
                        P2->OUT = ~P2->OUT;
                    }
                    else{
                        CupPosition[i] = 0;
                        BallIn[i] = 0;
                        if(i == 0)
                            P2->OUT = ~P2->OUT;                          // P1.0 = 1
                    }
                }

            }*/
        }
    }
}

void printDiffs() {
    int i;
    for (i = 0; i < 1; i++) {
        printf("%d\t%d\n",CupPrevious[i],CupCurrent[i]);
    }
}


void TA0_0_IRQHandler(void) {
    //BITBAND_PERI(TIMER_A0->CTL,TIMER_A_CTL_IFG_OFS) = 0;
    TIMER_A0->CCTL[0] &= ~TIMER_A_CCTLN_CCIFG;
    counter++;
    if (counter >= WAIT_TIME) {
        counter = 0;
        ADC14->CTL0 |= ADC14_CTL0_ENC | ADC14_CTL0_SC;
        P1->OUT = ~P1->OUT;
    }

    TIMER_A0->CCR[0] += 1;              // Add Offset to TACCR0
}


void ADC14_IRQHandler(void) {
    uint64_t status;
    status = getStatus();
    clearInterrupt(status);
    unsigned int i;

    if(status & ADC14_IER0_IE6)
    {
        //printf("hey\n");
        if (firstRead == 1) {
            for (i = 0; i < 10; i++) {
                CupPrevious[i] = ADC14->MEM[i];
                CupCurrent[i] = ADC14->MEM[i];
            }
            firstRead = 0;
            readFlag = 1;
            return;
        }

        for (i = 0; i < 10; i++) {
            CupCurrent[i] = ADC14->MEM[i];
        }
        readFlag = 1;
    }
}

void clearInterrupt(uint64_t mask) {
        uint32_t stat = mask & 0xFFFFFFFF;
        ADC14->CLRIFGR0 |= stat;
        stat = (mask >> 32);
        ADC14->CLRIFGR1 |= (stat);
}

uint64_t getStatus() {
    uint64_t irq = ((ADC14->IFGR1 << 32) | ADC14->IFGR0);
    return irq & ((ADC14->IER1 << 32) | ADC14->IER0);
}

void printADC() {
    printf("*********************************************\n");
    printf("%d\t",ADC14->MEM[0]);
    printf("%d\t",ADC14->MEM[1]);
    printf("%d\t",ADC14->MEM[2]);
    printf("%d\t",ADC14->MEM[3]);
    printf("%d\n",ADC14->MEM[4]);
    printf("%d\t",ADC14->MEM[5]);
    printf("%d\t",ADC14->MEM[6]);
    printf("%d\t",ADC14->MEM[7]);
    printf("%d\t",ADC14->MEM[8]);
    printf("%d\n",ADC14->MEM[9]);
}

void printCurrents() {
    printf("**********************************************\n");
    int i;
    for (i = 0; i < 10; i++) {
        printf("%d\t",CupCurrent[i]);
    }
    printf("\n");
}



