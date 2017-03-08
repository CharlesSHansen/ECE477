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
#define THRESHHOLD              3000
#define MOTOR_TIME              10
#define WAIT_TIME               6
#define NVIC_EN0_R              0xE000E100
#define SIZE_321Up              6
#define SIZE_DiamondUp          4
#define SIZE_BoxUp              5
#define SIZE_GentleUp           2
#define SIZE_LineUp             3
#define SIZE_TriUp              3

void printCurrents(void);
void clearInterrupt(uint64_t);
uint64_t getStatus();
void setPWM(int);
void updateMotors();
void pulseMotorDown(int);


volatile uint16_t CupPrevious[10];
volatile uint16_t CupCurrent[10];
volatile uint16_t CupPosition[10];
volatile uint16_t BallIn[10];
volatile uint16_t motorUp[10];
volatile uint16_t motorDown[10];
volatile int readFlag = 0;
volatile int firstRead = 1;
volatile int counterADC = 0;
volatile int counterMOTOR = 0;
volatile int motorOn = 0;
volatile int motorOff = 0;
volatile int uartFlag = 0;
volatile int uartChar = 0;

volatile uint8_t[SIZE_321Up]            _321Up = [0,1,2,3,4,5];
volatile uint8_t[10 - SIZE_321Up]       _321Down = [6,7,8,9];
volatile uint8_t[SIZE_DiamondUp]        _DiamondUp = [0,1,2,4];
volatile uint8_t[10 - SIZE_DiamondUp]   _DiamondDown = [3,5,6,7,8,9];
volatile uint8_t[SIZE_BoxUp]            _BoxUp = [1,2,4,7,8];
volatile uint8_t[10 - SIZE_BoxUp]       _BoxDown = [0,3,5,6,9];
volatile uint8_t[SIZE_GentleUp]         _GentleUp = [4,8];
volatile uint8_t[10 - SIZE_GentleUp]    _GentleDown = [0,1,2,3,5,6,7,9];
volatile uint8_t[SIZE_LineUp]           _LineUp = [1,4,8];
volatile uint8_t[10 - SIZE_LineUp]      _LineDown = [0,2,3,5,6,7,9];
volatile uint8_t[SIZE_TriUp]            _TriUp = [4,7,8];
volatile uint8_t[10 - SIZE_TriUp]       _TriDown = [0,1,2,3,5,6,9];

enum Directon {
    up,
    down
};


const eUSCI_UART_Config uartConfig =
    {
            EUSCI_A_UART_CLOCKSOURCE_SMCLK,          // SMCLK Clock Source
            78,                                     // BRDIV = 78
            2,                                       // UCxBRF = 2
            0,                                       // UCxBRS = 0
            EUSCI_A_UART_NO_PARITY,                  // No Parity
            EUSCI_A_UART_LSB_FIRST,                  // LSB First
            EUSCI_A_UART_ONE_STOP_BIT,               // One stop bit
            EUSCI_A_UART_MODE,                       // UART mode
            EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION  // Oversampling
    };

//Direction direction = down;


