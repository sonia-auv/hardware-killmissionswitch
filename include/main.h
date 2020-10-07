#ifndef MAIN_H
#define MAIN_H

#include "rtos.h"
#include "mbed.h"
#include "pinDef.h"
#include "RS485/RS485.h"
#include "RS485/RS485_definition.h"

DigitalIn Killswitch(KILL_SWITCH);
DigitalIn Missionswitch(MISSION_SWITCH);

#endif