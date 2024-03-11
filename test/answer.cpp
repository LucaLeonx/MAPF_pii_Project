#include <catch2/catch_test_macros.hpp>
#define CATCH_CONFIG_MAIN


#include "../source/Answer.h"
#include "../source/Answer.cpp"

// Just a stupid test to check the unit testing system is working
TEST_CASE("The answer to life, universe and everything", "[answer]"){
    Answer a;
    REQUIRE(42 == a.answer());
}