void main()
{
    volatile unsigned int i;
    unsigned int diff;

    // ******* GPIO *****************
    // ******************************

    P1->DIR |= BIT0 | BIT6 | BIT7;
    P1->OUT &= BIT0;

    P2->DIR |= BIT4 | BIT6;
    P2->OUT = 0;

    P10->DIR |= BIT5;
    P10->OUT &= BIT5;




    P1->OUT &= ~BIT0;                       // Clear LED to start
    P1->DIR |= BIT0;                        // Set P1.0/LED to output


    // ***************************************
    // ***************************************

    WDTCTL = WDTPW | WDTHOLD;                 // Stop WDT Interrupt

    __enable_irq(); // Enable interrupts

    //******** TIMER CONFIG ************************************************
    //**********************************************************************

    TIMER_A1->CCTL[0] = TIMER_A_CCTLN_CCIE; // TACCR0 interrupt enabled
    TIMER_A1->CCR[0] = 62500;
    TIMER_A1->CTL = TIMER_A_CTL_SSEL__SMCLK | TIMER_A_CTL_MC__UP | TIMER_A_CTL_ID__8;
    NVIC->ISER[0] = 1 << ((TA1_0_IRQn) & 31);


    TIMER_A0->CCTL[0] = TIMER_A_CCTLN_CCIE; // TACCR0 interrupt enabled
        TIMER_A0->CCR[0] = 20000;
        TIMER_A0->CTL = TIMER_A_CTL_SSEL__SMCLK | TIMER_A_CTL_MC__UP | TIMER_A_CTL_ID__8;
        NVIC->ISER[0] = 1 << ((TA0_0_IRQn) & 31);

    //********* MOTOR OUTPUT CONFIG ****************************************
    //**********************************************************************

    P5->DIR |= (BIT1 | BIT2 | BIT3 | BIT4 | BIT5);
    P4->DIR |= (BIT0 | BIT1);
    P6->DIR |= (BIT0 | BIT1);
    P9->DIR |= BIT1;

    P5->OUT &= ~(BIT1 | BIT2 | BIT3 | BIT4 | BIT5);
    P4->OUT &= ~(BIT0 | BIT1);
    P6->OUT &= ~(BIT0 | BIT1);
    P9->OUT &= ~(BIT1);

    //********* UART CONFIG ************************************************
    //**********************************************************************



    MAP_GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P3,
    GPIO_PIN2 | GPIO_PIN3, GPIO_PRIMARY_MODULE_FUNCTION);

    /* Setting DCO to 12MHz */
    MAP_CS_setDCOCenteredFrequency(CS_DCO_FREQUENCY_12);

    /* Configuring UART Module */
    MAP_UART_initModule(EUSCI_A2_BASE, &uartConfig);

    /* Enable UART module */
    MAP_UART_enableModule(EUSCI_A2_BASE);

    /* Enabling interrupts */
    MAP_UART_enableInterrupt(EUSCI_A2_BASE, EUSCI_A_UART_RECEIVE_INTERRUPT);
    MAP_Interrupt_enableInterrupt(INT_EUSCIA2);
    //MAP_Interrupt_enableSleepOnIsrExit();
    //MAP_Interrupt_enableMaster();

    //********* ADC 14 INTERRUPT CONFIG ************************************
    //**********************************************************************

    //IR SENSORS
    /*  CUP0 - P5.5
        CUP1 - P5.4
        CUP2 - P5.3
        CUP3 - P5.2
        CUP4 - P5.1
        CUP5 - P4.1
        CUP6 - P4.0
        CUP7 - P6.1
        CUP8 - P6.0
        CUP9 - P9.1*/

    //P5 Mask for ADC14 On (pins 1,2,3,4,5)
    P5SEL1 &= 0x00;
    P5SEL0 &= 0x00;
    P5SEL1 |= BIT1 | BIT2 | BIT3 | BIT4 |BIT5;
    P5SEL0 |= BIT1 | BIT2 | BIT3 | BIT4 |BIT5;
    //P4 Mask for ADC14 On (pins 0,1)
    P4SEL1 &= 0x00;
    P4SEL0 &= 0x00;
    P4SEL1 |= BIT0 | BIT1;
    P4SEL0 |= BIT0 | BIT1;
    //P6 Mask for ADC14 On (pins 0,1)
    P6SEL1 &= 0x00;
    P6SEL0 &= 0x00;
    P6SEL1 |= BIT0 | BIT1;
    P6SEL0 |= BIT0 | BIT1;
    //P9 Mask for ADC14 On (pins 1)
    P9SEL1 &= 0x00;
    P9SEL0 &= 0x00;
    P9SEL1 |= BIT1;
    P9SEL0 |= BIT1;

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
    ADC14->MCTL[0] = ADC14_MCTLN_INCH_0;   //Channel A0
    ADC14->MCTL[1] = ADC14_MCTLN_INCH_1;   //Channel A1
    ADC14->MCTL[2] = ADC14_MCTLN_INCH_2;   //Channel A2
    ADC14->MCTL[3] = ADC14_MCTLN_INCH_3;    //Channel A3
    ADC14->MCTL[4] = ADC14_MCTLN_INCH_4;   //Channel A4
    ADC14->MCTL[5] = ADC14_MCTLN_INCH_12;   //Channel A12
    ADC14->MCTL[6] = ADC14_MCTLN_INCH_13;   //Channel A13
    ADC14->MCTL[7] = ADC14_MCTLN_INCH_14;    //Channel A14
    ADC14->MCTL[8] = ADC14_MCTLN_INCH_15;    //Channel A15
    ADC14->MCTL[9] = ADC14_MCTLN_INCH_16 | ADC14_MCTLN_EOS; //Channel A16 and end stream

    uint32_t stat = ADC14_IER0_IE6 & 0xFFFFFFFF;
    ADC14->IER0 |= stat;
    stat = (ADC14_IER0_IE6 << 32);
    ADC14->IER1 |= (stat);

    SCB->SCR &= ~SCB_SCR_SLEEPONEXIT_Msk;   // Wake up on exit from ISR
    HWREG32(NVIC_EN0_R) = 0x01000000;

    //***********************************************************************
    //***********************************************************************

    for (i = 0; i<10; i++) {
        CupPrevious[i] = 0;
        CupCurrent[i] = 0;
        CupPosition[i] = 1;
        BallIn[i] = 0;
    }


    while (1)
    {

        //***** IR SENSOR HANDLE *****************
        //****************************************
        if (readFlag == 1) { //NEW VALUE READ FROM ADC
            readFlag = 0;
            //printDiffs();

            for(i = 0; i< 1; i++){
                diff = abs(CupCurrent[i] - CupPrevious[i]);
                if ((diff > THRESHHOLD) & CupPosition[i] == 1){
                    if(BallIn[i] == 0) {
                        // BALL ENTERING CUP - FLASH LIGHTS
                        BallIn[i] = 1;
                        pulseMotorDown(i);
                    }
                    else{
                        // BALL LEAVING CUP - MOVE MOTOR DOWN
                        CupPosition[i] = 0;
                        BallIn[i] = 0;
                        motorDown[i] = 1;

                    }
                }
                CupPrevious[i] = CupCurrent[i];
            }
        }

        //**** CHECK FOR RE-RACK FROM UART ************
        //*********************************************
        if (uartFlag == 1) {
            uartFlag = 0;
            switch(uartChar) {
            case 48: // 0 - 3-2-1
                // 0,1,2,3,4,5 up
                for (i = 0; i < SIZE_321Up; i++)  {
                    if (CupPosition[_321Up[i]] == 1) {
                        motorDown[_321Up[i]] = 1;
                        CupPosition[_321Up[i]] = 0;
                    }
                }
                for (i = 0; i < (10 - SIZE_321Up); i++) {
                    if (CupPosition[_321Down[i]] == 0) {
                        motorUp[_321Down[i]] = 1;
                        CupPosition[_321Down[i]] = 1;
                    }
                }
                break;
            case 49: // 1 - Diamond
                // 0,1,2,4 up
                for (i = 0; i < SIZE_DiamondUp; i++)  {
                    if (CupPosition[_DiamondUp[i]] == 1) {
                        motorDown[_DiamondUp[i]] = 1;
                        CupPosition[_DiamondUp[i]] = 0;
                    }
                }
                for (i = 0; i < (10 - SIZE_DiamondUp); i++) {
                    if (CupPosition[_321Down[i]] == 0) {
                        motorUp[_321Down[i]] = 1;
                        CupPosition[_321Down[i]] = 1;
                    }
                }
                break;
            case 50: // 2 - Box
                // 1,2,4,7,8
                break;
            case 51: // 3 - Gentlemen's
                // 4, 8
                break;
            case 52: // 4 - Line
                // 1,4,8
                break;
            case 53: // Triangle
                // 4,7,8
                break;
            default :
                break;
            }


            }
        }


        //**** CHECK FOR ANY MOTOR MOVEMENT SET *******
        //*********************************************
        P7->OUT |= BIT4 & (motorDown[0] << 4);      //Motor1 Down
        P7->OUT |= BIT5 & (motorUp[0] << 5);        //Motor1 Up
        P7->OUT |= BIT6 & (motorDown[1] << 6);      //Motor2 Down
        P7->OUT |= BIT7 & (motorUp[1] << 7);        //Motor2 Up
        P8->OUT |= BIT0 & (motorDown[2]);           //Motor3 Down
        P8->OUT |= BIT1 & (motorUp[2] << 1);        //Motor3 Up
        P3->OUT |= BIT0 & (motorDown[3]);           //Motor4 Down
        P3->OUT |= BIT1 & (motorUp[3] << 1);        //Motor4 Up
        P3->OUT |= BIT2 & (motorDown[4] << 2);      //Motor5 Down
        P3->OUT |= BIT3 & (motorUp[4] << 3);        //Motor5 Up
        P3->OUT |= BIT4 & (motorDown[5] << 4);      //Motor6 Down
        P3->OUT |= BIT5 & (motorUp[5] << 5);        //Motor6 Up
        P3->OUT |= BIT6 & (motorDown[6] << 6);      //Motor7 Down
        P3->OUT |= BIT7 & (motorUp[6] << 7);        //Motor7 Up
        P8->OUT |= BIT2 & (motorDown[7] << 2);      //Motor8 Down
        P8->OUT |= BIT3 & (motorUp[7] << 3);        //Motor8 Up
        P8->OUT |= BIT4 & (motorDown[8] << 4);      //Motor9 Down
        P8->OUT |= BIT5 & (motorUp[8] << 5);        //Motor9 Up
        P8->OUT |= BIT7 & (motorDown[9] << 2);      //Motor10 Down
        P9->OUT |= BIT0 & (motorUp[9]);             //Motor10 Up

        // If any movement, start timer
        for (i = 0; i < 10; i++) {
            if (motorDown[i] == 1 || motorUp[i] == 1) {
                motorOn = 1;
                break;
            }
        }


        //**** MOTOR TIMER DONE - TURN MOTOR OFF*******
        //*********************************************
        if (motorOff == 1) {
            // TURN ALL MOTORS OFF AT ONCE
            P5->OUT &= ~(BIT1 | BIT2 | BIT3 | BIT4 | BIT5);
            P4->OUT &= ~(BIT0 | BIT1);
            P6->OUT &= ~(BIT0 | BIT1);
            P9->OUT &= ~(BIT1);
            motorOff = 0;
            for (i = 0; i < 10; i++) {
                motorDown[i] = 0;
                motorUp[0] = 0;
            }
        }




    }
}

