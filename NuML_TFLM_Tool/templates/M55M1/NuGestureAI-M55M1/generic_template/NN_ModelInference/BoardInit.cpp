/**************************************************************************//**
 * @file     BoardInit.cpp
 * @version  V1.00
 * @brief    Target board initiate function
 *
 * @copyright SPDX-License-Identifier: Apache-2.0
 * @copyright Copyright (C) 2023 Nuvoton Technology Corp. All rights reserved.
 ******************************************************************************/
#include <cstdio>

#include "NuMicro.h"
#include "log_macros.h"

#include "ethosu_npu_init.h"

#define DESIGN_NAME "M55M1"
#define HYPERRAM_SPIM_PORT SPIM0        //For NuMaker-M55M1 board

static void SDCard0_PinConfig(void)
{
	/* Set multi-function pin for SDH */
    SET_SD0_nCD_PD13();
    SET_SD0_CLK_PE6();
    SET_SD0_CMD_PE7();
    SET_SD0_DAT0_PE2();
    SET_SD0_DAT1_PE3();
    SET_SD0_DAT2_PE4();
    SET_SD0_DAT3_PE5();
}

static void SDCard1_PinConfig(void)
{
	/* Set multi-function pin for SDH */
    SET_SD1_nCD_PA6();
    SET_SD1_CLK_PB6();
    SET_SD1_CMD_PA5();
    SET_SD1_DAT0_PA8();
    SET_SD1_DAT1_PA9();
    SET_SD1_DAT2_PA10();
    SET_SD1_DAT3_PA11();
}

/**
 * @brief  Set debug UART multi-function pins
 *
 * @param  None
 *
 * @return None
 */
void SetDebugUartMFP(void)
{
#if (!defined(DEBUG_ENABLE_SEMIHOST) || (DEBUG_ENABLE_SEMIHOST == 1)) && !defined(OS_USE_SEMIHOSTING)

    /* Set GPH5 as UART6 RXD and GPH4 as UART6 TXD */
    SET_UART5_RXD_PB4();
    SET_UART5_TXD_PB5();
#endif
}

/**
 * @brief    Set debug UART clock source and enable module clock
 *
 * @param    None
 *
 * @return   None
 */
void SetDebugUartCLK(void)
{
#if (!defined(DEBUG_ENABLE_SEMIHOST) || (DEBUG_ENABLE_SEMIHOST == 1)) && !defined(OS_USE_SEMIHOSTING)
    /* Enable External HXT clock */
    CLK_EnableXtalRC(CLK_SRCCTL_HXTEN_Msk);

    /* Waiting for HXT clock ready */
    CLK_WaitClockReady(CLK_STATUS_HXTSTB_Msk);
    /* Select UART5 clock source from HIRC */
    CLK_SetModuleClock(UART5_MODULE, CLK_UARTSEL0_UART5SEL_HIRC, CLK_UARTDIV0_UART5DIV(1));
    /* Enable UART clock */
    CLK_EnableModuleClock(UART5_MODULE);

    /* Reset UART module */
    SYS_ResetModule(SYS_UART5RST);
#endif
}


static void SYS_Init(void)
{
    /*---------------------------------------------------------------------------------------------------------*/
    /* Init System Clock                                                                                       */
    /*---------------------------------------------------------------------------------------------------------*/

    /* Enable Internal RC 12MHz clock */
    CLK_EnableXtalRC(CLK_SRCCTL_HIRCEN_Msk);

    /* Waiting for Internal RC clock ready */
    CLK_WaitClockReady(CLK_STATUS_HIRCSTB_Msk);

    /* Enable HXT clock */
    CLK_EnableXtalRC(CLK_SRCCTL_HXTEN_Msk);

    /* Waiting for HXT clock ready */
    CLK_WaitClockReady(CLK_STATUS_HXTSTB_Msk);

    /* Switch SCLK clock source to APLL0 and Enable APLL0 220MHz clock */
    CLK_SetBusClock(CLK_SCLKSEL_SCLKSEL_APLL0, CLK_APLLCTL_APLLSRC_HXT, FREQ_220MHZ);

    /* Enable APLL1 clock */
    CLK_EnableAPLL(CLK_APLLCTL_APLLSRC_HXT, FREQ_220MHZ, CLK_APLL1_SELECT);


    /* Update System Core Clock */
    /* User can use SystemCoreClockUpdate() to calculate SystemCoreClock. */
    SystemCoreClockUpdate();

    /* Enable GPIO module clock */
    CLK_EnableModuleClock(GPIOA_MODULE);
    CLK_EnableModuleClock(GPIOB_MODULE);
    CLK_EnableModuleClock(GPIOC_MODULE);
    CLK_EnableModuleClock(GPIOD_MODULE);
    CLK_EnableModuleClock(GPIOE_MODULE);
    CLK_EnableModuleClock(GPIOF_MODULE);
    CLK_EnableModuleClock(GPIOG_MODULE);
    CLK_EnableModuleClock(GPIOH_MODULE);
    CLK_EnableModuleClock(GPIOI_MODULE);
    CLK_EnableModuleClock(GPIOJ_MODULE);

    /* Enable FMC0 module clock to keep FMC clock when CPU idle but NPU running*/
    CLK_EnableModuleClock(FMC0_MODULE);

    /* Enable NPU module clock */
    CLK_EnableModuleClock(NPU0_MODULE);

    /* Enable CCAP0 module clock */
    CLK_EnableModuleClock(CCAP0_MODULE);

    /* Enable SDH1 module clock source as HCLK and SDH1 module clock divider as 4 */
    CLK_SetModuleClock(SDH1_MODULE, CLK_SDHSEL_SDH1SEL_APLL1_DIV2, CLK_SDHDIV_SDH1DIV(5));
    CLK_EnableModuleClock(SDH1_MODULE);

    /* Select UART module clock source and clock divider */
    SetDebugUartCLK();

    /*---------------------------------------------------------------------------------------------------------*/
    /* Init I/O Multi-function                                                                                 */
    /*---------------------------------------------------------------------------------------------------------*/

    /* Set multi-function pins for UART RXD and TXD */
    SetDebugUartMFP();

    SDCard1_PinConfig();
}

/**
  * @brief Initiate the hardware resources of board
  * @return 0: Success, <0: Fail
  * @details Initiate clock, UART, NPU, hyperflash/hyperRAM
  * \hideinitializer
  */
int BoardInit(void)
{
    /* Unlock protected registers */
    SYS_UnlockReg();

    SYS_Init();

    /* UART init - will enable valid use of printf (stdout
     * re-directed at this UART (UART6) */
    InitDebugUart();

    SYS_LockReg();                   /* Unlock register lock protect */

    SDH_Open_Disk(SDH1, CardDetect_From_GPIO);

    info("%s: complete\n", __FUNCTION__);

#if defined(ARM_NPU)

    int state;

    /* If Arm Ethos-U NPU is to be used, we initialise it here */
    if (0 != (state = arm_ethosu_npu_init()))
    {
        return state;
    }

#endif /* ARM_NPU */

    /* Print target design info */
    info("Target system: %s\n", DESIGN_NAME);

    return 0;
}


