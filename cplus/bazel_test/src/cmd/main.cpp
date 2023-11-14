#include <iostream>
#include "tools/number.h"
#include "tools/pool.h"
#include <vector>
#include <mutex>
#include <stdio.h>
using namespace std;

std::mutex lock;

void calc(int a, int b)
{
    std::unique_lock<std::mutex>(lock);
    std::cout << "calc a+b "
              << "a=" << a << ",b=" << b << ", ret=" << a + b << std::endl;

}

void run_pool()
{
    tools::ThreadPool pool(3);

    pool.init();

    for(int i= 0;i!=100;i++){
        pool.submit(calc, i, i+1);
    }

    pool.wait();

    // }l.shutdown();
}

int main(int argc, char **argv)
{
    std::cout << "test" << std::endl;
    std::cout << "get number=" << tools::NumberTool::number_to_string(2) << std::endl;

    run_pool();
        
    return 0;
}
