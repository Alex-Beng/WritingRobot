#include <thread>
#include <string>
#include <iostream>
using namespace std;

int threadtest(std::string name) {
    while (1) {
        std::cout<<name<<std::endl;
        _sleep(500);
    }
}


int main() {
    auto t1 = std::thread(threadtest, "th1");
    auto t2 = std::thread(threadtest, "th2");
    cout<<std::this_thread::get_id()<<endl;
    cout<<t1.get_id()<<endl;
    cout<<t2.get_id()<<endl;
    
    // t1.detach();
    // t2.detach();

    // t1.join();
    // t2.join();
    return 0;
}