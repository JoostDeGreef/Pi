#include "pigpio++.hpp"

extern "C"
{
  #include <pigpio.h>
}

using namespace std;
using namespace GPIO;

namespace 
{
void ReportError(string s)
{
  throw Exception(s);
}
void ReportError(int res, string s,
  int c0, Error e0)
{
  if(res==c0) ReportError(s+to_string(e0));
  else ReportError(s+"UNKNOWN");
}
void ReportError(int res, string s,
  int c0, Error e0,
  int c1, Error e1
{
  if(res==c1) ReportError(s+to_string(e1));
  else ReportError(res,s,c0,e0);  
}
void ReportError(int res, string s,
  int c0, Error e0,
  int c1, Error e1,
  int c2, Error e2
{
  if(res==c2) ReportError(s+to_string(e2));
  else ReportError(res,s,c0,e0,c1,e1);  
}

int gpioSetMode(const unsigned int pin, const GPIO::MODE & mode)
{
  return 0;
}

};

Pin::Pin(const unsigned int pin)
  : m_pin(pin)
{
  Library::Instance();
}

Pin::Pin(const Pin & other)
  : m_pin(other.m_pin)
{}
    
const Pin & Pin::GlitchFilter(const unsigned int & steady) const
{
  auto res = gpioGlitchFilter(m_pin, steady);
  if(PI_OK != res)
  {
    ReportError(res, 
      "gpioGlitchFilter("+to_string(m_pin)+","+to_string()+") -> ",
      PI_OK,         Error::OK,
      PI_BAD_GPIO,   Error::BAD_GPIO,
      PI_BAD_FILTER, Error::BAD_FILTER);
  }
  return *this;
}

bool Pin::Read() const
{
}

const Pin & Pin::SetMode(const GPIO::Mode & mode) const
{
  WrapFunction(
    gpioSetMode(m_pin, mode),
    PI_OK,         Error::OK,
    PI_BAD_GPIO,   Error::BAD_GPIO,
    PI_BAD_MODE,   Error::BAD_MODE
  );
  return *this;
}

const Pin & Pin::SetPullUpDown(const GPIO::PullUpDown & pullUpDown) const
{}

void Pin::Write(const bool value) const
{}
    
Library & Library::Instance()
{
  static Library library;
  return library;
}
    
void Library::Initialize()
{
}

void Library::Terminate()
{
}
    
Library::Library()
{
  Initialize();
}

Library::~Library()
{
  Terminate();
}
  
Exception::Exception(const std::string & what)
  : std::runtime_error(what)
{}

std::string to_string(const GPIO::Mode & mode)
{
  return "";
}

std::string to_string(const GPIO::PullUpDown & pullUpDown)\
{
  return "";
}

std::string to_string(const GPIO::ErrorCode & errorCode)
{
  return "";
}

