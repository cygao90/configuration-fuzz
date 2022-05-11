# Usage
```
mkdir in out
mkdir in/config_queue in/input_queue
echo a=1 > in/config_queue/test
echo aaaaaa > in/input_queue/test
./afl-fuzz -i in -o out -d ./test out/.cur_config
```

## testcase
```C++
#include <cctype>
#include <cstdio>
#include <iostream>
#include <string>
#include <fstream>
#include <algorithm>
#include <unordered_map>

using namespace std;

int main(int argc, char** argv) {
    if (argc < 2)
        exit(0);
    string config_path(argv[1]);
    string input, line;
    ifstream conf(config_path);
    unordered_map<string, string> m;

    if (!conf.is_open()) {
        printf("Unable to open '%s'.\n", config_path.c_str());
        exit(0);
    }

    while (getline(conf, line)) {
        line.erase(remove_if(line.begin(), line.end(), [](unsigned char x) { return isspace(x); }), line.end());
        if (line.empty()) continue;
        auto equal = line.find('=');
        if (equal == string::npos) {
            exit(0);
        }
        auto key = line.substr(0, equal);
        auto value = line.substr(equal + 1);

        m[key] = value;
        printf("%s = %s\n", key.c_str(), value.c_str());
    }

    cin >> input;

    if (m.find("b") != m.end() && input.length() > 10) {
        int *a = 0;
        *a = 1;
    }

    if (m.find("b") != m.end() && m["b"] == "0") {
        int *a = 0;
        *a = 1;
    }

    if (m.find("c") != m.end() && m["c"] == "10") {
        if (input == "12345") {
            int *a = 0;
            *a = 1; 
        }
    }
    return 0;
}
```