void pulseMotorDown(int a) {

}

void printDiffs() {
    int i;
    printf("***************************************\n");
    for (i = 0; i < 1; i++) {
        printf("%d\t%d\n",CupPrevious[i],CupCurrent[i]);
    }

}





void TA0_0_IRQHandler(void) {
    TIMER_A0->CCTL[0] &= ~TIMER_A_CCTLN_CCIFG;
    //P2->OUT ^= BIT6;
    TIMER_A0->CCR[0] += 1;
}



void TA1_0_IRQHandler(void) {
    TIMER_A1->CCTL[0] &= ~TIMER_A_CCTLN_CCIFG;

    if (motorOn == 1) {
        counterMOTOR++;
        if (counterMOTOR >= MOTOR_TIME) {
            motorOff = 1;
           // P2->OUT &= ~BIT6; // TURN ALL MOTORS OFF
            motorOn = 0;
            counterMOTOR = 0;
        }
    }
    counterADC++;
    if (counterADC >= WAIT_TIME) {
        counterADC = 0;
        ADC14->CTL0 |= ADC14_CTL0_ENC | ADC14_CTL0_SC;
        //P1->OUT = ~P1->OUT;
    }
    TIMER_A1->CCR[0] += 1;              // Add Offset to TACCR0
}

void EUSCIA2_IRQHandler(void) // Code from DriverLib example
{
    uint32_t status = MAP_UART_getEnabledInterruptStatus(EUSCI_A2_BASE);

    MAP_UART_clearInterruptFlag(EUSCI_A2_BASE, status);

    if(status & EUSCI_A_UART_RECEIVE_INTERRUPT_FLAG)
    {
        uartChar = MAP_UART_receiveData(EUSCI_A2_BASE);
        uartFlag = 1;
        printf("%c\n",MAP_UART_receiveData(EUSCI_A2_BASE));
       // MAP_UART_transmitData(EUSCI_A2_BASE, MAP_UART_receiveData(EUSCI_A2_BASE));
    }

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



