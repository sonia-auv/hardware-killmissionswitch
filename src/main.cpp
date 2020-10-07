/***
 * 
 * Example code: This code is a simple program that turn on/off a LED with a button while another LED flash.
 * 
 ***/

#include "main.h"

RS485 rs(SLAVE_killMission);

Thread thread_killswitch;
Thread thread_missionswitch;

void function_kill()
{
  uint8_t cmd_array[1] = {CMD_KILL};
  uint8_t buffer_receiver[255];
  uint8_t buffer_send[255];
  uint8_t nb_command = 1;
  uint8_t nb_byte_send = 1;

  while(1)
  {
    rs.read(cmd_array,nb_command,buffer_receiver);
    if(Killswitch.read())
    {
      buffer_send[0] = 1;
    }
    else
    {
      buffer_send[0] = 0;
    }
    rs.write(SLAVE_killMission,cmd_array[0],nb_byte_send,buffer_send);
  }
}

void function_mission()
{
  uint8_t cmd_array[1] = {CMD_MISSION};
  uint8_t buffer_receiver[255];
  uint8_t buffer_send[255];
  uint8_t nb_command = 1;
  uint8_t nb_byte_send = 1;

  while(1)
  {
    rs.read(cmd_array,nb_command,buffer_receiver);
    if(Missionswitch.read())
    {
      buffer_send[0] = 1;
    }
    else
    {
      buffer_send[0] = 0;
    }
    rs.write(SLAVE_killMission,cmd_array[0],nb_byte_send,buffer_send);
  }
}


int main() 
{
  thread_killswitch.start(function_kill);
  thread_killswitch.set_priority(osPriorityHigh);

  thread_missionswitch.start(function_mission);
  thread_missionswitch.set_priority(osPriorityHigh);
}