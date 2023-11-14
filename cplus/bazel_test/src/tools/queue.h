#ifndef QUEUE_H
#define QUEUE_H
#include <mutex>
#include <queue>
namespace tools
{
    template <typename T>
    class SafeQueue
    {
    private:
        std::mutex m_mux;
        std::queue<T> m_queue;

    public:
        SafeQueue() {}
        SafeQueue(SafeQueue &&other) {}
        ~SafeQueue() {}

        bool empty()
        {
            std::unique_lock<std::mutex>(m_mux);
            return m_queue.empty();
        }

        int size()
        {
            std::unique_lock<std::mutex>(m_mux);
            return m_queue.size();
        }

        void enqueue(T &t)
        {
            std::unique_lock<std::mutex>(m_mux);
            m_queue.emplace(t);
        }

        bool dequeue(T &t)
        {
            std::unique_lock<std::mutex>(m_mux);
            if (m_queue.empty())
            {
                return false;
            }
            t = std::move(m_queue.front());
            m_queue.pop();
            return true;
        }
    };
} // namespace tools

#endif