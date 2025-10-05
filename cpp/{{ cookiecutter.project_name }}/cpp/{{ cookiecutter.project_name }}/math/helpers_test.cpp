#include "gtest/gtest.h"
#include "{{ cookiecutter.project_name }}/math/helpers.h"

namespace {
    using {{ cookiecutter.project_name|lower }}::math::helpers::Helpers;
    
    TEST({{ cookiecutter.project_name[:1]|upper }}MHelpersTest, MustGetSumOfSquares) {
        EXPECT_EQ(
            14,
            (Helpers<int>::sum_of_squares({1, 2, 3}))
        );
    }

    TEST({{ cookiecutter.project_name[:1]|upper }}MHelpersTest, MustGetAverage) {
        EXPECT_EQ(
            2,
            (Helpers<int>::average({1, 2, 3}))
        );
    }
}