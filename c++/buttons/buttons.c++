#include <iostream>
#include <iostream>
#include <pigpio.h>

using namespace std;

const unsigned int GPIO_BTN0 = 14;
const unsigned int GPIO_BTN1 = 18;
const unsigned int GPIO_LED_PWR = 47;

int led_state = 0;

void buttonCallback(int gpio, int level, uint32_t tick);

bool init()
{
  int pigpioVersion = gpioInitialise();
  if(pigpioVersion == PI_INIT_FAILED)
  {
    cerr << "pigpoi initialisation failed." << endl; 
    return false;
  }
  else
  {
    cout << "pigpoi version " << pigpioVersion << " initialised." << endl; 
//    cout << "hardware revision number = " << gpioHardwareRevision() << "." << endl;
  }
  auto modeToString = [](unsigned int mode)
  {
    switch(mode)
    {
      case PI_INPUT: return "PI_INPUT";
      case PI_OUTPUT: return "PI_OUTPUT";
      case PI_ALT0: return "PI_ALT0";
      case PI_ALT1: return "PI_ALT1";
      case PI_ALT2: return "PI_ALT2";
      case PI_ALT3: return "PI_ALT3";
      case PI_ALT4: return "PI_ALT4";
      case PI_ALT5: return "PI_ALT5";
      default: return "UNKNOWN";
    }
  };
  auto logGpioSetMode = [&modeToString](unsigned int gpio, unsigned int mode)
  {
    auto res = gpioSetMode(gpio, mode);
    switch(res)
    {
      case 0:
        cout << "gpio " << gpio << " set to " << modeToString(mode) << "." << endl;
        return true;
      case PI_BAD_GPIO:
        cerr << "gpioSetMode(" << gpio << "," << modeToString(mode) << ") -> PI_BAD_GPIO." << endl;
        break;
      case PI_BAD_MODE:
        cerr << "gpioSetMode(" << gpio << "," << modeToString(mode) << ") -> PI_BAD_MODE." << endl;
        break;
      default:
        cerr << "gpioSetMode(" << gpio << "," << modeToString(mode) << ") -> UNKNOWN ERROR." << endl;
        break;
    }
    return false;
  };
  auto logGpioSetAlertFunc = [](unsigned int gpio, gpioAlertFunc_t f)
  {
    auto res = gpioSetAlertFunc(gpio,f);
    switch(res)
    {
      case 0:
        cout << "callback installed for gpio " << gpio << "." << endl;
        return true;
      case PI_BAD_USER_GPIO:
        cerr << "gpioSetAlertFunc(" << gpio << ",f) -> PI_BAD_USER_GPIO." << endl;
        break;
      default:
        cerr << "gpioSetAlertFunc(" << gpio << ",f) -> UNKNOWN ERROR." << endl;
        break;
    }
    return false;
  };
  return logGpioSetMode(GPIO_BTN0, PI_INPUT)
      && logGpioSetMode(GPIO_BTN1, PI_INPUT)
      && logGpioSetMode(GPIO_LED_PWR, PI_OUTPUT)
      && logGpioSetAlertFunc(GPIO_BTN0, &buttonCallback)
      && logGpioSetAlertFunc(GPIO_BTN1, &buttonCallback);
}

void buttonCallback(int gpio, int level, uint32_t tick)
{
  switch(level)
  {
    case 1: // rising edge
cout << "." << flush;
      led_state = 1 - led_state;
      gpioWrite(GPIO_LED_PWR, led_state);
      break;
    default:
      break;
  }
}

int main()
{
  int res = EXIT_FAILURE;
  if(init())
  {
    res = EXIT_SUCCESS;
  }
  gpioWrite(GPIO_LED_PWR, led_state);
  
  cout << "Hit enter key to exit..." << endl;
  cin.get();
  //system("bash -i -c read -n 1");
   
  gpioTerminate();
  return res;
}

