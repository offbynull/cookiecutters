#ifndef "{{ cookiecutter.project_name|upper }}_CLI_CLI_H"
#define "{{ cookiecutter.project_name|upper }}_CLI_CLI_H"

#include "{{ cookiecutter.project_name }}/math/helpers.h"

namespace {{ cookiecutter.project_name }}::cli::cli {
    using {{ cookiecutter.project_name|lower }}::math::helpers::Helpers;

    struct CommandLineInterface {
        int main(int argc, char* argv[]) {
            return Helpers::average({1, 2, 3});
        }
    };
}

#endif // {{ cookiecutter.project_name|upper }}_CLI_CLI_H