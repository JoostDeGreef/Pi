#include <iostream>
#include <string>
#include <memory>
#include <exception>
#include <set>

namespace GPIO
{
  class enum Mode
  {
    INPUT,
    OUTPUT,
    ALT0,
    ALT1,
    ALT2,
    ALT3,
    ALT4,
    ALT5
  };
  
  class enum PullUpDown
  {
    OFF,
    DOWN,
    UP
  };
  
  class enum ErrorCode
  {
    OK,
    BAD_GPIO,
    BAD_PUD,
    BAD_MODE,
    BAD_FILTER,
    UNKNWON
  };

  class Pin;
  class Library;
  
  class Pin
  {
  public:
    Pin(const unsigned int pin);
    Pin(const Pin & other);
    
    const Pin & GlitchFilter(const unsigned int & steady) const;
    bool Read() const;
    const Pin & SetMode(const GPIO::Mode & mode) const;
    const Pin & SetPullUpDown(const GPIO::PullUpDown & pullUpDown) const;
    void Write(const bool value) const;
    
  private:
    unsigned int m_pin;
  };
  
  class Library
  {
  public:
    static Library & Instance();
    ~Library();
    
  private:
    void Initialize();
    void Terminate();
    
  private:
    Library();
  };
  
  class Exception : public std::runtime_error
  {
  public:
    Exception(const std::string & what);
  };
}

namespace std
{
  std::string to_string(const GPIO::Mode & mode);
  std::string to_string(const GPIO::PullUpDown & pullUpDown);
  std::string to_string(const GPIO::ErrorCode & errorCode);
};

