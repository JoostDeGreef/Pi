#include <iostream>
#include <iostream>
#include <pigpio.h>

using namespace std;

const unsigned int GPIO_BTN0 = 14;
const unsigned int GPIO_BTN1 = 15;
const unsigned int GPIO_LED_PWR = 47;
const unsigned int GPIO_SCALE = 18;

int led_state = 1;
int scale = 0;
int max_scale = 100;

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
  auto pudToString = [](unsigned int pud)
  {
    switch(pud)
    {
      case PI_PUD_OFF: return "PI_PUD_OFF";
      case PI_PUD_DOWN: return "PI_PUD_DOWN";
      case PI_PUD_UP: return "PI_PUD_UP";
      default: return "UNKNOWN";
    }
  };
  auto logGpioSetPullUpDown = [&pudToString](unsigned int gpio, unsigned int pud)
  {
    auto res = gpioSetPullUpDown(gpio, pud);
    switch(res)
    {
      case 0:
        cout << "gpio " << gpio << " pull up/down set to " << pudToString(pud) << "." << endl;
        return true;
      case PI_BAD_GPIO:
        cerr << "gpioSetPullUpDown(" << gpio << "," << pudToString(pud) << ") -> PI_BAD_GPIO." << endl;
        break;
      case PI_BAD_PUD:
        cerr << "gpioSetPullUpDown(" << gpio << "," << pudToString(pud) << ") -> PI_BAD_PUD." << endl;
        break;
      default:
        cerr << "gpioSetPullUpDown(" << gpio << "," << pudToString(pud) << ") -> UNKNOWN ERROR." << endl;
        break;
    }
    return false;
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
  auto logGpioGlitchFilter = [](unsigned int gpio, unsigned int steady)
  {
    auto res = gpioGlitchFilter(gpio, steady);
    switch(res)
    {
      case 0:
        cout << "gpio " << gpio << " glitch filter set to " << steady << "." << endl;
        return true;
      case PI_BAD_GPIO:
        cerr << "gpioGlitchFilter(" << gpio << "," << steady << ") -> PI_BAD_GPIO." << endl;
        break;
      case PI_BAD_FILTER:
        cerr << "gpioGlitchFilter(" << gpio << "," << steady << ") -> PI_BAD_FILTER." << endl;
        break;
      default:
        cerr << "gpioGlitchFilter(" << gpio << "," << steady << ") -> UNKNOWN ERROR." << endl;
        break;
    }
    return false;
  };
  auto configureButton = [&](unsigned int btn)
  {
    return logGpioSetMode(btn, PI_INPUT)
        && logGpioSetPullUpDown(btn, PI_PUD_DOWN)
        && logGpioGlitchFilter(btn, 600)
        && logGpioSetAlertFunc(btn, &buttonCallback);
  };
  return configureButton(GPIO_BTN0)
      && configureButton(GPIO_BTN1)
      && logGpioSetMode(GPIO_LED_PWR, PI_OUTPUT);
}

void buttonCallback(int gpio, int level, uint32_t tick)
{
  switch(level)
  {
    case 1: // rising edge
      led_state = 1 - led_state;
cout << "\r" << led_state << flush;
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
  
    gpioWrite(GPIO_LED_PWR, led_state);
    
    gpioSetMode(GPIO_SCALE, PI_OUTPUT);
    gpioPWM(GPIO_SCALE, 25);
  
    cout << "Hit enter key to exit..." << endl;
    cin.get();
    
    gpioPWM(GPIO_SCALE, 0);
  }
  
  gpioTerminate();
  
  return res;
}

