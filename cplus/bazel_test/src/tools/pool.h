#ifndef POOL_H
#define POOL_H

#include <iostream>
#include <functional>
#include <mutex>
#include <thread>
#include <future>
#include <utility>
#include <vector>
#include <atomic>
#include "tools/noncopy.h"
#include "tools/queue.h"

namespace tools
{

    class ThreadPool : public NonCopyable
    {
    private:
        std::atomic<bool> m_shutdown;

        std::mutex m_conditional_mutex;

        std::condition_variable m_conditional_lock;

        std::vector<std::thread> m_threads;

        SafeQueue<std::function<void()>> m_queue;

    public:
        class ThreadWorker
        {
        private:
            int m_id;
            ThreadPool *m_pool;

        public:
            ThreadWorker(ThreadPool *pool, const int id) : m_pool(pool), m_id(id)
            {
                std::cout << "create worker id=" << id << std::endl;
            }
            void operator()()
            {
                std::function<void()> func;

                bool dequeued;

                while (!m_pool->m_shutdown)
                {
                    {
                        std::unique_lock<std::mutex> lock(m_pool->m_conditional_mutex);
                        if (m_pool->m_queue.empty())
                        {
                            m_pool->m_conditional_lock.wait(lock);
                        }
                        dequeued = m_pool->m_queue.dequeue(func);
                    }
                    if (dequeued)
                    {
                        func();
                    }
                }
            }
        };

        ThreadPool(const int paralesim = 3) : m_shutdown(false),
                                              m_threads(std::vector<std::thread>(paralesim))
        {
        }

        void init()
        {
            for (auto i = 0; i != m_threads.size(); ++i)
            {
                m_threads.at(i) = std::thread(ThreadWorker(this, i));
            }
        }

        void shutdown()
        {
            m_shutdown = true;
            m_conditional_lock.notify_all();

            for (auto i = 0; i != m_threads.size(); ++i)
            {
                if (m_threads.at(i).joinable())
                {
                    m_threads.at(i).join();
                }
            }
        }

        void wait()
        {
            for (auto i = 0; i != m_threads.size(); ++i)
            {
                if (m_threads.at(i).joinable())
                {
                    m_threads.at(i).join();
                }
            }
        }

        template <typename F, typename... Args>
        auto submit(F &&f, Args &&...args) -> std::future<decltype(f(args...))>
        {
            std::function<decltype(f(args...))()> func = std::bind(std::forward<F>(f),
                                                                   std::forward<Args>(args)...);
            auto task_ptr = std::make_shared<std::packaged_task<decltype(f(args...))()>>(func);

            std::function<void()> warpper_func = [task_ptr]()
            {
                (*task_ptr)();
            };

            m_queue.enqueue(warpper_func);
            m_conditional_lock.notify_one();
            return task_ptr->get_future();
        }
    };

}
#endif