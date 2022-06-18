/***
 * 
 * Killswitch Circuit board program
 * Updated : 2022-05-14
 * 
 ***/

#include "main.h"

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
    buffer_send[0] = !Killswitch.read();
    rs.write(SLAVE_KILLMISSION,cmd_array[0],nb_byte_send,buffer_send);
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
    buffer_send[0] = !Missionswitch.read();
    rs.write(SLAVE_KILLMISSION,cmd_array[0],nb_byte_send,buffer_send);
  }
}

int main() 
{
  thread_killswitch.start(function_kill);
  thread_killswitch.set_priority(osPriorityHigh);

  thread_missionswitch.start(function_mission);
  thread_missionswitch.set_priority(osPriorityHigh);
}