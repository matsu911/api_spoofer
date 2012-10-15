int printf(__const char* format, ...)
{
  va_list args;
  va_start(args, format);
  typedef int (*ftype)(__const char*, ...);
  int ret = ((ftype)dlsym(RTLD_NEXT, "vprintf"))(format, args);
  va_end(args);
  return ret;
}
