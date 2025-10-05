#include <iostream>
#include <Poco/ASCIIEncoding.h>
#include "main.hpp"

int main() {
    std::cout << "helloworld" << std::endl << Poco::ASCIIEncoding().canonicalName();
    return 0;
}