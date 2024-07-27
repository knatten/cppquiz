#include <algorithm>
#include <filesystem>
#include <format>
#include <iostream>
#include <random>
#include <ranges>
#include <string>
#include <vector>

namespace fs = std::filesystem;

struct Question {
    int id;
    std::string porter;
};

std::string exec(const std::string &cmd);
std::vector<Question> get_porters(const fs::path &questions_dir);
std::optional<std::string> get_porter(const fs::path &question);
std::vector<Question> get_winners(const std::vector<Question> &questions);

int main() {
    const auto cwd = fs::current_path();
    const auto questions_dir = cwd / "questions";
    if (!fs::exists(questions_dir)) {
        throw std::runtime_error(
            "Please run this from the root of the porting repo");
    }

    const std::vector<Question> ported_questions = get_porters(questions_dir);
    std::cout << std::format("Found {} questions ported by someone else\n",
                             ported_questions.size());
    std::vector<Question> winners = get_winners(ported_questions);
    std::cout << "\n--- WINNERS ---\n";
    for (const auto &winner : winners) {
        std::cout << std::format("{} (ported question {})\n", winner.porter,
                                 winner.id);
    }
}

std::string trim_trailing_newline(std::string str) {
    str.erase(std::find_if(str.rbegin(), str.rend(),
                           [](char ch) { return ch != '\n'; })
                  .base(),
              str.end());
    return str;
}

std::vector<Question> get_porters(const fs::path &questions_dir) {
    std::vector<Question> ported_questions;
    for (const auto &question_dir : fs::directory_iterator{questions_dir}) {
        const auto porter =
            get_porter(fs::path{"questions"} / question_dir.path().filename());
        if (!porter.has_value()) {
            continue;
        }
        const int id = std::stoi(question_dir.path().filename());
        ported_questions.push_back(Question{id, *porter});
    }
    return ported_questions;
}

// Update these shas next time we port the questions
std::optional<std::string> get_porter(const fs::path &question) {
    const std::string last_commit_before_porting{
        "6349ecaf7e910e22ca0c94c197906b750146f821"};
    // These just fix formatting or in other ways mask the commit that did the
    // bulk of the work
    const std::vector<std::string> ignore_commits{
        "02b5715d05e9134ec55cb6af650eadf21c6f1883",
        "eb171261cf1f5a7399293c2ff8e7aa673174ef95",
        "f609a99e567a33e508888287f0ad9c4649c3f3ba",
        "5cccca9ae6d244ab5d325c28af1ddbadf26882e0",
        "cc48db976c5b2e165b3f51502c48d03f94b19c0f",
        "75559b0516d5d780e34d3a0b1db9c4756c13d345",
        "e0db4c77402277b8015825475928e5b2068d392c",
        "b619e417de305214c61d41a8e00bb9d1d780142c",
        "b9eed3792df987e258775722d8be148b2fd214fe",
        "f2e316dd3cacbbc3122e07d01b93e7ed9ead2e28",
        "7164db908c79281019fbacc99d0425184c4909b6",
        "81a59616ac3136571db08fcca793e89a6ac6b5de",
        "9021d425fb77dc086d47f31e2e929ba3f8c15d3d",
        "3c3685a657dd8215a685d70e9e1f3c680d3a5c3a",
        "aafc0184f1cf0dddedc503bc8d6c0a528ccbd12a",
        "abf92b156f4e87fe75e4b4b06dbbe4bde2d64177",
        "8d3646d3499d75c6e54fb62f0e1ef35542a79404",
        "21dbec818884f01587175fe5fddc7e300a9c9a25",
        "66f02553566fa52d2d47025c00e62e828a2c3997"};

    const auto commits =
        exec(std::format("git log --pretty=format:%H {}.. -- {}",
                         last_commit_before_porting, question.string())) |
        std::views::split('\n') | std::views::transform([](auto &&subrange) {
            return std::string(subrange.begin(), subrange.end());
        }) |
        std::views::filter([&](const auto &sha) {
            return !std::ranges::contains(ignore_commits, sha);
        }) |
        std::ranges::to<std::vector>();
    if (commits.empty()) {
        std::cout << std::format("{} was not ported\n", question.string());
        return {};
    }
    const auto porter = trim_trailing_newline(exec(
        std::format("git show --no-patch --format=%ae {}", commits.front())));
    if (porter == "anders@knatten.org") {
        std::cout << std::format("{} was ported by Anders, ignoring\n",
                                 question.string());
        return {};
    }
    std::cout << std::format("{} was ported by {}\n", question.string(),
                             porter);
    return porter;
}

std::vector<Question> get_winners(const std::vector<Question> &questions) {
    std::vector<Question> winners;
    std::random_device device;
    std::mt19937 generator{device()};
    std::uniform_int_distribution<size_t> distribution(0, questions.size() - 1);
    while (winners.size() < 3) {
        const auto &potential_winner = questions[distribution(generator)];
        if (std::ranges::find_if(winners, [&](const auto &winner) {
                return winner.porter == potential_winner.porter;
            }) == winners.end()) {
            winners.push_back(potential_winner);
        }
    }
    return winners;
}

// Based on https://stackoverflow.com/a/478960/7084
std::string exec(const std::string &cmd) {
    std::array<char, 1024> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"),
                                                  pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), static_cast<int>(buffer.size()), pipe.get()) !=
           nullptr) {
        result += buffer.data();
    }
    return result;
}
