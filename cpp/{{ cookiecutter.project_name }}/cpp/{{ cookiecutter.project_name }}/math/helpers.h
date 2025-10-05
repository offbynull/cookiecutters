#ifndef "{{ cookiecutter.project_name|upper }}_MATH_HELPERS_H"
#define "{{ cookiecutter.project_name|upper }}_MATH_HELPERS_H"

#include <vector>
#include <numeric>
#include <concepts>
#include <type_traits>

namespace {{ cookiecutter.project_name|lower }}::math::helpers {
    template <std::integral T>
    struct Helpers {
        static T sum_of_squares(const std::vector<T>& v) {
            return std::accumulate(v.begin(), v.end(), T{0},
                [](T acc, T x) { return acc + x * x; });
        }

        static double average(const std::vector<T>& v) {
            if (v.empty()) return 0.0;
            auto sum = std::accumulate(v.begin(), v.end(), T{0});
            return static_cast<double>(sum) / static_cast<double>(v.size());
        }
    };
}

#endif // {{ cookiecutter.project_name|upper }}_MATH_HELPERS_H