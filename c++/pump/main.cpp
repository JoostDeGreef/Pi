#include <iostream>
#include "pigpio++.hpp"

using namespace std;

int main()
{
  int res = EXIT_FAILURE;
  try
  {
    
  
    int res = EXIT_SUCCESS;
  }
  except(GPIO::Exception & ex)
  {
    std::cerr << ex.what() << std::endl;
  }
  
  return res;
}

