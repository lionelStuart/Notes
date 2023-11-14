#ifndef NONCOPY_H
#define NONCOPY_H

namespace tools
{

    class NonCopyable
    {
    public:
        NonCopyable() = default;
        NonCopyable(const NonCopyable &) = delete;
        NonCopyable &operator=(const NonCopyable &) = delete;
    };
}
#endif