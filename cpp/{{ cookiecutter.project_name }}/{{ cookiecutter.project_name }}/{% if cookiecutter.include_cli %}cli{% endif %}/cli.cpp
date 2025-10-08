#include "{{ cookiecutter.project_name }}/cli/cli.h"

// Do not modify.
int main(int argc, char* argv[]) {
    return {{ cookiecutter.project_name }}::cli::cli::CommandLineInterface {}.main(argc, argv);
}